<img src="src-tauri/icons/icon.png" alt="deckagog" width="200" />

A simple way to install Gog games (Windows and Linux) on steamdeck.

> I am in no way affiliated with Steam or Gog. This is just a tool I wanted, and I thought it could be useful to others.

![screenshot](screenshot.png)


## Installation

Download [the latest release](https://github.com/notnullgames/deckagog/releases) and put it in a sensible directory. Add it as a non-steam game in steam.

For now, you will need to make an initial login token externally. I made a little script you can run in desktop-mode:

```sh
curl -L https://raw.githubusercontent.com/notnullgames/deckagog/main/login.sh | bash
```

You should only need to do this once.

## TODO

This is not done at all. I need to do a few things:

- Use [player-id](https://playerdb.co/) to link up better data
- actually install windows games in proton
- make non-steam-game entries directly
- Make plugins for gog, humblebundle, ea, etc and rename the main project
- look at [tauri-oauth-supabase](https://github.com/JeaneC/tauri-oauth-supabase) for example of 
spawning window and watching URL chnage (for gog auth and others)
- key-nav, very light graphics & basic layout example [here](https://github.com/dead/react-key-navigation/tree/master/examples/youtube-react-tv)
- use bunjs, since it can totally work fiune with tauri app, and build as [executable](https://bun.sh/docs/bundler/executables) for easier install



## thanks

I got some ideas from:

- [heroic-gogl](https://github.com/Heroic-Games-Launcher/heroic-gogdl)
- [HeroicBashLauncher](https://github.com/redromnon/HeroicBashLauncher)
- [GameLauncherResearch](https://github.com/Lariaa/GameLauncherResearch/wiki)
