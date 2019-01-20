#!/usr/bin/env bash

printenv | sed 's/^\(.*\)$/export \1/g' > /etc/profile.d/env.sh

cron -f
