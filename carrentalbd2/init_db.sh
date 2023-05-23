#!/usr/bin/bash


initdb -D database
createuser --encrypted --pwprompt $2 --password $3
createdb --owner=$2 $1