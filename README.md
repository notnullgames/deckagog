<img src="src-tauri/icons/icon.png" alt="deckagog" width="200" />

A simple way to install Gog games (Windows and Linux) on steamdeck.

> I am in no way affiliated with Steam or Gog. This is just a tool I wanted, and I thought it could be useful to others.

![screenshot](screenshot.png)


## Installation

Download [the release](TODO) and put it in a sensible directory. Add it as a non-steam game in steam.

For now, you will need to make an initial login token externally. I made a little script you can run in desktop-mode:

```sh
curl -L https://raw.githubusercontent.com/notnullgames/deckagog/login.sh | bash
```

You should only need to do this once.

## thanks

I got some ideas from:

- [heroic-gogl](https://github.com/Heroic-Games-Launcher/heroic-gogdl)
- [HeroicBashLauncher](https://github.com/redromnon/HeroicBashLauncher)
