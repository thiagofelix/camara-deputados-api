import os
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.models import db_connect

def crawl(name, **options):
    settings = get_project_settings()
    settings['HTTPCACHE_ENABLED'] = False
    settings['LOG_LEVEL'] = 'INFO'
    process = CrawlerProcess(settings)
    process.crawl(name, **options)
    process.start()

def votos(event, context):
    crawl('voto', data='hoje')

def presencas(event, context):
    crawl('presenca', data='hoje')

def deputados(event, context):
    crawl('deputado')

def dbscripts():
    here = os.path.dirname(os.path.realpath(__file__))
    engine = db_connect()
    files = (
        'create_views.sql',
        'grand_postgrest_permissions.sql'
    )

    for file_name in files:
        with open(os.path.join(here, 'dbscripts', file_name), 'r') as sql_file:
            logging.info('Running %s' % file_name)
            engine.execution_options(autocommit=True).execute(sql_file.read())

