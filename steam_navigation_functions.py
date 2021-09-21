import os

def open_steam_profile_page(steam64id):
    url = "steam://openurl/https://steamcommunity.com/profiles/%s/"%(str(steam64id))
    os.startfile(url)

def open_steam_profile_settings_page(steam64id):
    url = "steam://openurl/https://steamcommunity.com/profiles/%s/edit/info/"%(str(steam64id))
    os.startfile(url)

def open_who_can_send_me_offers_page(steam64id):
    url = "steam://openurl/https://steamcommunity.com/profiles/%s/tradeoffers/privacy/"%(str(steam64id))
    os.startfile(url)

def open_steam_profile_privacy_options_page(steam64id):
    url = "steam://openurl/https://steamcommunity.com/profiles/%s/edit/settings/"%(str(steam64id))
    os.startfile(url)