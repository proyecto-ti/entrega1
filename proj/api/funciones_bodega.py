import requests
from hashlib import sha1
import hmac
import base64
import json

api_key = 'A#soL%kRvHX2qHm'
api_url_base = 'https://integracion-2019-dev.herokuapp.com/bodega/'

name_sku_dict = {"sesamo": "1011",
                "nori_Entero": "1016",
                "camaron": "1006",
                "azucar": "1003",
                "arroz_grano_corto": "1001"}

almacen_id_dict = {"recepcion" : "5cbd3ce444f67600049431b9",
                    "despacho" : "5cbd3ce444f67600049431ba",
                    "almacen_1" : "5cbd3ce444f67600049431bb",
                    "almacen_2" : "5cbd3ce444f67600049431bc",
                    "pulmon" : "5cbd3ce444f67600049431bd",
                    "cocina" : "5cbd3ce444f67600049431be"}

sku_stock_dict = {  "1301" : 50, "1201" : 250, "1209" : 20, "1109" : 50,"1309" : 170,
                    "1106" : 400,"1114" : 50,"1215" : 20,"1115" : 30,"1105" : 50,
                    "1013" : 300,"1216" : 50,"1116" : 250,"1110" : 80,"1310" : 20,
                    "1210" : 150,"1112" : 130,"1108" : 10,"1407" : 40,"1207" : 20,
                    "1107" : 50,"1307" : 170,"1211" : 60}

min_amount = {"1301" : 50,"1201" : 250,"1209" : 20,"1109" : 50,"1309" : 170,"1106" : 400,
            "1114" : 50,"1215" : 20,"1115" : 30,"1105" : 50,"1013" : 300,"1216" : 50,
            "1116" : 250,"1110" : 80,"1310" : 20,"1210" : 150,"1112" : 130,"1108" : 10,
            "1407" : 40,"1207" : 20,"1107" : 50,"1307" : 170,"1211" : 60}

our_products = ["1001". "1003", "1006", "1016", "1011"]

def sign_request(string):
    key = str.encode(api_key)
    raw = str.encode(string)
    hashed = hmac.new(key, raw, digestmod=sha1)
    hashed_bytes = hashed.digest()
    encoded = base64.b64encode(hashed_bytes)
    encoded = str(encoded, 'UTF-8')
    return encoded

def ObtenerSkuconStock(almacenId):
    message = 'GET' + almacenId
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}skusWithStock?almacenId={}'.format(api_url_base, almacenId)
    result = requests.get(url, headers=headers).json()
    return result

def revisarBodega():
    url = '{}almacenes/'.format(api_url_base)

    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request('GET'))}

    result = requests.get(url, headers=headers).json()
    return result

def fabricarSinPago(sku, cantidad):
    message = 'PUT' + sku + str(cantidad)
    url = '{}fabrica/fabricarSinPago'.format(api_url_base)
    headers_ = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"sku": sku, "cantidad": int(cantidad)}

    result = requests.put(url, headers=headers_ , data=json.dumps(body))
    if result.status_code == 200:
        return result
    else:
        return result

def update_dictionary_stocks(dictionary, stock_type):
    for sku in stock_type:
        if not sku["_id"] in dictionary:
            dictionary.update({ sku["_id"] : sku["total"] })
        else:
            dictionary[sku["_id"]] += sku["total"]
    return dictionary
