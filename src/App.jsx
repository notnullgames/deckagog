// import { invoke } from '@tauri-apps/api/tauri'

import { useEffect, useState } from 'react'
import * as gog from './gog.js'
import cx from 'classnames'

function App () {
  const [games, setGames] = useState([])
  const [count, setCount] = useState(0)
  const [currentSelected, setCurrentSelected] = useState(0)
  const [currentDetails, setCurrentDetails] = useState(false)

  // TODO: make sure keys match default steam keys and/or add joystuck support
  const keyDownHandler = e => {
    e.preventDefault()

    if (e.key === 'Enter') {
      setCurrentDetails(currentSelected)
    }

    if (e.key === 'Backspace' && currentDetails !== false) {
      setCurrentDetails(false)
    }

    if (e.key === 'ArrowRight') {
      setCurrentSelected(c => {
        let n = c + 1
        if (n + 1 > games.length) {
          n = 0
        }
        return n
      })
    }

    if (e.key === 'ArrowLeft') {
      setCurrentSelected(c => {
        let n = c - 1
        if (n < 0) {
          n = games.length - 1
        }
        return n
      })
    }

    if (e.key === 'ArrowDown') {
      setCurrentSelected(c => {
        let n = c + 8
        if (n + 1 > games.length) {
          n = c % 8
        }
        return n
      })
    }

    if (e.key === 'ArrowUp') {
      setCurrentSelected(c => {
        let n = c - 8
        if (n < 0) {
          n = c + (Math.floor(games.length / 8) * 8)
          if (n + 1 > games.length) {
            n = n - 8
          }
        }
        return n
      })
    }
  }

  // manage scrolling (top on regular page, to current-poster on list)
  useEffect(() => {
    if (currentDetails === false) {
      document.querySelector('.poster.current')?.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' }, 500)
    } else {
      document.body.scrollIntoView({ behavior: 'smooth' }, 500)
    }
  }, [currentDetails, currentSelected])

  // attach key-handlers
  useEffect(() => {
    window.addEventListener('keydown', keyDownHandler)
    return () => window.removeEventListener('keydown', keyDownHandler)
  }, [games.length, currentDetails])

  // get data
  useEffect(() => {
    gog.games()
      .then(g => {
        setCount(g.length)
        return Promise.all(g.map(id => gog.details(id)))
      }).then(r => {
        const n = r.filter(g => !g?.message && g?._embedded.productType === 'GAME')
        setCount(n.length)
        setGames(n)
      })
      // TODO: rev-sort by purchase-date
      // TODO: filter non-games and DLC
  }, [])

  return (
    <div>
      {currentDetails === false && (
        <div className='posterGrid'>
          {games.length !== count && (
            <div className='wait'>Please wait while I get info about your {count} games.</div>
          )}
          {games.map((game, i) => game?._links?.boxArtImage?.href && (
            <img className={cx('poster', { current: i === currentSelected })} onClick={() => { setCurrentSelected(i); setCurrentDetails(i) }} key={i} width='140' src={game?._links?.boxArtImage?.href} title={game?._embedded?.product?.title} alt={game?._embedded?.product?.title} />
          ))}
        </div>
      )}
      {currentDetails !== false && (
        <div className='infoPage'>
          {/* <a href='#' className='back' onClick={() => setCurrentDetails(false)}>BACK</a> */}
          <h1 className='detail_title' style={{ backgroundImage: `url(${games[currentDetails]?._links?.galaxyBackgroundImage?.href})` }}>{games[currentDetails]?._embedded?.product?.title}</h1>
          <button>Install</button>
          <div className='description' dangerouslySetInnerHTML={{ __html: games[currentDetails].overview }} />
          <pre>{JSON.stringify(games[currentDetails], null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default App
