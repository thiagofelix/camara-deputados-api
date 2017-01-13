# -*- coding: utf-8 -*-

import ast
import logging
import hashlib

from datetime import datetime
from scrapy.exporters import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder
from sqlalchemy.orm import sessionmaker
from models import ScrapItem, db_connect, create_tables

def getkey(item, name):
    genkey = lambda x: hashlib.sha1(x.encode('utf-8')).hexdigest()

    if name == 'presenca':
        return genkey(item['ideCadastro'] + item['data'] + item['descricao'])
    elif name == 'deputado':
        return genkey(item['ideCadastro'] + item['numLegislatura'])
    elif name == 'voto':
        return genkey(item['ideCadastro'] + item['proposicao'] + item['sessao'])

class JsonExporter(BaseItemExporter):
    def __init__(self, **kwargs):
        self._configure(kwargs, dont_fail=True)
        kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**kwargs)

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        return self.encoder.encode(itemdict) + '\n'

class StoreItemDBPipeline(object):
    """Camara pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)
        self.exporter = JsonExporter(encoding='utf-8')

    def open_spider(self, spider):
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        """Save items in the database.
        This method is called for every item pipeline component.
        """
        id = getkey(item, spider.name)
        data = self.exporter.export_item(item)
        model = ScrapItem(id=id, doc=ast.literal_eval(data), kind=spider.name,
                          updated_at=datetime.now())

        try:
            new_model = self.session.merge(model)
            self.session.add(new_model)
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return item
