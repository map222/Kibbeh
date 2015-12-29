# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:01:14 2015

@author: Chauncey
"""

import time

def get_top_restos_zip_4square(foursquare_client, zip_list):
    ''' Load top 250 restaurants in different price ranges and zip codes
    
    Arguments:
        foursquare_client: FourSquare object initiated with api_key
        zip_list: integer list of zip codes to search through
    '''
    restaurant_data = []
    query_limit = 50
    
    # get list of top 250 restaurants in each price bracket
    offset_list = range(0, 251, query_limit)
    price_list = range(1,5)
    for cur_zip in zip_list:
        print(cur_zip)
        for cur_offset in offset_list:
            for cur_price in price_list:
                zip_params = {'near': str(cur_zip), 'section': 'food', 
                                     'limit': query_limit, 'offset': cur_offset, 'price': cur_price}
                cur_query = foursquare_client.venues.explore(params=zip_params)
                #pdb.set_trace()
                restaurant_data.extend( cur_query['groups'][0]['items'])
                time.sleep(0.5)
    return restaurant_data
