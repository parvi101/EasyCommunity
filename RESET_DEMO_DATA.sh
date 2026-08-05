#!/usr/bin/env bash
cd "$(dirname "$0")"
rm -f data/*.db
echo "Demo database reset. It will be recreated when the app starts."
