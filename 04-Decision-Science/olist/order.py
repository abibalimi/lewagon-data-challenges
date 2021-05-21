import os
import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''

    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        02-01 > Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filtering out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        #self.data = self.data[self.data['order_status'] == 'delivered']
        orders = self.data['orders'].copy()
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
        orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
        
        result_df = pd.DataFrame()
        
        result_df['order_id'] = orders['order_id']
        result_df['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
        result_df['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']).dt.days
        result_df['delay_vs_expected'] = (result_df['wait_time'] - result_df['expected_wait_time'])\
            .apply(lambda x: np.abs(x) if x > 0 else 0)
        result_df['order_status'] = orders['order_status']
        return result_df.query("order_status == 'delivered'")
    
    def get_review_score(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()

        def dim_five_star(item):
            return 1 if item == 5 else 0

        def dim_one_star(item):
            return 1 if item == 1 else 0
        
        result_df = pd.DataFrame()
        result_df['order_id'] = reviews['order_id']
        result_df['dim_is_five_star'] = reviews["review_score"].map(dim_five_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        result_df["dim_is_one_star"] = reviews["review_score"].map(dim_one_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        result_df['review_score'] = reviews['review_score']
        
        return result_df
    
    
    def get_number_products(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, number_of_products
        """
        items = self.data['order_items'].copy()
        return items[["order_id","product_id"]].groupby("order_id").count()\
            .rename(columns={'product_id':'number_of_products'})
        
        
    def get_number_sellers(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, number_of_sellers
        """
        items = self.data['order_items'].copy()
        return items[['order_id','seller_id']].groupby('order_id').count()\
            .rename(columns={'seller_id':'number_of_sellers'})
    def get_price_and_freight(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, price, freight_value
        """
        items = self.data['order_items'].copy()
        return items[['order_id','price','freight_value']].groupby('order_id').sum()

    #def get_distance_seller_customer(self):
    #    """
    #    02-01 > Returns a DataFrame with order_id
    #    and distance between seller and customer
    #    """
        # Optional
        # Hint: you can use the haversine_distance logic coded in olist/utils.py

        """     def get_training_data(self, is_delivered=True,
                          with_distance_seller_customer=False):
        """
        #02-01 > Returns a clean DataFrame (without NaN), with the following columns:
        #[order_id, wait_time, expected_wait_time, delay_vs_expected, order_status,
        #dim_is_five_star, dim_is_one_star, review_score, number_of_products,
        #number_of_sellers, freight_value, distance_customer_seller]
        """
        # Hint: make sure to re-use your instance methods defined above
        
        result = self.get_wait_time()\
            .merge(self.get_review_score(), on='order_id')\
                .merge(self.get_number_products(), on='order_id')\
                    .merge(self.get_number_sellers(), on='order_id')\
                        .merge(self.get_price_and_freight(), on='order_id')
        
        return result.dropna() """
                
        # Optional
    def get_distance_seller_customer(self):
        """
        02-01 > Returns a DataFrame with order_id
        and distance between seller and customer
        """

        # import data

        data = self.data
        matching_table = Olist().get_matching_table()

        # Since one zipcode can map to multiple (lat, lng), take first one
        geo = data['geolocation']
        geo = geo.groupby('geolocation_zip_code_prefix',
                          as_index=False).first()

        # Select sellers and customers
        sellers = data['sellers']
        customers = data['customers']

        # Merge geo_location for sellers
        sellers_mask_columns = ['seller_id', 'seller_zip_code_prefix',
                                'seller_city', 'seller_state',
                                'geolocation_lat', 'geolocation_lng']

        sellers_geo = sellers.merge(
            geo,
            how='left',
            left_on='seller_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[sellers_mask_columns]

        # Merge geo_location for customers
        customers_mask_columns = ['customer_id', 'customer_zip_code_prefix',
                                  'customer_city', 'customer_state',
                                  'geolocation_lat', 'geolocation_lng']

        customers_geo = customers.merge(
            geo,
            how='left',
            left_on='customer_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[customers_mask_columns]

        # Use the matching table and merge customers and sellers
        matching_geo = matching_table.merge(sellers_geo,
                                            on='seller_id')\
                                     .merge(customers_geo,
                                            on='customer_id',
                                            suffixes=('_seller',
                                                      '_customer'))
        # Remove na()
        matching_geo = matching_geo.dropna()

        matching_geo.loc[:, 'distance_seller_customer'] =\
            matching_geo.apply(
                lambda row: haversine_distance(
                    row['geolocation_lng_seller'],
                    row['geolocation_lat_seller'],
                    row['geolocation_lng_customer'],
                    row['geolocation_lat_customer']), axis=1)
        # Since an order can have multiple sellers,
        # return the average of the distance per order
        order_distance =\
            matching_geo.groupby(
                'order_id',
                as_index=False).agg({'distance_seller_customer': 'mean'})

        return order_distance

    def get_training_data(self, is_delivered=True,
                          with_distance_seller_customer=False):
        """
        02-01 > Returns a clean DataFrame (without NaN), with the following
        columns: [order_id, wait_time, expected_wait_time, delay_vs_expected,
        dim_is_five_star, dim_is_one_star, review_score, number_of_products,
        number_of_sellers, price, freight_value, distance_customer_seller]
        """
        # Hint: make sure to re-use your instance methods defined above
        training_set =\
            self.get_wait_time(is_delivered)\
                .merge(
                self.get_review_score(), on='order_id'
               ).merge(
                self.get_number_products(), on='order_id'
               ).merge(
                self.get_number_sellers(), on='order_id'
               ).merge(
                self.get_price_and_freight(), on='order_id'
               )
        # Skip heavy computation of distance_seller_customer unless specified
        if with_distance_seller_customer:
            training_set = training_set.merge(
                self.get_distance_seller_customer(), on='order_id')

        return training_set.dropna()