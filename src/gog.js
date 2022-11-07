import { readTextFile, writeTextFile, BaseDirectory } from '@tauri-apps/api/fs'
import { getClient } from '@tauri-apps/api/http'

let client

// load auth from ~/.deckagog.json
let auth
readTextFile('.deckagog.json', { dir: BaseDirectory.Home })
  .then(j => {
    auth = JSON.parse(j)
  })
  .catch(e => {
    window.alert('You must setup auth. Please refer to the README.')
  })

// get the current token (cache or by refresh from rust, due to CORS)
export async function token () {
  if (auth?.expires && Date.now() < auth.expires) {
    console.log('token good, returning')
    return auth.access_token
  } else {
    console.log('token needs refreshing')
    const s = new URLSearchParams({
      client_id: '46899977096215655',
      client_secret: '9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9',
      redirect_uri: 'https://embed.gog.com/on_login_success?origin=client',
      grant_type: 'refresh_token',
      refresh_token: auth.refresh_token
    })
    client = client || await getClient()
    auth = await client.get(`https://auth.gog.com/token?${s.toString()}`).then(r => r.data)
    auth.expires = (auth.expires_in * 1000) + Date.now()
    await writeTextFile('.deckagog.json', JSON.stringify(auth), { dir: BaseDirectory.Home })
    console.log('token saved')
    return auth
  }
}

// get user's game-IDs (from rust, due to CORS)
export async function games () {
  const t = await token()
  client = client || await getClient()
  return client.get('https://embed.gog.com/user/data/games', { headers: { Authorization: `Bearer ${t}` } })
    .then(r => r.data)
    .then(g => g.owned)
}

// get game-details
export function details (id) {
  return fetch(`https://api.gog.com/v2/games/${id}`).then(r => r.json())
}
