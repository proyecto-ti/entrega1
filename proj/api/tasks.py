from __future__ import absolute_import, unicode_literals
from celery import task
import requests


@task()
def get_inventories_grupoxx():
    url = 'http://tuerca' + str(2) + '.ing.puc.cl/inventories/'
    headers_ = {'Content-Type': 'application/json'}
    result = requests.get(url, headers=headers_)
    print(result.json())
