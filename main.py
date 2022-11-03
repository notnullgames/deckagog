import webview
import requests
import os
import configparser
import time
import urllib

configFile = os.path.expanduser('~/.deckagog')
config = configparser.ConfigParser()
config.read(configFile)

content_url = 'dist/index.html'
if os.environ.get('DECKAGOG_MODE') == 'dev':
  content_url = 'http://localhost:5173/'

debug = os.environ.get('DECKAGOG_MODE') == 'dev'

def on_loaded_auth_check():
  u = window.get_current_url()
  if u.startswith('https://embed.gog.com/on_login_success'):
    window.events.loaded -= on_loaded_auth_check
    u = urllib.parse.urlparse(u)
    code = dict(urllib.parse.parse_qsl(u.query))['code']
    s = urllib.parse.urlencode({
      'client_id': '46899977096215655',
      'client_secret': '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9',
      'redirect_uri': 'https://embed.gog.com/on_login_success?origin=client',
      'grant_type': 'authorization_code',
      'code': code
    })
    auth = requests.get(f'https://auth.gog.com/token?{s}').json()
    config['auth'] = {
      'access_token': auth['access_token'],
      'refresh_token': auth['refresh_token'],
      'user_id': auth['user_id'],
      'expires': auth['expires_in'] + int(time.time())
    }
    with open(configFile, 'w') as f:
      config.write(f)

# trigger web login flow
def login():
  try:
    if config['auth']['expires'] > time.time():
      # if the key is set, but expiredd, do a refresh
      s = urllib.parse.urlencode({
        'client_id': '46899977096215655',
        'client_secret': '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9',
        'redirect_uri': 'https://embed.gog.com/on_login_success?origin=client',
        'grant_type': 'refresh_token',
        'refresh_token': config['auth']['refresh_token']
      })
      auth = requests.get(f'https://auth.gog.com/token?{s}').json()
      config['auth'] = {
        'access_token': auth['access_token'],
        'refresh_token': auth['refresh_token'],
        'user_id': auth['user_id'],
        'expires': auth['expires_in'] + int(time.time())
      }
      with open(configFile, 'w') as f:
        config.write(f)
    # if all is ok, but not expired, it's basically a noop here
  except:
    # if any of the keys are missing start at beginning of login flow
    window.load_url('https://auth.gog.com/auth?client_id=46899977096215655&redirect_uri=https%3A%2F%2Fembed.gog.com%2Fon_login_success%3Forigin%3Dclient&response_type=code&layout=client2')
    window.evaluate_js("document.body.style.backgroundColor='black'")
    window.events.loaded += on_loaded_auth_check


class JsAPI:
  def get_games(self):
    login()
    for id in requests.get('https://embed.gog.com/user/data/games', headers = { 'Authorization': f'Bearer {config['auth']['access_token']}' }).json():
      try:
        game = cache[id]
      except:
        cache[id]=requests.get(f'https://embed.gog.com/account/gameDetails/{id}.json', headers = { 'Authorization': f'Bearer {config['auth']['access_token']}' }).json()
        game = cache[id]

  def download(self, id):
    login()
    output=create_file_dialog(webview.FOLDER_DIALOG)
    print(f'download {id} {output}')

js_api = JsAPI()
window = webview.create_window(
  js_api=js_api,
  title='Deckagog',
  url=content_url,
  width=1280,
  height=800,
  fullscreen=(not debug)
)
webview.start(debug=debug)