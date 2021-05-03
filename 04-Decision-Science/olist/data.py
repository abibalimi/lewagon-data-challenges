import os
import pandas as pd


class Olist:

    def get_data(self):
        #import ipdb; ipdb.set_trace()
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrame loaded from csv files
        """
        # Hints: Build csv_path as "absolute path" in order to call this method from anywhere.
        # Do not hardcode your path as it only works on your machine ('Users/username/code...')
        # Use __file__ as absolute path anchor independant of your computer
        # Make extensive use of `import ipdb; ipdb.set_trace()` to investigate what `__file__` variable is really
        # Use os.path library to construct path independent of Unix vs. Windows specificities
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data','csv')
        file_names = [fname for fname in os.listdir(csv_path) if fname.endswith('.csv')]
        key_names = [kname[6:-12] if '_dataset.csv' in kname else kname[:-4] for kname in file_names]
        data_frames = [pd.read_csv(os.path.join(csv_path, csv)) for csv in file_names]
        data = {key: value for (key,value) in zip(key_names,data_frames)}

        return data
        
    def get_matching_table(self):
        """
        01-01 > This function returns a matching table between
        columns [ "order_id", "review_id", "customer_id", "product_id", "seller_id"]
        """

    def ping(self):
        """
        You call ping I print pong.
        """
        print('pong')

ol = Olist()
ol.get_data()