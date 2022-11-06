import webview
import requests
import os
import time
import urllib
import json

# a disk-cache that acts like a dict
class Cache(object):
  def __init__(self, cacheFile):
    self.cacheFile = cacheFile
    try:
      f = open(cacheFile, "r")
      self.__dict__.update(json.loads(f.read()))
      f.close()
    except:
      pass

  def __getitem__(self, key):
    return self.__dict__[key]

  def __setitem__(self, key, value):
    self.__dict__[key] = value
    f = open(self.cacheFile, "w")
    f.write(json.dumps(self.__dict__))
    f.close()

  def __delitem__(self, key):
    del self.__dict__[key]
    f = open(self.cacheFile, "w")
    f.write(json.dumps(self.__dict__))
    f.close()

  def __contains__(self, key):
    return key in self.__dict__

  def __len__(self):
    return len(self.__dict__)

  def __repr__(self):
    return repr(self.__dict__)

def _on_loaded_auth_check():
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
    a = requests.get(f'https://auth.gog.com/token?{s}').json()
    a['expires'] = time.time() + a['expires_in']
    cache['auth'] = a
    window.load_url(content_url)

def token():
  try:
    if cache['auth']['expires'] > time.time():
      return cache['auth']['access_token']
    else:
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
      return cache['auth']['access_token']
  except Exception as e:
    print(e)


def get_games():
  t = token()
  return requests.get('https://embed.gog.com/user/data/games', headers = { 'Authorization': f'Bearer {t}' }).json()['owned']

def download(id, files, outDir):
  t = token()
  game = details(id)
  # TODO: download game here

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


cache = Cache(os.path.expanduser('~/.deckagog.json'))

content_url = 'dist/index.html'
if os.environ.get('DECKAGOG_MODE') == 'dev':
  content_url = 'http://localhost:5173/'

intiial_url = content_url
if 'auth' not in cache:
  intiial_url = 'https://auth.gog.com/auth?client_id=46899977096215655&redirect_uri=https%3A%2F%2Fembed.gog.com%2Fon_login_success%3Forigin%3Dclient&response_type=code&layout=client2'

window = webview.create_window(
  js_api=JsAPI(),
  title='Deckagog',
  url=intiial_url,
  width=1280,
  height=800
)

window.events.loaded += _on_loaded_auth_check

webview.start(debug=True)
