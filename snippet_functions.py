from PIL import ImageGrab#, Image
# import cv2
import numpy as np
import time

from mouse_functions import click_only
from config import w, h, nearby_snippet_check_threshold
from helper_functions import change_privacy_options_to_public

#%% Haystack functions
def haystack_pixel_generator(x1, y1, x2, y2):
    return max(0, x1 - nearby_snippet_check_threshold), max(0, y1 - nearby_snippet_check_threshold), min(w, x2 + nearby_snippet_check_threshold), min(h, y2 + nearby_snippet_check_threshold)

def find_matches(haystack, needle):
    arr_h = np.array(np.asarray(haystack)[:, :, :3], 'uint8')
    arr_n = np.array(np.asarray(needle)[:, :, :3], 'uint8')

    y_h, x_h = arr_h.shape[:2]
    y_n, x_n = arr_n.shape[:2]

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1

    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            arr_t = (arr_s == arr_n)                # Create test matrix
            if arr_t.all():                         # Only consider exact matches
                matches = (xmin,ymin)
                return matches

#%% [Depracted[ [STAGE 1.1] Steam Client Confirmation after login
def confirm_steam_client_internal(steam_client):
    from positions import STEAM_CLIENT_X_1, STEAM_CLIENT_Y_1, \
        STEAM_CLIENT_X_2, STEAM_CLIENT_Y_2
    STEAM_CLIENT_X_1, STEAM_CLIENT_Y_1, STEAM_CLIENT_X_2, STEAM_CLIENT_Y_2 = haystack_pixel_generator(STEAM_CLIENT_X_1, 
                                                                                                      STEAM_CLIENT_Y_1, 
                                                                                                      STEAM_CLIENT_X_2, 
                                                                                                      STEAM_CLIENT_Y_2)
    image = ImageGrab.grab([STEAM_CLIENT_X_1, STEAM_CLIENT_Y_1, STEAM_CLIENT_X_2, STEAM_CLIENT_Y_2]).convert("RGB")
    output = find_matches(image, steam_client)
    if output == None:
        return False
    else:
        return output

def confirm_steam_client(snippets_dict):
    steam_client = snippets_dict['steam_client']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_steam_client_internal(steam_client)
        if output != False:
            return output
    return False

#%% [Depracted] [STAGE 1.1] Confirm Steam Email Guard Login Page
# steam_login_email_auth_confirm = snippets_dict['steam_login_email_auth_confirm']
def confirm_steam_client_email_auth_internal(steam_login_email_auth_confirm):
    from positions import STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_1, \
        STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_1, \
            STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_2, \
                STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_2
    STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_1, STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_1, \
        STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_2, STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_2 = \
            haystack_pixel_generator(STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_1, STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_1,
                                     STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_2, STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_2)
    image = ImageGrab.grab([STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_1, 
                            STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_1, 
                            STEAM_LOGIN_EMAIL_AUTH_CONFIRM_X_2, 
                            STEAM_LOGIN_EMAIL_AUTH_CONFIRM_Y_2]).convert("RGB")
    output = find_matches(image, steam_login_email_auth_confirm)
    if output == None:
        return False
    else:
        return output

def confirm_steam_client_email_auth(snippets_dict):
    steam_login_email_auth_confirm = snippets_dict['steam_login_email_auth_confirm']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_steam_client_email_auth_internal(steam_login_email_auth_confirm)
        if output != False:
            return output
    return False

#%% [STAGE 1.1] Confirm whether logged in successful or email guard is needed
def confirm_client_or_guard_auth(snippets_dict):
    steam_login_email_auth_confirm = snippets_dict['steam_login_email_auth_confirm']
    steam_client = snippets_dict['steam_client']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_client = confirm_steam_client_internal(steam_client)
        if output_client != False:
            return ("Logged in", output_client)
        output_email_auth = confirm_steam_client_email_auth_internal(steam_login_email_auth_confirm)
        if output_email_auth != False:
            return ("Guard Login", output_email_auth)
    return False

#%% [STAGE 1.2] Confirm Steam Email Guard Page After clicking Next
def confirm_steam_client_after_clicking_next_internal(steam_client_after_clicking_next):
    from positions import STEAM_LOGIN_EMAIL_AFTER_NEXT_X_1, STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_1, \
        STEAM_LOGIN_EMAIL_AFTER_NEXT_X_2, STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_2
    STEAM_LOGIN_EMAIL_AFTER_NEXT_X_1, STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_1, \
        STEAM_LOGIN_EMAIL_AFTER_NEXT_X_2, STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_2 = \
            haystack_pixel_generator(STEAM_LOGIN_EMAIL_AFTER_NEXT_X_1, 
                                     STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_1, 
                                     STEAM_LOGIN_EMAIL_AFTER_NEXT_X_2, 
                                     STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_2)
    image = ImageGrab.grab([STEAM_LOGIN_EMAIL_AFTER_NEXT_X_1, 
                            STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_1, 
                            STEAM_LOGIN_EMAIL_AFTER_NEXT_X_2, 
                            STEAM_LOGIN_EMAIL_AFTER_NEXT_Y_2]).convert("RGB")
    output = find_matches(image, steam_client_after_clicking_next)
    if output == None:
        return False
    else:
        return output

def confirm_steam_client_after_clicking_next(snippets_dict):
    steam_client_after_clicking_next = snippets_dict['steam_client_after_clicking_next']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_after_clicking_next = confirm_steam_client_after_clicking_next_internal(steam_client_after_clicking_next)
        if output_after_clicking_next != False:
            return output_after_clicking_next
    return False

#%% [STAGE 1.4] Confirm Steam guard success Page after entering code
def confirm_steam_client_auth_success_internal(steam_client_auth_success):
    from positions import STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_1, STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_1, \
        STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_2, STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_2 
    STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_1, STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_1, \
        STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_2, STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_2 = \
            haystack_pixel_generator(STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_1, 
                                     STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_1, 
                                     STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_2, 
                                     STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_2)
    image = ImageGrab.grab([STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_1, 
                            STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_1, 
                            STEAM_LOGIN_EMAIL_AUTH_SUCCESS_X_2, 
                            STEAM_LOGIN_EMAIL_AUTH_SUCCESS_Y_2]).convert("RGB")
    output = find_matches(image, steam_client_auth_success)
    if output == None:
        return False
    else:
        return output

def confirm_steam_client_auth_success(snippets_dict):
    steam_client_auth_success = snippets_dict['steam_client_auth_success']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_auth_success = confirm_steam_client_auth_success_internal(steam_client_auth_success)
        if output_auth_success != False:
            return output_auth_success
    return False

#%% [STAGE 2.1] PART 1 Confirm Steam Profile Page
def confirm_steam_profile_page_setup_welcome_page_internal(steam_profile_setup_page):
    from positions import STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_1, STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_1, \
        STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_2, STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_2
    STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_1, STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_1, \
        STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_2, STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_1, 
                                     STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_1, 
                                     STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_2, 
                                     STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_1, 
                            STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_1, 
                            STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_X_2, 
                            STEAM_PROFILE_PAGE_SETUP_WELCOME_PAGE_Y_2])
    output = find_matches(image, steam_profile_setup_page)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_page_setup_welcome_page(snippets_dict):
    steam_profile_setup_page = snippets_dict['steam_profile_setup_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_setup = confirm_steam_profile_page_setup_welcome_page_internal(steam_profile_setup_page)
        if output_profile_setup != False:
            return output_profile_setup
    return False

#%% [STAGE 2.1] PART 2 Confirm Steam Profile Page confirmed
def confirm_steam_profile_page_internal(steam_profile_page):
    from positions import STEAM_PROFILE_PAGE_X_1, STEAM_PROFILE_PAGE_Y_1, \
        STEAM_PROFILE_PAGE_X_2, STEAM_PROFILE_PAGE_Y_2
    STEAM_PROFILE_PAGE_X_1, STEAM_PROFILE_PAGE_Y_1, \
        STEAM_PROFILE_PAGE_X_2, STEAM_PROFILE_PAGE_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_PAGE_X_1, 
                                     STEAM_PROFILE_PAGE_Y_1, 
                                     STEAM_PROFILE_PAGE_X_2, 
                                     STEAM_PROFILE_PAGE_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_PAGE_X_1, STEAM_PROFILE_PAGE_Y_1, 
                            STEAM_PROFILE_PAGE_X_2, STEAM_PROFILE_PAGE_Y_2])
    output = find_matches(image, steam_profile_page)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_page(snippets_dict):
    steam_profile_page = snippets_dict['steam_profile_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_page = confirm_steam_profile_page_internal(steam_profile_page)
        if output_profile_page != False:
            return output_profile_page
    return False

#%% [STAGE 2.1] FINAL 
def confirm_steam_profile_page_or_steam_profile_setup(snippets_dict):
    steam_profile_page = snippets_dict['steam_profile_page']
    steam_profile_setup_page = snippets_dict['steam_profile_setup_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_page = confirm_steam_profile_page_internal(steam_profile_page)
        if output_profile_page != False:
            return ("Steam Profile Page", output_profile_page)
        output_profile_setup = confirm_steam_profile_page_setup_welcome_page_internal(steam_profile_setup_page)
        if output_profile_setup != False:
            return ("Steam Profile Setup", output_profile_setup)
    return False

#%% [STAGE 2.2] Confirm steam profile settings page.

def confirm_steam_profile_settings_page_internal(steam_profile_settings_page):
    from positions import STEAM_PROFILE_SETTINGS_PAGE_X_1, STEAM_PROFILE_SETTINGS_PAGE_Y_1, \
        STEAM_PROFILE_SETTINGS_PAGE_X_2, STEAM_PROFILE_SETTINGS_PAGE_Y_2
    STEAM_PROFILE_SETTINGS_PAGE_X_1, STEAM_PROFILE_SETTINGS_PAGE_Y_1, \
        STEAM_PROFILE_SETTINGS_PAGE_X_2, STEAM_PROFILE_SETTINGS_PAGE_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_SETTINGS_PAGE_X_1, 
                                     STEAM_PROFILE_SETTINGS_PAGE_Y_1, 
                                     STEAM_PROFILE_SETTINGS_PAGE_X_2, 
                                     STEAM_PROFILE_SETTINGS_PAGE_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_SETTINGS_PAGE_X_1, 
                            STEAM_PROFILE_SETTINGS_PAGE_Y_1, 
                            STEAM_PROFILE_SETTINGS_PAGE_X_2, 
                            STEAM_PROFILE_SETTINGS_PAGE_Y_2])
    output = find_matches(image, steam_profile_settings_page)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_settings_page(snippets_dict):
    steam_profile_settings_page = snippets_dict['steam_profile_settings_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_settings_page = confirm_steam_profile_settings_page_internal(steam_profile_settings_page)
        if output_profile_settings_page != False:
            return output_profile_settings_page
    return False

#%% [STAGE 3.1]
def confirm_steam_profile_inventory_button_internal(steam_profile_inventory_option):
    from positions import STEAM_PROFILE_INVENTORY_OPTION_X_1, STEAM_PROFILE_INVENTORY_OPTION_Y_1, \
        STEAM_PROFILE_INVENTORY_OPTION_X_2, STEAM_PROFILE_INVENTORY_OPTION_Y_2
    STEAM_PROFILE_INVENTORY_OPTION_X_1, STEAM_PROFILE_INVENTORY_OPTION_Y_1, \
        STEAM_PROFILE_INVENTORY_OPTION_X_2, STEAM_PROFILE_INVENTORY_OPTION_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_INVENTORY_OPTION_X_1, 
                                     STEAM_PROFILE_INVENTORY_OPTION_Y_1, 
                                     STEAM_PROFILE_INVENTORY_OPTION_X_2, 
                                     STEAM_PROFILE_INVENTORY_OPTION_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_INVENTORY_OPTION_X_1, 
                            STEAM_PROFILE_INVENTORY_OPTION_Y_1, 
                            STEAM_PROFILE_INVENTORY_OPTION_X_2, 
                            STEAM_PROFILE_INVENTORY_OPTION_Y_2])
    output = find_matches(image, steam_profile_inventory_option)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_inventory_button(snippets_dict):
    steam_profile_inventory_option = snippets_dict['steam_profile_inventory_option']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_inventory_option = confirm_steam_profile_inventory_button_internal(steam_profile_inventory_option)
        if output_profile_inventory_option != False:
            return output_profile_inventory_option
    return False

#%% [STAGE 3.2]
def confirm_steam_profile_inventory_page_internal(steam_profile_inventory_page):
    from positions import STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_1, STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_1, \
        STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_2, STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_2
    STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_1, STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_1, \
        STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_2, STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_2 = \
            haystack_pixel_generator(STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_1, 
                                     STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_1, 
                                     STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_2, 
                                     STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_2)
    image = ImageGrab.grab([STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_1, 
                            STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_1, 
                            STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_X_2, 
                            STEAM_CLIENT_INVENTORY_PAGE_CONFIRM_Y_2])
    output = find_matches(image, steam_profile_inventory_page)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_inventory_page(snippets_dict):
    steam_profile_inventory_page = snippets_dict['steam_profile_inventory_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_inventory_page = confirm_steam_profile_inventory_page_internal(steam_profile_inventory_page)
        if output_profile_inventory_page != False:
            return output_profile_inventory_page
    return False


#%% [STAGE 3.3] 
def confirm_steam_profile_trade_offer_who_can_send_button_internal(steam_profile_trade_offer_page):
    from positions import STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_1, STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_1, \
        STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_2, STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_2
    STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_1, STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_1, \
        STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_2, STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_1, 
                                     STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_1, 
                                     STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_2, 
                                     STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_1, 
                            STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_1, 
                            STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_X_2, 
                            STEAM_PROFILE_TRADE_OFFER_WHO_CAN_SEND_Y_2])
    output = find_matches(image, steam_profile_trade_offer_page)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_trade_offer_who_can_send_button(snippets_dict):
    steam_profile_trade_offer_page = snippets_dict['steam_profile_trade_offer_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_profile_trade_offer_page = confirm_steam_profile_trade_offer_who_can_send_button_internal(steam_profile_trade_offer_page)
        if output_profile_trade_offer_page != False:
            return output_profile_trade_offer_page
    return False

#%% [STAGE 3.4]
def confirm_steam_who_can_send_me_trade_offer_page_internal(steam_who_can_send_me_trade_offer_page):
    from positions import STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_1, STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_1, \
        STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_2, STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_2
    STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_1, STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_1, \
        STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_2, STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_2 = \
            haystack_pixel_generator(STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_1, 
                                     STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_1, 
                                     STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_2, 
                                     STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_2)
    image = ImageGrab.grab([STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_1, 
                            STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_1, 
                            STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_X_2, 
                            STEAM_WHO_CAN_SEND_ME_TRADE_OFFER_Y_2])
    output = find_matches(image, steam_who_can_send_me_trade_offer_page)
    if output == None:
        return False
    else:
        return output

def confirm_steam_who_can_send_me_trade_offer_page(snippets_dict):
    steam_who_can_send_me_trade_offer_page = snippets_dict['steam_who_can_send_me_trade_offer_page']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_who_can_send_me_TO = confirm_steam_who_can_send_me_trade_offer_page_internal(steam_who_can_send_me_trade_offer_page)
        if output_who_can_send_me_TO != False:
            return output_who_can_send_me_TO
    return False

#%% [STAGE 4.3I] # TODO WIP
def confirm_steam_profile_privacy_options_friends_only_internal(steam_profile_privacy_options_friends_only):
    from positions import STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, \
        STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2
    STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, \
        STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, 
                                     STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, 
                                     STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, 
                                     STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, 
                            STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, 
                            STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, 
                            STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2])
    output = find_matches(image, steam_profile_privacy_options_friends_only)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_privacy_options_friends_only(snippets_dict):
    steam_profile_privacy_options_friends_only = snippets_dict['steam_profile_privacy_options_friends_only']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_privacy_page_friends_only = confirm_steam_profile_privacy_options_friends_only_internal(steam_profile_privacy_options_friends_only)
        if output_privacy_page_friends_only != False:
            return output_privacy_page_friends_only
    return False

#%% [STAGE 4.3I] # TODO WIP
def confirm_steam_profile_privacy_options_public_internal(steam_profile_privacy_options_public):
    from positions import STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, \
        STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2
    STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, \
        STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2 = \
            haystack_pixel_generator(STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, 
                                     STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, 
                                     STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, 
                                     STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2)
    image = ImageGrab.grab([STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_1, 
                            STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_1, 
                            STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_X_2, 
                            STEAM_PROFILE_PRIVACY_PAGE_INVENTORY_CHANGE_Y_2])
    output = find_matches(image, steam_profile_privacy_options_public)
    if output == None:
        return False
    else:
        return output

def confirm_steam_profile_privacy_options_public(snippets_dict):
    steam_profile_privacy_options_public = snippets_dict['steam_profile_privacy_options_public']
    for i in range(30):
        time.sleep(1)
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output_privacy_page_friends_only = confirm_steam_profile_privacy_options_public_internal(steam_profile_privacy_options_public)
        if output_privacy_page_friends_only != False:
            return output_privacy_page_friends_only
    return False

#%% [STAGE 4.3] combines privacy options friends only and public [Internal]
def confirm_steam_profile_privacy_setting_internal(snippets_dict):
    steam_profile_privacy_options_public = snippets_dict['steam_profile_privacy_options_public']
    steam_profile_privacy_options_friends_only = snippets_dict['steam_profile_privacy_options_friends_only']
    output = confirm_steam_profile_privacy_options_public_internal(steam_profile_privacy_options_public)
    if output != False:
        return ("Public", output)
    output = confirm_steam_profile_privacy_options_friends_only_internal(steam_profile_privacy_options_friends_only)
    if output != False:
        return ("Friends Only", output)
    return False

def confirm_steam_profile_privacy_setting(snippets_dict):
    for i in range(30):
        if i%5 == 0: click_only(1500, 1060, 0.1, 1)
        output = confirm_steam_profile_privacy_setting_internal(snippets_dict)
        if output != False:
            return output
    return False

#%%  [STAGE 4.4]
def confirm_and_change_privacy_options_to_public(snippets_dict):
    exit_count = 10
    count = 0
    while count < exit_count:
        output = confirm_steam_profile_privacy_setting_internal(snippets_dict)
        if output == False:
            continue
        else:
            if output[0] == "Public":
                print("Found Settings as Public")
                return True
            elif output[0] == "Friends Only":
                print("Found Settings as Friends Only: Changing to Public.")
                change_privacy_options_to_public()
        time.sleep(2)
    return False