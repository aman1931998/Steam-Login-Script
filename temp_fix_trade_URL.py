# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:03:30 2021

@author: aman1
"""

import pandas as pd
import pickle
import os

with open(os.path.join('dynamic', 'accounts_trade_url_copied.pkl'), 'rb') as file:
    tuc = pickle.load(file)


data = pd.read_excel('aman_batch_2.xlsx')
steamids = data['SteamID'].tolist()
usernames = data['Username'].tolist()

l_error = ['ignorant6327dispensable305', 'blink82exultant42', 'swing6unadvised0566']

# for i in tuc: #i = tuc[0]
#     get_index = usernames.index(i)
#     steamid = str(steamids[get_index])
#     trade_url = open(os.path.join('account_trade_url', i + ".txt"), 'r').read()
#     if steamid not in trade_url:
#         l_error.append(i)
#         print(i)


with open(os.path.join('dynamic', 'accounts_trade_url_copied.pkl'), 'wb') as file:
    #tuc = pickle.load(file)
    pickle.dump(tuc, file)



from helper_functions import *


acc_loaded = load_list_of_accounts_logged_in()
for i in l_error:
    try:
        acc_loaded.remove(i)
    except:
        print(i)
save_list_of_accounts_logged_in(acc_loaded)

acc_loaded = load_list_of_accounts_profile_setup_done()
for i in l_error:
    try:
        acc_loaded.remove(i)
    except:
        print(i)
save_list_of_accounts_profile_setup_done(acc_loaded)

acc_loaded = load_list_of_accounts_profile_privacy_changed()
for i in l_error:
    try:
        acc_loaded.remove(i)
    except:
        print(i)
save_list_of_accounts_profile_privacy_changed(acc_loaded)

acc_loaded = load_list_of_accounts_trade_url_copied()
for i in l_error:
    try:
        acc_loaded.remove(i)
    except:
        print(i)
save_list_of_accounts_trade_url_copied(acc_loaded)

for i in l_error:
    os.remove(os.path.join('account_trade_url', i + ".txt"))
    print(i)
