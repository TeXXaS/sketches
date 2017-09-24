#!/bin/bash

echo "preparing nginx configuration"

cp config /etc/nginx/sites-available/testing-rewrite
echo "entry in sites-available is up-to-date"

if [ ! -f $FILE ];
then
  ln -s /etc/nginx/sites-available/testing-rewrite /etc/nginx/sites-enabled/testing-rewrite
  echo "link in sites-enabled added"
else
  echo "link in sites-enabled was there"
fi

echo "preparing www directory"
mkdir -p /var/www/testing-rewrite/
cp *.html /var/www/testing-rewrite/
cp -r prods /var/www/testing-rewrite/
chown www-data:www-data -R /var/www/testing-rewrite

echo "restarting server"
service nginx restart

echo "to see processing"
echo "tail -f /var/log/nginx/testing-rewrite-error.log"
echo "pro-tip - throw some enters to mark location before going to your browser"
echo "page address: http://localhost:10080/wiki/File:image.jpg "
