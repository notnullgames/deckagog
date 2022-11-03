import webview
import requests
import os
import time
import urllib
import json

cacheFile = os.path.expanduser('~/.deckagog.json')
class Cache(object):
  def __init__(self):
    try:
      f = open(cacheFile, "r")
      self.__dict__.update(json.loads(f.read()))
      f.close()
    except:
      pass

  def __getitem__(self, key):
    return self.__dict__[key]

  def __setitem__(self, key, value):
    print(f'save {key}:{value}')
    self.__dict__[key] = value
    f = open(cacheFile, "w")
    f.write(json.dumps(self.__dict__))
    f.close()

  def __delitem__(self, key):
    del self.__dict__[key]
    f = open(cacheFile, "w")
    f.write(json.dumps(self.__dict__))
    f.close()

  def __contains__(self, key):
    return key in self.__dict__

  def __len__(self):
    return len(self.__dict__)

  def __repr__(self):
    return repr(self.__dict__)

cache = Cache()

content_url = 'dist/index.html'
if os.environ.get('DECKAGOG_MODE') == 'dev':
  content_url = 'http://localhost:5173/'

debug = os.environ.get('DECKAGOG_MODE') == 'dev'

def _on_loaded_auth_check():
  print('_on_loaded_auth_check')
  u = window.get_current_url()
  if u.startswith('https://embed.gog.com/on_login_success'):
    window.events.loaded -= _on_loaded_auth_check
    u = urllib.parse.urlparse(u)
    code = dict(urllib.parse.parse_qsl(u.query))['code']
    s = urllib.parse.urlencode({
      'client_id': '46899977096215655',
      'client_secret': '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9',
      'redirect_uri': 'https://embed.gog.com/on_login_success?origin=client',
      'grant_type': 'authorization_code',
      'code': code
    })
    cache['auth'] = requests.get(f'https://auth.gog.com/token?{s}').json()
    window.load_url(content_url)
    


def token():
  print('token')
  try:
    if cache['auth']['expires'] > time.time():
      print('cache hit, within time, returning access')
      return cache['auth']['access_token']
    else:
      print('cache hit, not within time, refreshing')
      s = urllib.parse.urlencode({
        'client_id': '46899977096215655',
        'client_secret': '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9',
        'redirect_uri': 'https://embed.gog.com/on_login_success?origin=client',
        'grant_type': 'refresh_token',
        'refresh_token': cache['auth']['refresh_token']
      })
      a = requests.get(f'https://auth.gog.com/token?{s}').json()
      a['expires'] = a['expires_in'] + int(time.time())
      cache['auth'] = a
      print('cache hit, refreshed')
      return cache['auth']['access_token']
  except Exception as e:
    print(e)
    cache['auth'] = {}
    # if any of the keys are missing start at beginning of login flow
    window.load_url('https://auth.gog.com/auth?client_id=46899977096215655&redirect_uri=https%3A%2F%2Fembed.gog.com%2Fon_login_success%3Forigin%3Dclient&response_type=code&layout=client2')
    window.evaluate_js("document.body.style.backgroundColor='black'")
    print('wating for login')
    window.events.loaded += _on_loaded_auth_check
    while True:
      print('looping')
      try:
        if cache['auth']['expires']:
          print('found auth')
          return cache['auth']['access_token']
      except:
        pass
      time.sleep(0.5)


def get_games():
  t = token()
  return requests.get('https://embed.gog.com/user/data/games', headers = { 'Authorization': f'Bearer {t}' }).json()

def details(id):
  try:
    return cache[id]
  except:
    t = token()
    cache[id] = requests.get(f'https://embed.gog.com/account/gameDetails/{id}.json', headers = { 'Authorization': f'Bearer {t}' }).json()
    return cache[id]

def download(id, files, outDir):
  t = token()
  game = details(id)


class JsAPI:
  def get_games(self):
    return get_games()

  def download(self, id):
    game = details(id)
    outDir = create_file_dialog(webview.FOLDER_DIALOG)
    # TODO: filter patches
    games = []
    download(id, games, outDir)
    return {
      'games': games,
      'outDir': outDir,
      'data': game
    }

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

