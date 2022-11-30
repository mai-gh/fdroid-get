import requests
import sys
from time import sleep
from bs4 import BeautifulSoup

UA = 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'

app_list = [
  'org.fdroid.fdroid',
  'org.telegram.messenger',
  'com.ominous.quickweather',
  'com.aurora.store',
  'org.mozilla.fennec_fdroid',
  'com.menny.android.anysoftkeyboard',
  'com.kunzisoft.keepass.libre',
  'net.osmand.plus',
  'app.organicmaps',
  'de.reimardoeffinger.quickdic',
  'com.foobnix.pro.pdf.reader',
  'de.beowulf.libretranslater',
  'com.machiav3lli.backup', # Neo Backup
  'com.mitzuli',
  'org.videolan.vlc',
  'com.termux',
  'com.physphil.android.unitconverterultimate',
  'org.secuso.privacyfriendlynotes',
  'com.github.tmo1.sms_ie',

]


# get https://f-droid.org/repo/index-v2.json
# get https://f-droid.org/repo/index-v2.json.asc
# verify

import code
import gnupg
from pprint import pprint
from os.path import exists
from json import load as jsonload


# verify this against https://f-droid.org/docs/Release_Channels_and_Signing_Keys/
# F-Droid client app for Android -> official binary releases -> Primary key fingerprint
# gpg --recv-keys "37D2 C987 89D8 3119 4839 4E3E 41E7 044E 1DBA 2E89"
gpg = gnupg.GPG(gnupghome="/tmp")
import_result = gpg.recv_keys('hkps://keyserver.ubuntu.com', "37D2 C987 89D8 3119 4839 4E3E 41E7 044E 1DBA 2E89")

#pprint(vars(import_result))
#exit()

gpg.encoding = 'utf-8'

s = requests.Session()
s.headers.update({'User-Agent': UA})



def download(url):
  filename = url.split('/')[-1]
  if not exists(filename):
    print(f"downloading {filename}")
    r = s.get(url)
    with open(filename, "wb") as file:
      file.write(r.content)

download("https://f-droid.org/repo/index-v2.json")
download("https://f-droid.org/repo/index-v2.json.asc")
index_json_asc_stream = open('index-v2.json.asc', "rb")
verified = gpg.verify_file(index_json_asc_stream, 'index-v2.json')
if not verified: raise ValueError("Signature could not be verified!")

with open('index-v2.json', 'r') as file:
  index_json = jsonload(file)

#for key in index_json['packages']: print(f"{key} : {index_json['packages'][key]['metadata']['name']['en-US']}")

code.interact(local=locals())











#r = s.get('https://f-droid.org/repo/index-v2.json.asc')
#index_json_asc = r.content

#verified = gpg.verify(index_json)

#pprint(index_json)


#soup = BeautifulSoup(r.text, 'html.parser')
#buttons_list = soup.find_all(class_ = "download")
#for b in buttons_list:
#  first_link_code = b['onclick'].split("'")[1]
#  first_link = "http://filecrypt.co/Link/" + first_link_code + '.html'
#  first_link_resp = s.get(first_link)
#
#  if first_link_resp.status_code == 404:
#    print('ERROR 404: probably need to update User-Agent')
#    exit()
#
#  soup = BeautifulSoup(first_link_resp.text, 'html.parser')
#  second_link = soup.find("script").text.split("'")[1]
#  second_link_resp = s.get(second_link)
#  print(second_link_resp.url)
#  sleep(2)
