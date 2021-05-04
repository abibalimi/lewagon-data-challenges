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

    def get_distance_seller_customer(self):
        """
        02-01 > Returns a DataFrame with order_id
        and distance between seller and customer
        """
        # Optional
        # Hint: you can use the haversine_distance logic coded in olist/utils.py

    def get_training_data(self, is_delivered=True,
                          with_distance_seller_customer=False):
        """
        02-01 > Returns a clean DataFrame (without NaN), with the following columns:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status,
        dim_is_five_star, dim_is_one_star, review_score, number_of_products,
        number_of_sellers, freight_value, distance_customer_seller]
        """
        # Hint: make sure to re-use your instance methods defined above
        
        result = self.get_wait_time()\
            .merge(self.get_review_score(), on='order_id')\
                .merge(self.get_number_products(), on='order_id')\
                    .merge(self.get_number_sellers(), on='order_id')\
                        .merge(self.get_price_and_freight(), on='order_id')
        
        return result.dropna()
                
        