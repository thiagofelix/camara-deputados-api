# -*- coding: utf-8 -*-

import os

BOT_NAME = 'camara_deputados_api'
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

FEED_URI = 'stdout:'
FEED_EXPORT_ENCODING = 'utf-8'
HTTPCACHE_ENABLED = True
DELTAFETCH_ENABLED = True
COOKIES_ENABLED = False
LOG_ENABLED = False

ITEM_PIPELINES = {
    'crawler.pipelines.StoreItemDBPipeline': 600
}

SPIDER_MIDDLEWARES = {
    # 'scrapy_deltafetch.DeltaFetch': 100,
}

DATABASE = {
    'drivername': 'postgres',
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'username': os.environ.get('DB_USER', None),
    'password': os.environ.get('DB_PASS', None),
    'database': os.environ.get('DB_NAME', 'camaradeputados')

}
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
TELNETCONSOLE_ENABLED = False
