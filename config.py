#### SETTINGS FOR the script
import os


steam_path = os.path.join('C:\\', 'Program Files (x86)', 'Steam', 'Steam.exe')


# Threshold value to consider for checking data around.
nearby_snippet_check_threshold = 100

# Max login attempts
max_login_attempts = 3

after_login_email_wait = 15

# Windows resolution
w, h = 1920, 1080

# Get Steam profile ready
get_steam_profile_ready = True

# Change Profile Privacy
change_profile_privacy = True

# Get Steam Trade URL
get_steam_trade_url = True

# Login Code attempts
max_fetch_login_code_attempts = 6

# Trade URL Copy attempts
max_trade_url_copy_attempts = 5

#%%
PATH_TO_ACCOUNT_SHEET = os.path.join('data', 'account_sheet.xlsx')
PATH_TO_ACTIVE_ACCOUNTS = os.path.join('data', 'active_usernames.xlsx')
