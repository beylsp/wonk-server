#!/bin/sh

user=$(oauth2l fetch -f json --json client_secret.json userinfo.email | \
	python -c "import sys, json; print json.load(sys.stdin)['id_token']['sub']")

token=$(oauth2l fetch -f json --json client_secret.json userinfo.email | \
	python -c "import sys, json; print json.load(sys.stdin)['access_token']")

authtoken=$(curl -s -H "Token-Provider: google" -H "Access-Token: $token" -H "User-Id: $user" http://127.0.0.1:5000/token/ | \
     python -c "import sys, json; print json.load(sys.stdin)['token']")

curl -s -H "Authentication-Token: $authtoken" -H "User-Id: $user" -H "If-Modified-Since: Sun, 1 May 1994 14:20:00 GMT" http://127.0.0.1:5000/r/

curl -s -H "Authentication-Token: $authtoken" -H "User-Id: $user" http://127.0.0.1:5000/r/5010/
