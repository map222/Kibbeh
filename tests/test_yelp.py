# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:32:53 2015

@author: Chauncey
"""

import json
import pandas as pd
from nose.tools import assert_equals
import Kibbeh.src.feature_calc as feature_calc
import ast

working_dir = 'C:\\Users\\Chauncey\\Documents\\GitHub\\Kibbeh\\tests\\'
#working_dir = 'C:\\Users\\Me\\Documents\\GitHub\\Kibbeh'

# load yelp
with open(working_dir + 'test_data\\yelp_restaurant_test.json', 'r') as json_file:
    yelp_restos = json.load( json_file)
        
with open(working_dir + 'test_data\\yelp_test_df.csv', 'r', encoding='utf8') as csv_file:
    yelp_df = pd.read_csv(csv_file, sep=';', index_col='name', dtype={'phone':str})
    yelp_df['categories'] = yelp_df['categories'].apply(ast.literal_eval )

def test_parse_single_resto():
    assert yelp_df.head(1).equals( feature_calc.feature_extract_yelp_json(yelp_restos[0]) )
    
def test_parse_list_restos():
    assert yelp_df.equals(feature_calc.feature_extract_yelp_list(yelp_restos))