from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import requests
import json
import datetime

############################################
#             Account Data                 #
account = "your-Mail"
password = "your-Password"
clientname = 'anyname'
#                                          #
############################################

rooturl = "https://api.discovergy.com"
consumer_token_url = rooturl + "/public/v1/oauth1/consumer_token"
r = requests.post(url=consumer_token_url, data={'client': clientname})

consumer_token = r.json()

request_token_url = rooturl + "/public/v1/oauth1/request_token"
oauth = OAuth1Session(client_key=consumer_token["key"], client_secret=consumer_token['secret'], signature_method="HMAC-SHA1")
fetch_response = oauth.fetch_request_token(request_token_url)
oauth_token = fetch_response["oauth_token"]

oauth_verifier_url = rooturl + "/public/v1/oauth1/authorize?oauth_token=" + oauth_token + "&email=" + account + "&password=" + password

oauth_verifier = requests.get(oauth_verifier_url)
verifier = oauth_verifier.text[15:]

access_token_url = rooturl + "/public/v1/oauth1/access_token"
access_token = oauth.fetch_access_token(access_token_url,verifier=verifier)
meter_url = rooturl + "/public/v1/meters"
reading_root_url = rooturl + "/public/v1/readings"
meters = oauth.get(meter_url)
readingstime = round(datetime.datetime.now().timestamp() - 60) *1000

for meter in meters.json():
    meterid = meter["meterId"]
    serial = meter["serialNumber"]
    reading_url = reading_root_url + "?meterId=" + meterid + "&from=" + str(readingstime)
    reading = oauth.get(reading_url)
