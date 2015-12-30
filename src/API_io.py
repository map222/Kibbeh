# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:01:14 2015

@author: Chauncey
"""

import time
import numpy as np

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

def get_menus_fs(foursquare_client, fs_id_list ):
    ''' Downloads menus from foursquare, using foursquare id's for restaurants
    
    fs_id_list: a list or numpy array of strings that have foursquare id's for venues.
    '''
    
    fs_id_list = np.unique(np.array(fs_id_list)) # make sure they are unique
    
    restaurant_menus = []
    counter = 0
    for cur_fs_id in fs_id_list:
        counter+=1
        
        # get a menu, and put the id in the dictionary
        temp_menu = foursquare_client.venues.menu( cur_fs_id )
        temp_menu['menu']['id'] = cur_fs_id
        #pdb.set_trace()
        if 'provider' in temp_menu['menu'].keys(): # make sure the menu has items (API has less menus than website)
            restaurant_menus.append( temp_menu['menu'] )
        elif temp_menu['menu']['menus']['count'] >0: # check to make sure above wo
            print('Menu with no provider has items for restaurant: {0}'.format(cur_fs_id))
            
        if counter % 50 == 0: # ghetto logging
            print(str(counter))
        time.sleep(0.75)
    return restaurant_menus