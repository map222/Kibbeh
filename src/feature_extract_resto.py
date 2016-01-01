# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:00:57 2015

@author: Chauncey
"""

import pandas as pd

# yelp feature extraction
def feature_extract_yelp_list(json_list):
    ''' get features for each restaurant, and return use pandas concat to get them'''
    return pd.concat(map(feature_extract_yelp_json, json_list))

def feature_extract_yelp_json(cur_json):
    ''' extract features from a single json element'''
    #print(cur_json['name'])
    feature_list = ('id', 'rating', 'categories', 'name', 'phone', 'review_count')
    cur_dict = dict((x, cur_json[x]) for x in feature_list if x in cur_json.keys())
    cur_dict['categories'] = [[x[0] for x in cur_dict['categories']]]
    return pd.DataFrame(cur_dict).set_index('name')

# yelp feature extraction
def feature_extract_fs_list(fs_json_list):
    ''' get features for each restaurant, and return use pandas concat to get them'''
    return pd.concat(map(feature_extract_fs_json, fs_json_list))

def feature_extract_fs_json(cur_json):
    cur_venue= cur_json['venue']
    
    # get base features
    feature_list = ('id', 'rating', 'categories', 'name', 'rating', 'price', 'stats', 'contact')
    #pdb.set_trace()
    cur_dict = dict((x, cur_venue[x]) for x in feature_list if x in cur_venue.keys())
    
    # extract nested features
    nest_features = [['price','tier'], ['stats','checkinsCount'], ['stats','tipCount'],
                     ['stats','usersCount'], ['contact', 'phone']]
    for key, nested_key in nest_features:
        if nested_key in cur_dict[key].keys():
            cur_dict[nested_key] = cur_dict[key][nested_key] 
        
    # get categories
    new_cat = []
    for cur_cat in cur_dict['categories']:
        new_cat.append( cur_cat['shortName'])
    cur_dict['categories'] = new_cat
    
    # drop nested features that we have
    drop_keys = ['contact', 'price', 'stats']
    for key in drop_keys:
        cur_dict.pop(key)
        
    return pd.DataFrame(cur_dict).set_index('name')