#!/bin/bash

echo "cleaning nginx configuration"

if [ ! -f $FILE ];
then
  rm /etc/nginx/sites-available/testing-rewrite
  echo "entry in sites-available removed"
else
  echo "entry in sites-available was not there"
fi

if [ ! -f $FILE ];
then
  rm /etc/nginx/sites-enabled/testing-rewrite
  echo "link in sites-enabled removed"
else
  echo "link in sites-enabled was not there"
fi

echo "restarting server"
service nginx restart

# put result file
echo "removing /var/www/testing-rewrite/ directory"
rm -rf /var/www/testing-rewrite/
