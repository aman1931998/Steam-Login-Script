import pyperclip as pc
import time
import subprocess
import pickle
import pandas as pd
import os
import numpy as np
from datetime import datetime
from mouse_functions import press_and_release, click_only, hover_only
import config as cfg

from positions import STEAM_PROFILE_PRIVACY_INVENTORY_X, STEAM_PROFILE_PRIVACY_INVENTORY_Y, \
    STEAM_PROFILE_PRIVACY_INVENTORY_DROP_DOWN_MENU_PUBLIC_X, STEAM_PROFILE_PRIVACY_INVENTORY_DROP_DOWN_MENU_PUBLIC_Y, \
        STEAM_PROFILE_PRIVACY_PAGE_BLANK_X, STEAM_PROFILE_PRIVACY_PAGE_BLANK_Y

def get_active_usernames(path = cfg.PATH_TO_ACTIVE_ACCOUNTS):
    return pd.read_excel(path)['Username'].tolist()

#%% Error
def load_list_of_accounts_with_error():
    try:
        with open(os.path.join('dynamic', 'accounts_with_error.pkl'), 'rb') as file:
            return pickle.load(file)
    except:
        return []

def load_detailed_dict_of_accounts_with_error():
    try:
        with open(os.path.join('dynamic', "accounts_with_error_detailed.pkl"), 'rb') as file:
            return pickle.load(file)
    except:
        return {}

def save_detailed_dict_of_accounts_with_error(dict_accounts_with_error):
    try:
        with open(os.path.join('dynamic', 'accounts_with_error_detailed.pkl'), 'wb') as file:
            pickle.dump(dict_accounts_with_error, file)
        return True
    except:
        return False

def save_list_of_accounts_with_error(list_accounts_with_error):
    try:
        with open(os.path.join('dynamic', 'accounts_with_error.pkl'), 'wb') as file:
            pickle.dump(list_accounts_with_error, file)
        return True
    except:
        return False

def add_account_to_accounts_with_error(account_name, error_name = 'default'):
    dict_accounts_with_error = load_detailed_dict_of_accounts_with_error()
    list_accounts_with_error = load_list_of_accounts_with_error()
    if account_name in list_accounts_with_error:
        found_error_name = ""
        for e in dict_accounts_with_error.keys():
            if account_name in dict_accounts_with_error[e]:
                found_error_name = e
                break
        if error_name == e:
            print("Similar Error Received.")
            return
        else:
            print("Already in Accounts with error database marked with Error: %s"%(found_error_name))
            print("Updating account name: %s with error: %s"%(account_name, error_name))
    list_accounts_with_error.append(str(account_name))
    if error_name in dict_accounts_with_error.keys():
        dict_accounts_with_error[error_name].append(account_name)
    else:
        dict_accounts_with_error[error_name] = [account_name]
    output = save_list_of_accounts_with_error(list_accounts_with_error)
    if not output: 
        raise Exception("Error occured while saving accounts_with_error.pkl file.")
    try:
        output = save_detailed_dict_of_accounts_with_error(dict_accounts_with_error)
    except:
        raise Exception("Error occured while saving accounts_with_error.pkl file.")

#%% Stage 1: Logged in
def load_list_of_accounts_logged_in():
    try:
        with open(os.path.join('dynamic', 'accounts_logged_in.pkl'), 'rb') as file:
            return pickle.load(file)
    except:
        return []

def save_list_of_accounts_logged_in(list_accounts_logged_in):
    try:
        with open(os.path.join('dynamic', 'accounts_logged_in.pkl'), 'wb') as file:
            pickle.dump(list_accounts_logged_in, file)
        return True
    except:
        return False

def add_account_to_accounts_logged_in(account_name):
    list_accounts_logged_in = load_list_of_accounts_logged_in()
    if account_name in list_accounts_logged_in:
        print("Already in Accounts with error database")
        return False
    list_accounts_logged_in.append(str(account_name))
    output = save_list_of_accounts_logged_in(list_accounts_logged_in)
    if not output: 
        raise Exception("Error occured while saving accounts_logged_in.pkl file.")

#%% Stage 2: Profile setup done
def load_list_of_accounts_profile_setup_done():
    try:
        with open(os.path.join('dynamic', 'accounts_profile_setup_done.pkl'), 'rb') as file:
            return pickle.load(file)
    except:
        return []

def save_list_of_accounts_profile_setup_done(list_accounts_profile_setup_done):
    try:
        with open(os.path.join('dynamic', 'accounts_profile_setup_done.pkl'), 'wb') as file:
            pickle.dump(list_accounts_profile_setup_done, file)
        return True
    except:
        return False

def add_list_of_accounts_profile_setup_done(account_name):
    list_accounts_profile_setup_done = load_list_of_accounts_profile_setup_done()
    if account_name in list_accounts_profile_setup_done:
        print("Already in Accounts with profile setup done database.")
        return False
    list_accounts_profile_setup_done.append(account_name)
    output = save_list_of_accounts_profile_setup_done(list_accounts_profile_setup_done)
    if output == False:
        raise Exception("Error occured while saving accounts_profile_setup_done.pkl")

#%% Stage 3: Privacy Changed
def load_list_of_accounts_profile_privacy_changed():
    try:
        with open(os.path.join('dynamic', 'accounts_profile_privacy_changed.pkl'), 'rb') as file:
            return pickle.load(file)
    except:
        return []

def save_list_of_accounts_profile_privacy_changed(list_accounts_profile_privacy_changed):
    try:
        with open(os.path.join('dynamic', 'accounts_profile_privacy_changed.pkl'), 'wb') as file:
            pickle.dump(list_accounts_profile_privacy_changed, file)
        return True
    except:
        return False

def add_list_of_accounts_profile_privacy_changed(account_name):
    list_accounts_profile_privacy_changed = load_list_of_accounts_profile_privacy_changed()
    if account_name in list_accounts_profile_privacy_changed:
        print("Already in Accounts with profile privacy changed database.")
        return False
    list_accounts_profile_privacy_changed.append(account_name)
    output = save_list_of_accounts_profile_privacy_changed(list_accounts_profile_privacy_changed)
    if output == False:
        raise Exception("Error occured while saving accounts_profile_privacy_changed.pkl")

#%% Trade URL copied.
def load_list_of_accounts_trade_url_copied():
    try:
        with open(os.path.join('dynamic', 'accounts_trade_url_copied.pkl'), 'rb') as file:
            return pickle.load(file)
    except:
        return []

def save_list_of_accounts_trade_url_copied(list_accounts_trade_url_copied):
    try:
        with open(os.path.join('dynamic', 'accounts_trade_url_copied.pkl'), 'wb') as file:
            pickle.dump(list_accounts_trade_url_copied, file)
        return True
    except:
        return False

def add_list_of_accounts_trade_url_copied(account_name):
    list_accounts_trade_url_copied = load_list_of_accounts_trade_url_copied()
    if account_name in list_accounts_trade_url_copied:
        print("Already in Accounts with trade URL copied database.")
        return False
    list_accounts_trade_url_copied.append(account_name)
    output = save_list_of_accounts_trade_url_copied(list_accounts_trade_url_copied)
    if output == False:
        raise Exception("Error occured while saving accounts_trade_url_copied.pkl")

def save_account_completion_timestamp(username):
    with open(os.path.join('account_completion_date', username + ".txt"), 'w') as file:
        file.write(str(datetime.now()))
    return True

#%% Getting accounts in dict 
def get_active_accounts(account_sheet_path = cfg.PATH_TO_ACCOUNT_SHEET):
    all_accounts = pd.read_excel(account_sheet_path)['Username'].tolist()

    list_accounts_logged_in = load_list_of_accounts_logged_in()
    list_accounts_profile_setup_done = load_list_of_accounts_profile_setup_done()
    list_accounts_profile_privacy_changed = load_list_of_accounts_profile_privacy_changed()
    list_accounts_trade_url_copied = load_list_of_accounts_trade_url_copied()
    dict_accounts_with_error = load_detailed_dict_of_accounts_with_error()

    active_accounts = {"All Accounts": all_accounts, 
                       "Logged In": list_accounts_logged_in, 
                       "Profile Setup Done": list_accounts_profile_setup_done, 
                       "Privacy Changed": list_accounts_profile_privacy_changed, 
                       "Trade URL Copied": list_accounts_trade_url_copied, 
                       "Error Dict": dict_accounts_with_error}
    print("#Accounts Logged In: %d"%(len(list_accounts_logged_in)))
    print("#Accounts Profile Setup Done: %d"%(len(list_accounts_profile_setup_done)))
    print("#Accounts Privacy Changed: %d"%(len(list_accounts_profile_privacy_changed)))
    print("#Accounts Trade URL Copied: %d"%(len(list_accounts_trade_url_copied)))
    return active_accounts

#%%
def launch_steam_and_login(username, password, steam_path = os.path.join('C:\\', 'Program Files (x86)', 'Steam', 'Steam.exe')):
    if steam_path == None:
        raise Exception("Steam path not given.")
    if not steam_path.endswith('Steam.exe'):
        raise Exception("Steam path Invalid.")
    if not os.path.isfile(steam_path):
        raise Exception("Steam path not found.")
    
    proc = subprocess.Popen(steam_path + " -login %s %s"%(str(username), str(password)))
    return proc

#%%
def get_account_database(account_sheet_path = cfg.PATH_TO_ACCOUNT_SHEET):
    data = pd.read_excel(account_sheet_path)
    print("Found a database of %d accounts"%(len(data)))
    steamIDs = data['SteamID']
    usernames = data['Username']
    passwords = data['Password']
    email_addresses = data['Email_Address']
    email_passwords = data['Email_Password']
    domain = data['Domain']
    data_dict = {}
    for i in range(len(usernames)):
        data_dict[usernames[i]] = {}
        data_dict[usernames[i]]['Password'] = passwords[i]
        data_dict[usernames[i]]['Email_Address'] = email_addresses[i]
        data_dict[usernames[i]]['Email_Password'] = email_passwords[i]
        data_dict[usernames[i]]['SteamID'] = steamIDs[i]
        data_dict[usernames[i]]['Steam64ID'] = Convert(str(steamIDs[i])).steam_id64_converter()
        data_dict[usernames[i]]['Domain'] = domain[i]
    return data_dict

#%%
def load_image_snippets():
    l = os.listdir('email_snippets')
    d = {}
    for i in l:
        image = np.load(os.path.join('email_snippets', i))
        d[i.split('.')[0]] = image
    print("Found %d Snippets"%(len(d)))
    return d

#%%
def cleaner():    
    # kill csgo processes
    os.system('taskkill /f /im csgo.exe /im steam.exe /im steamwebhelper.exe /im steamservice.exe /im steamerrorreporting.exe')
    
    # # kill steam processes
    # os.system('taskkill /f ')
    
    # # kill steamwebhelper processes
    # os.system('taskkill /f ')
    os.system('taskkill /f /im cmd.exe')
    
    #kill open cmd process
    os.system('taskkill /f /im cmd.exe')








#%% trade url [STAGE 3.5]
def copy_trade_url_from_page(username):
    count = 0
    status = False
    while count < cfg.max_trade_url_copy_attempts and not status:
        time.sleep(0.5)
        press_and_release('ctrl+a')
        time.sleep(0.35)
        press_and_release('ctrl+c')
        trade_url = pc.paste()
        pc.copy('')
        try:
            assert "steamcommunity.com" in trade_url
            file = open(os.path.join('account_trade_url', username + '.txt'), 'w')
            file.write(trade_url)
            file.close()
            status = True
        except:
            count += 1
    return status

def change_privacy_options_to_public():
    click_only(STEAM_PROFILE_PRIVACY_PAGE_BLANK_X, STEAM_PROFILE_PRIVACY_PAGE_BLANK_Y, 0.3, 1)
    hover_only(STEAM_PROFILE_PRIVACY_INVENTORY_X, STEAM_PROFILE_PRIVACY_INVENTORY_Y, 0.5, 0.5)
    click_only(None, None, 0.3, 1)
    hover_only(STEAM_PROFILE_PRIVACY_INVENTORY_DROP_DOWN_MENU_PUBLIC_X, STEAM_PROFILE_PRIVACY_INVENTORY_DROP_DOWN_MENU_PUBLIC_Y, 0.5, 0.5)
    click_only(None, None, 0.3, 1)
    click_only(STEAM_PROFILE_PRIVACY_PAGE_BLANK_X, STEAM_PROFILE_PRIVACY_PAGE_BLANK_Y, 0.3, 1)


#%% CONVERT
class Convert(object):
    """Class for converting SteamID between different versions of it"""

    def __init__(self, steamid):
        """Init"""
        self.sid = steamid
        self.change_val = 76561197960265728
        self.alert()

    def set_steam_id(self, steamid):
        """Sets new steam ID"""
        self.sid = steamid
        self.recognize_sid()
        self.alert()

    def get_steam_id(self):
        """Returns given Steam ID"""
        return self.sid

    def recognize_sid(self, choice=0):
        """Recognized inputted steamID
        SteamID code = 1
        SteamID3 code = 2
        SteamID32 code = 3
        SteamID64 code = 4
        Not found = 0
        Choice int 1 or 0
        1- prints recognized steam ID and returns code
        0- Returns only code"""
        if choice != 0 and choice != 1:
            print('Assuming choice is 1')
            choice = 1
        if self.sid[0] == 'S':  # SteamID
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID')
            return 1
        elif self.sid[0] in ['U', 'I', 'M', 'G', 'A', 'P', 'C', 'g', 'T', 'L', 'C', 'a']:  # SteamID3
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID3')
            return 2
        elif self.sid[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.sid) < 17:  # SteamID32
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID32')
            return 3
        elif self.sid[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(self.sid) == 17:  # SteamID64
            if choice == 1:
                print('Recognized ', self.sid, ' as SteamID64')
            return 4
        else:
            if choice == 1:
                print(self.sid, 'is not recognized as any SteamID')
            return 0

    def alert(self):
        """Prints alert when user tries to convert one of special accounts"""
        recognized = self.recognize_sid(0)
        if recognized == 1:
            if self.sid[6] != '0':
                print('Result of converting:', self.sid, 'steam ID may not be correct')
        elif recognized == 2:
            if self.sid[0] != 'U':
                print('Result of converting:', self.sid, 'steam ID may not be correct')

    def steam_id_converter(self):
        """Converts other SteamID versions to steamID"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Returns steamID
            return self.sid
        elif recognized == 2:  # Converts SteamID3 to SteamID
            steam3 = int(self.sid[4:])
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)
        elif recognized == 3:  # Converts SteamID32 to SteamID
            steam3 = int(self.sid)
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)
        elif recognized == 4:  # Converts SteamID64 SteamID64
            steam3 = int(self.steam_id32_converter())
            return 'STEAM_0:' + str(self.oddity(steam3)) + ':' + str(steam3 // 2)

    @staticmethod
    def oddity(number):
        """Checks oddity of given number"""
        if number % 2 == 0:
            return 0
        else:
            return 1

    def steam_id3_converter(self):
        """Converts other SteamID versions to SteamID3"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts SteamID to SteamID3
            return 'U:1:' + str(self.steam_id32_converter())
        elif recognized == 2:  # returns SteamID3
            return self.sid
        elif recognized == 3:  # Converts SteamID32 to SteamID3
            return 'U:1:' + str(self.sid)
        elif recognized == 4:  # Converts SteamID64 to SteamID3
            return 'U:1:' + str(int(self.sid) - self.change_val)

    def steam_id32_converter(self):
        """Converts other steamID versions to steamID32"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts from steamID to SteamID32
            y = self.sid[8:9]  # STEAM_0:y:zzzzzz
            z = self.sid[10:]  # STEAM_0:y:zzzzzz
            return int(z) * int(2) + int(y)
        elif recognized == 2:  # Converts from steamID3 to SteamID32
            return int(self.sid[4:])
        elif recognized == 3:  # Returns steamID32
            return int(self.sid)
        elif recognized == 4:  # Converts from steamID64 to SteamID32
            return int(self.sid) - self.change_val

    def steam_id64_converter(self):
        """Converts other SteamID versions to SteamID64"""
        recognized = self.recognize_sid(0)
        if recognized == 1:  # Converts from steamID to SteamID64
            y = self.sid[8:9]  # STEAM_0:y:zzzzzz
            z = self.sid[10:]  # STEAM_0:y:zzzzzz
            return int(z) * int(2) + int(y) + self.change_val
        elif recognized == 2:  # Converts steamID3 to SteamID64
            return int(self.sid[4:]) + self.change_val
        elif recognized == 3:  # Converts steamID32 to SteamID64
            return int(self.sid) + self.change_val
        elif recognized == 4:  # Returns steamID64
            return int(self.sid)

