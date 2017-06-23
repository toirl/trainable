#!/bin/sh
python setup.py develop
trainable-admin db init
pserve heroku.ini http_port=$PORT client_secret=$CLIENT_SECRET
