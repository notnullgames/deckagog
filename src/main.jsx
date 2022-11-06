import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom/client'
import Navigation, { VerticalList, HorizontalList, Grid, Focusable } from 'react-key-navigation'
import cx from 'classnames'

import './index.css'

function App () {
  const [games, setGames] = useState([])
  const [count, setCount] = useState(0)
  const [currentSelected, setCurrentSelected] = useState(0)
  const [currentDetails, setCurrentDetails] = useState(false)

  const keyDownHandler = e => {
    e.preventDefault()

    if (e.key === 'Enter') {
      setCurrentDetails(currentSelected)
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

  useEffect(() => {
    document.querySelector('.poster.current')?.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' }, 500)
  }, [currentSelected])

  useEffect(() => {
    if (currentDetails === false) {
      document.querySelector('.poster.current')?.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' }, 500)
    } else {
      document.body.scrollIntoView({
        behavior: 'smooth'
      }, 500)
    }
  }, [currentDetails])

  useEffect(() => {
    window.addEventListener('keydown', keyDownHandler)
    pywebview.api.get_games()
      .then(g => {
        setCount(g.length)
        return Promise.all(g.map((id, i) => fetch(`https://api.gog.com/v2/games/${id}`).then(r => r.json())))
      }).then(r => {
        const n = r.filter(g => !g?.message)
        setCount(n.length)
        setGames(n)
      })
      // TODO: rev-sort by purchase-date
      // TODO: filter non-games and DLC

    return () => window.removeEventListener('keydown', keyDownHandler)
  }, [games.length])

  return (
    <div>
      {currentDetails === false && (
        <div className='posterGrid'>
          {games.length !== count && (
            <div className='wait'>Please wait while I get info about your {count} games.</div>
          )}
          {games.map((game, i) => game?._links?.boxArtImage?.href && (
            <img className={cx('poster', { current: i === currentSelected })} onClick={() => setCurrentDetails(i)} key={i} width='140' src={game?._links?.boxArtImage?.href} title={game?._embedded?.product?.title} alt={game?._embedded?.product?.title} />
          ))}
        </div>
      )}
      {currentDetails !== false && (
        <div className='infoPage'>
          <a href='#' className='back' onClick={() => setCurrentDetails(false)}>BACK</a>
          <pre>{JSON.stringify(games[currentDetails], null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
