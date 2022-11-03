# deckagog

A simple way to install Gog games (Windows and Linux) on steamdeck.

## Installation

Download [the release](TODO) and put it in a sensible directory. Add it as a non-steam game in steam, and run it.


## thanks

I got some ideas from:

- [heroic-gogl](https://github.com/Heroic-Games-Launcher/heroic-gogdl)
- [HeroicBashLauncher](https://github.com/redromnon/HeroicBashLauncher)

### notes


```sh
# install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --force-reinstall

# you can put this in ~/.bashrc to persist
export PATH=${PATH}:/home/deck/.local/bin

# install stuff you will need
pip install vdf requests
```