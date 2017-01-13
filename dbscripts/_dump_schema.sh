#!/usr/bin/env sh

pg_dump -d camaradeputados -h localhost -sOc -t scrap_items -t votos -t deputados -t presencas --if-exists -f camaradeputados.schema.backup
