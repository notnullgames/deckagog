#!/bin/bash

# this script will create login credentials for you
# run with curl -L https://raw.githubusercontent.com/notnullgames/deckagog/login.sh | bash

curl -L https://github.com/notnullgames/goglogin/releases/download/0.0.0/linux-x86-64.zip > /tmp/linux-x86-64.zip
cd /tmp
unzip linux-x86-64.zip
CODE=$(./goglogin)
rm goglogin

curl -L "https://auth.gog.com/token?client_id=46899977096215655&client_secret=9d85c43b1482497dbbce61f6e4aa173a433796eeae2ca8c5f6129f2dc4de46d9&redirect_uri=https%3A%2F%2Fembed.gog.com%2Fon_login_success%3Forigin%3Dclient&grant_type=authorization_code&code=${CODE}" > ~/.deckagog.json