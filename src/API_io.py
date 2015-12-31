# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:01:14 2015

@author: Chauncey
"""

import time
import numpy as np

def remove_duplicate_fs_restos(fs_resto_list):
    fs_id_set = {x['venue']['id'] for x in fs_resto_list}
    new_fs_restos = []
    for cur_resto in fs_resto_list:
        #pdb.set_trace()
        if cur_resto['venue']['id'] in fs_id_set:
            fs_id_set.remove(cur_resto['venue']['id'])
            new_fs_restos.append(cur_resto)
    return new_fs_restos

def get_fs_top_restos_zip(foursquare_client, zip_list):
    ''' Load top 250 restaurants in different price ranges and zip codes
    
    Arguments:
        foursquare_client: FourSquare object initiated with api_key
        zip_list: integer list of zip codes to search through
    '''
    resto_list = []
    query_limit = 50
    
    # get list of top 250 restaurants in each price bracket
    offset_list = range(0, 251, query_limit)
    price_list = range(1,5)
    for cur_zip in zip_list:
        print('Download data for {0} zip code.'.format(cur_zip))
        for cur_offset in offset_list:
            for cur_price in price_list:
                zip_params = {'near': str(cur_zip), 'section': 'food', 
                                     'limit': query_limit, 'offset': cur_offset, 'price': cur_price}
                cur_query = foursquare_client.venues.explore(params=zip_params)
                #pdb.set_trace()
                resto_list.extend( cur_query['groups'][0]['items'])
                time.sleep(0.5)
    return remove_duplicate_fs_restos(resto_list)

def get_fs_menus(foursquare_client, fs_id_list ):
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
    
def get_fs_restos_by_ll(grid_values, foursquare_client, grid_step = 0.01, grid_radius=250):
    ''' get restaurants by latitude and longitude
        most restaurants returned by this do not have ratings
        '''
    restaurant_data = []
    query_limit = 50
    
    # set up longitude latitude grid
    grid_step = 0.01
    x_range = np.arange(grid_values[0], grid_values[1], grid_step)
    y_range = np.arange(grid_values[2], grid_values[3], grid_step)
    
    for x in x_range:
        for y in y_range:
            #pdb.set_trace
            string_ll = str(y) + ',' +str(x)
            grid_params = {'ll': string_ll, 'categoryId': '4d4b7105d754a06374d81259',
                                                      'radius': grid_radius, 'limit': query_limit}
            cur_query = foursquare_client.venues.search(params=grid_params)
            #pdb.set_trace()
            restaurant_data.extend(cur_query['venues'])
            time.sleep(0.5)
    return restaurant_data

    
def get_yelp_restaurants(yelp_api):
    restaurant_data = []
    for cur_offset in range(0, 1000, 20):
        # sort = 0 sets by default, limited to 1000, sort = 2 is ranked from best to worst, but limited to 40
        cur_query = yelp_api.search_query(term='food', location = 'Seattle', sort=0, limit=20, offset = cur_offset) 
        #pdb.set_trace()
        restaurant_data.extend( cur_query['businesses'])
    return restaurant_data