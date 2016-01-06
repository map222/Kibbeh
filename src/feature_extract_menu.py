# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 16:35:32 2015

@author: Chauncey
"""

from nltk.corpus import stopwords
import json
import re
from collections import Counter

def remove_duplicate_fs_menus(fs_menu_list):
    fs_id_set = {x['id'] for x in fs_menu_list}
    new_fs_menus = []
    for cur_menu in fs_menu_list:
        #pdb.set_trace()
        if cur_menu['id'] in fs_id_set:
            fs_id_set.remove(cur_menu['id'])
            new_fs_menus.append(cur_menu)
    return new_fs_menus

stop_words = set(stopwords.words('english'))
def wordify_json_menu(json_menu, stop_words):
    ''' Converts the dictionary representation of a menu to a simple list of words
    
    json_menu: a dictionary / json from foursquare of a restaurant menu
    '''
    dumb_keys = {'name', 'count', 'items', 'Main', 'Menu', # yelp
                 'description', 'entries', 'price', 'prices',
                 'section_name', 'subsections', 'currency_symbol',
                 'menu_name', 'type', 'item' # locu
                 }
    cur_menu = json_menu
    string_menu = json.dumps(cur_menu)
    letters_only_menu =re.sub("[^a-zA-Z0-9]", " ", string_menu )
    letters_only_menu = letters_only_menu.lower()
    menu_words = letters_only_menu.split() # split into words
    menu_words = [w for w in menu_words if len(w) > 2] # get rid of 1-2 letter words
    menu_words = [w for w in menu_words if w not in stop_words]
    menu_words = [w for w in menu_words if w not in dumb_keys]
    [menu_words, num_items,  num_sections, num_menus ] = count_menu_items(menu_words)
    return ' '.join(menu_words), num_items,  num_sections, num_menus
    
def count_menu_items( menu_words):
    ''' Count the number of menus, and number of items in each menu.
        Then remove them from the menu
        
        menu_words: a list of words on the menu'''
        
    counted_menu = Counter( menu_words)
    num_menus = counted_menu['menuid']
    num_items = counted_menu['entryid']
    num_sections = counted_menu['sectionid']
    # delete these words from menu
    #menu_words = [w for w in menu_words if w not in {'entryid', 'menuid', 'sectionid'}]
    return menu_words, num_items,  num_sections, num_menus 