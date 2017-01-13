#!/usr/bin/env sh

pg_dump -d camaradeputados -h localhost -aF p -f camaradeputados.data.backup
