#!/bin/bash
PYTHON_ENV="default-crawlers"
PIP="/home/admin/.miniconda3/envs/$PYTHON_ENV/bin/pip"
REQUIREMENTS="/home/admin/anp-crawler/requirements.txt"

echo "Installing requirements..."
$PIP install -r "$REQUIREMENTS"

echo "Updating environment files..."
touch /home/admin/.env
echo "$CRAWLER_ENVIRONMENT" >> /home/admin/.env

echo "Updating services and environment files..."
sudo mkdir -p /var/log/scrapyd
sudo touch /var/log/scrapyd/access.log
sudo touch /var/log/scrapyd/error.log
sudo cp -f /home/admin/anp-crawler/.deploy/*.service /etc/systemd/system/
sudo cp -f /home/admin/anp-crawler/.deploy/.env /home/admin/.env

echo "Restarting services..."
sudo systemctl daemon-reload
sudo systemctl restart scrapyd

echo "Done!"