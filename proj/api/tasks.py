from __future__ import absolute_import, unicode_literals
from celery import task
import requests
from .funciones_bodega import *

@task
def pedir_stock_minimo_grupos():
    pedir = restar_stock_actual()
    liberar_recepcion()
    for sku, cantidad in pedir.items():
        pedir_productos_sku(sku, 1)
        liberar_recepcion()

@task
def crear_productos():
    enviar_fabricar()
