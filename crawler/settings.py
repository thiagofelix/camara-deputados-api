# -*- coding: utf-8 -*-

import os

BOT_NAME = 'camara_deputados_api'
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

FEED_EXPORT_ENCODING = 'utf-8'
HTTPCACHE_ENABLED = True
COOKIES_ENABLED = False
LOG_ENABLED = True
LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 5

ITEM_PIPELINES = {
    'crawler.pipelines.StoreItemDBPipeline': 600
}

DATABASE = {
    'drivername': 'postgres',
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'username': os.environ.get('DB_USER', None),
    'password': os.environ.get('DB_PASS', None),
    'database': os.environ.get('DB_NAME', 'camaradeputados')
}
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 2
ROBOTSTXT_OBEY = False
TELNETCONSOLE_ENABLED = False
