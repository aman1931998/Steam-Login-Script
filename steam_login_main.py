import time

from config import steam_path, max_fetch_login_code_attempts, get_steam_profile_ready, change_profile_privacy, get_steam_trade_url, max_login_attempts, after_login_email_wait
from helper_functions import get_account_database, get_active_accounts, load_image_snippets, cleaner, launch_steam_and_login, \
    add_account_to_accounts_with_error, save_account_completion_timestamp, add_account_to_accounts_logged_in, add_list_of_accounts_profile_setup_done, \
        copy_trade_url_from_page, add_list_of_accounts_trade_url_copied, add_list_of_accounts_profile_privacy_changed, get_active_usernames
from email_functions import establish_connection_to_mailserver, imap_login_into_mail, get_steam_code_from_mail
from snippet_functions import confirm_client_or_guard_auth, confirm_steam_client_after_clicking_next, confirm_steam_client_auth_success, \
    confirm_steam_client, confirm_steam_profile_page_or_steam_profile_setup, confirm_steam_profile_page, confirm_steam_profile_settings_page, \
        confirm_steam_who_can_send_me_trade_offer_page, confirm_steam_profile_privacy_setting, confirm_and_change_privacy_options_to_public
from positions import STEAM_LOGIN_EMAIL_AUTH_NEXT_BUTTON_X, STEAM_LOGIN_EMAIL_AUTH_NEXT_BUTTON_Y, \
    STEAM_ENTER_EMAIL_GUARD_CODE_X, STEAM_ENTER_EMAIL_GUARD_CODE_Y, \
        STEAM_LOGIN_EMAIL_AUTH_FINISH_BUTTON_X, STEAM_LOGIN_EMAIL_AUTH_FINISH_BUTTON_Y, \
            STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X, STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y, \
                STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_1, STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_1
from steam_navigation_functions import open_steam_profile_page, open_who_can_send_me_offers_page, open_steam_profile_privacy_options_page

from mouse_functions import click_only, write_and_execute, hover_only

#%%
# get account database
account_data = get_account_database()
account_usernames = get_active_usernames() #list(account_data.keys()) ## TODO change function to pick accounts
print("Current session as %d Accounts to cover"%(len(account_usernames)))
# get list of accounts
# USER_INPUT
print("Loading the Remaining accounts...")
active_accounts = get_active_accounts()   #load_list_of_accounts_with_error

# Loading all snippets
print("Loading all image snippets...")
snippets_dict = load_image_snippets()

# Cleaner
cleaner()

account_usernames = [username for username in account_usernames if not \
                         (username in active_accounts['Logged In'] \
                          and username in active_accounts['Privacy Changed'] \
                              and username in active_accounts['Profile Setup Done'] \
                                  and username in active_accounts['Trade URL Copied'])
                             ]
print("%d Accounts to cover: "%(len(account_usernames)))
time.sleep(2)
#%% i += 1
for username in account_usernames: # username = account_usernames[0]
    # Additional check if account is done or not
    if username in active_accounts['Logged In'] and username in active_accounts['Privacy Changed'] and \
        username in active_accounts['Profile Setup Done'] and username in active_accounts['Trade URL Copied']:
        print("Username: %s Done. Skipping..."%(username))
        continue
    # else:
    #     raise Exception()
    if username not in account_data.keys():
        print("Username %s not found in database"%(username))
        continue

    password = account_data[username]['Password']
    email_address = account_data[username]['Email_Address']
    email_password = account_data[username]['Email_Password']
    steamID = account_data[username]['SteamID']
    steam64ID = account_data[username]['Steam64ID']
    domain = account_data[username]['Domain']
    print("Current Account name: %s\nPassword: %s\nEmail Address: %s\nEmail Password: %s"%(username, password, email_address, email_password))
    
    #%% [STAGE 1.1] Launching steam
    confirmation = False
    count = 0
    while count < max_login_attempts and not confirmation:
        print("LOGIN ATTEMPT: %d"%(count + 1))
        count += 1
        # cleaner
        print("Cleaning old instances...")
        cleaner()
        
        print("Launching Steam...")
        proc = launch_steam_and_login(username, password, steam_path)
    
        # Confirming launch of steam client or asking steam code.
        output__ = confirm_client_or_guard_auth(snippets_dict)
        if output__ == False: #Case 1: neither login nor email: Error
            add_account_to_accounts_with_error(username, "confirm_steam_launch")
            print("[STAGE 1.1] Error while logging in account %s."%(username))
            proc.kill()
            continue
        
        assert len(output__) == 2
        if output__[0] == 'Guard Login': #Case 2: Email Guard Login
            if username in active_accounts['Logged In']:
                print("Found Account in Logged in database....")
            print("Guard Login Detected.")
            # Clicking on Next button of guard login
            click_only(STEAM_LOGIN_EMAIL_AUTH_NEXT_BUTTON_X, 
                       STEAM_LOGIN_EMAIL_AUTH_NEXT_BUTTON_Y, 0.3, 3)
    
            #%% [STAGE 1.2] Verifying next button pressed or not.
            output = confirm_steam_client_after_clicking_next(snippets_dict)
            if output == False:
                add_account_to_accounts_with_error()
                print("[STAGE 1.2] Error while confirming Guard Page After clicking Next")
                proc.kill()
                continue
        
            #%% [STAGE 1.3] Getting Steam guard code
            print("Waiting %d seconds for guard code to arrive."%(after_login_email_wait))
            time.sleep(after_login_email_wait)
            
            print("Establishing connection to the mail server: %s"%(domain))
            try:
                imap = establish_connection_to_mailserver(domain)
            except Exception as e:
                print(e)
                add_account_to_accounts_with_error(username, "mail_server_connection")
                print("[STAGE 1.3] Error while generating connection to mail server.")
                proc.kill()
                continue
                
            print("Logging in using Email address: %s and Email Password: %s"%(email_address, email_password))
            try:
                imap = imap_login_into_mail(imap, email_address, email_password)
            except Exception as e:
                print(e)
                add_account_to_accounts_with_error(username, "email_login")
                print("[STAGE 1.3] Error while logging in to the mail server.")
                proc.kill()
                continue
        
            guard_code = None
            for i in range(max_fetch_login_code_attempts):
                try:
                    guard_code = get_steam_code_from_mail(imap)
                except:
                    print("Error while trying to fetch login code.")
                if len(guard_code) == 5:
                    print("Found Guard Code: %s"%(guard_code))
                    break
                print("Unable to fetch Code.")
                time.sleep(5)
            if len(guard_code) != 5:
                add_account_to_accounts_with_error(username, "guard_code")
                print("[STAGE 1.3] Error while getting steam login code. Ignoring account.")
                proc.kill()
                continue
            
            #%% [STAGE 1.4] Entering steam guard code
            print("Entering guard code: %s into steam client."%(guard_code))
            click_only(STEAM_ENTER_EMAIL_GUARD_CODE_X, STEAM_ENTER_EMAIL_GUARD_CODE_Y, 0.3, 3)
            time.sleep(0.5)
            write_and_execute(guard_code)
            
            # Verifying success or not
            output = confirm_steam_client_auth_success(snippets_dict)
            if output == False:
                add_account_to_accounts_with_error(username, "steam_guard_auth_success")
                print("[STAGE 1.4] Error while logging in account %s."%(username))
                proc.kill()
                continue
            
            click_only(STEAM_LOGIN_EMAIL_AUTH_FINISH_BUTTON_X, 
                       STEAM_LOGIN_EMAIL_AUTH_FINISH_BUTTON_Y, 0.3, 4)
            
            output = confirm_steam_client(snippets_dict)
            if output == False:
                add_account_to_accounts_with_error(username, "steam_guard_success_client_failed")
                print("[STAGE 1.5] Error while confirming Steam Client after successful email guard login.")
                proc.kill()
                continue
            
            #%% Adding Timestamp for the account
            print("Adding Timestamp for Successful login for username %s"%(username))
            print("Username %s: Steam Guard Login Done."%(username))
            save_account_completion_timestamp(username)
            if username not in active_accounts["Logged In"]: active_accounts["Logged In"].append(username)
            add_account_to_accounts_logged_in(username)
    
        elif output__[0] == 'Logged in':
            add_account_to_accounts_logged_in(username)
            print("Steam Launch Confirmed")
            if username not in active_accounts["Logged In"]: active_accounts["Logged In"].append(username)
        confirmation = True
    
    #%% [STAGE 2] Setting profile.
    if username not in active_accounts['Profile Setup Done'] and get_steam_profile_ready:
        #%% [STAGE 2.1] Opening Steam Profile Page
        print("Loading Steam Profile Page")
        open_steam_profile_page(steam64ID)
        print("Confirming Steam Profile Page")
        ### CHANGE THIS FUNCTION TO MULTI CHECK
        output_ = confirm_steam_profile_page_or_steam_profile_setup(snippets_dict)
        if output_ == False:
            add_account_to_accounts_with_error(username, "steam_profile_page_or_setup")
            print("[STAGE 2.1] Error while confirming Steam profile page or Steam profile setup page.")
            proc.kill()
            continue

        assert len(output_) == 2
        if output_[0] == "Steam Profile Setup":
            if username in active_accounts['Profile Setup Done']:
                print("Found Account in Profile Setup Done database....")
            print("Steam Profile Welcome Page confirmed")
            time.sleep(2)
            print("Setting up steam account.")
            #%% [STAGE 2.2] Opening Steam profile settings page
            print("Opening Steam Profile Settings page")
            click_only(STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_1 + 50, 
                       STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_1 + 10, 0.3, 3)
            # open_steam_profile_settings_page(steam64ID)
            print("Confirming Steam Profile settings page.")
            output = confirm_steam_profile_settings_page(snippets_dict)
            if output == False:
                add_account_to_accounts_with_error(username, "steam_profile_settings_page")
                print("[STAGE 2.2] Error while confirming Steam Profile Settings Page.")
                proc.kill()
                continue
            time.sleep(2)
            print("Opening Steam Profile Page again.")
            open_steam_profile_page(steam64ID)
            output = confirm_steam_profile_page(snippets_dict)
            if output == False:
                add_account_to_accounts_with_error(username, "steam_profile_page_after_setup")
                print("[STAGE 2.1X] Error while confirming Steam Profile Page after setup is completed.")
                proc.kill()
                continue
            print("Username %s: Profile Setup Done"%(username))
            if username not in active_accounts['Profile Setup Done']: active_accounts['Profile Setup Done'].append(username)
            add_list_of_accounts_profile_setup_done(username)
            
        if output_[0] == 'Steam Profile Page':
            add_list_of_accounts_profile_setup_done(username)
            print("Steam Profile Setup is Already done.")
            if username not in active_accounts['Profile Setup Done']: active_accounts['Profile Setup Done'].append(username)
    else:
        add_list_of_accounts_profile_setup_done(username)
        print("Username %s: Profile Setup already Marked DONE.")
        if username not in active_accounts['Profile Setup Done']: active_accounts['Profile Setup Done'].append(username)

    #%% [STAGE 3] Copying Trade URLs
    if username not in active_accounts['Trade URL Copied'] and get_steam_trade_url:
        print("Getting Trade URL for account.")
        print("Opening Who can send me trade offers page.")
        open_who_can_send_me_offers_page(steam64ID)
        print("Confirming who can send me trade offers page.")
        output = confirm_steam_who_can_send_me_trade_offer_page(snippets_dict)
        if output == False:
            add_account_to_accounts_with_error(username, "who_can_send_me_trade_offers")
            print("[STAGE 3.4] Error while confirming who can send me trade offers page.")
            proc.kill()
            continue
        print("Who can send me trade offers page confirmed.")
        print("Clicking on Trade URL.")
        hover_only(STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X, STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y, 0.5, 0.5)
        click_only(None, None, 0.1, 1)
        print("Copying the trade URL")
        output = copy_trade_url_from_page(username)
        if output:
            print("Username %s: Trade URL Copied."%(username))
            add_list_of_accounts_trade_url_copied(username)
            if username not in active_accounts['Trade URL Copied']: active_accounts['Trade URL Copied'].append(username)
        else:
            add_account_to_accounts_with_error(username, "trade_url_copied")
            print("[STAGE 3.5] Error while copying the Trade URL.")
            proc.kill()
            continue
    else:
        add_list_of_accounts_trade_url_copied(username)
        print("Username %s: TRADE URL COPIED already Marked DONE.")
        if username not in active_accounts['Trade URL Copied']: active_accounts['Trade URL Copied'].append(username)

    #%% [STAGE 4] Profile Privacy change
    if username not in active_accounts['Privacy Changed'] and change_profile_privacy:
        print("Opening Steam Profile Privacy Options.")
        open_steam_profile_privacy_options_page(steam64ID)
        print("Confirming Steam Profile Privacy Options page")
        output = confirm_steam_profile_privacy_setting(snippets_dict)
        if output == False:
            add_account_to_accounts_with_error(username, "profile_privacy_page")
            print('[STAGE 4.3] Error while confirming Profile Privacy Settings page.')
            proc.kill()
            continue
        print("Profile Privacy settings Page Confirmed.")
        print("Changing profile privacy options...")
        output = confirm_and_change_privacy_options_to_public(snippets_dict)
        if output == False:
            add_account_to_accounts_with_error(username, "privacy_options_change")
            print('[STAGE 4.4] Error while changing privacy options.')
            proc.kill()
            continue
        print("Username %s: Privacy Options changed."%(username))
        add_list_of_accounts_profile_privacy_changed(username)
        if username not in active_accounts['Privacy Changed']: active_accounts['Privacy Changed'].append(username)
        
    else:
        print("Username %s: Profile Privacy change Marked DONE.")
        add_list_of_accounts_profile_privacy_changed(username)
        if username not in active_accounts['Privacy Changed']: active_accounts['Privacy Changed'].append(username)
