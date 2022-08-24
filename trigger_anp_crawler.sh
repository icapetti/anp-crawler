#!/bin/bash

if [ "$1" == "local" ];
then
    echo "====== [NOT IMPLEMENTED] The data will be saved locally. Starting ANP crawler... ======"
elif [ "$1" == "s3" ];
then
    echo "====== The data will be saved on AWS S3. Starting ANP crawler... ======"
    scrapy crawl anp
else
    echo "====== Select a valid option for data output: local or s3 ======"
fi