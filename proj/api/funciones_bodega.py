import requests
from hashlib import sha1
import hmac
import base64
import json
from .poblamiento import excel_final

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


def sign_request(string):

    # key = b"CONSUMER_SECRET&" #If you dont have a token yet
    key = str.encode(api_key)
    # The Base String as specified here:
    raw = str.encode(string) # as specified by OAuth

    hashed = hmac.new(key, raw, digestmod=sha1)

    hashed_bytes = hashed.digest()
    # The signature
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
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    body = {"sku": sku, "cantidad": int(cantidad)}

    result = requests.put(url, headers=headers, data=json.dumps(body))
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

def obtener_productos_almacen(almacenId, sku):
    message = 'GET' + almacenId + sku
    headers = {'Content-Type': 'application/json',
               'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
    url = '{}stock?almacenId={}&sku={}'.format(api_url_base, almacenId, sku)
    result = requests.get(url, headers=headers).json()
    return result


def obtener_id_producto(sku, cantidad, almacenId):
    #lista de almacenes con el producto
    cantidad_id = 0
    lista_id_productos = []
    lista_productos = ObtenerSkuconStock(almacenId)
    for producto in lista_productos:
        if producto['_id'] == sku:
            lista_productos_almacen = obtener_productos_almacen(almacenId, sku)
            print(lista_productos_almacen)
            for producto_unitario in lista_productos_almacen:
                lista_id_productos.append(producto_unitario['_id'])
                cantidad_id += 1
                if cantidad_id == cantidad:
                    return lista_id_productos
    # en caso de que la cantidad sea mayor que lo que se tiene, igual se entrega la lista con todos los existentes
    return lista_id_productos

def mover_entre_almacenes(sku, cantidad, almacenId_origen, almacenId_destino):
    lista_id = obtener_id_producto(sku, cantidad, almacenId_origen)
    for productoId in lista_id:
        message = 'POST' + productoId + almacenId_destino
        url = '{}moveStock'.format(api_url_base)
        headers_ = {'Content-Type': 'application/json',
                    'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
        body = {"productoId": productoId, "almacenId": almacenId_destino}

        requests.post(url, headers=headers_, data=json.dumps(body))


def mover_entre_bodegas(sku, cantidad, almacenId_origen, almacenId_destino, precio=0, oc=''):
    lista_id = obtener_id_producto(sku, cantidad, almacenId_origen)
    for productoId in lista_id:
        message = 'POST' + productoId + almacenId_destino
        url = '{}moveStock'.format(api_url_base)
        headers_ = {'Content-Type': 'application/json',
                    'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request(message))}
        body = {"productoId": productoId, "almacenId": almacenId_destino}
        requests.post(url, headers=headers_, data=json.dumps(body))


def pedir_productos_sku(sku, cantidad):
    productos = excel_final() #lista de los productos
    productores = productos[sku].productores
    total_pedido = 0
    for grupo in productores:
        try:
            result = get_inventories_grupox(grupo)
            #print("GRUPO", str(grupo), "esta con STA_CODE:", result.status_code)
            if grupo != 2 and result.status_code == 200:
                for resultados in result.json():
                    if resultados['sku'] == sku:
                        result_2 = post_orders_grupox(grupo, cantidad, sku)
                        print(result_2)
            else:
                pass
        except:
            pass

def cantidad_producto(sku):
    cantidad = 0
    for almacen in almacen_id_dict:
        lista_productos = ObtenerSkuconStock(almacen_id_dict[almacen])
        for producto in lista_productos:
            if producto['_id'] == sku:
                cantidad += producto['total']
                break
    return cantidad
#pedir_productos_sku('1001', 1)

def get_inventories_grupox(grupo):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/inventories/'
    headers_ = {'Content-Type': 'application/json'}
    result = requests.get(url, headers=headers_)
    return result

def post_orders_grupox(grupo, cantidad, sku):
    url = 'http://tuerca' + str(grupo) + '.ing.puc.cl/orders/'
    headers_ = {'Content-Type': 'application/json'}
    body = {'sku': sku, 'cantidad': cantidad, 'almacenId': almacen_id_dict['recepcion']}
    result = requests.post(url, headers=headers_, data=json.dumps(body))
    return result
"""
try:
    #print(get_inventories_grupox(2).json())
    print(pedir_productos_sku('1001', 1))
    #print(get_inventories_grupox(2).json())
except:
    print("dias")
"""


def liberar_recepcion():
    #funcion que deja recepcion vacia, se mandan productos a almcanen1 o almacen2
    datos_bodegas = revisarBodega()
    #espacio en recepcion
    espacio_usado = datos_bodegas[0]['usedSpace']
    if espacio_usado == 0:
        #recepcion ya esta vacia
        return
    else:
        lista_recepcion = ObtenerSkuconStock("5cbd3ce444f67600049431b9")
        for producto in lista_recepcion:
            #se actualizan datos de bodega
            datos_bodegas = revisarBodega()
            #revisa si cabe en almacen1
            if producto['total'] <= datos_bodegas[2]['totalSpace'] - datos_bodegas[2]['usedSpace']:
                #traspasa todos esos productos a almacen1
                mover_entre_almacenes(producto['_id'], producto['total'], "5cbd3ce444f67600049431b9", "5cbd3ce444f67600049431bb")
            #revisa si cabe en almacen2
            elif producto['total'] <= datos_bodegas[3]['totalSpace'] - datos_bodegas[3]['usedSpace']:
                #traspasa todos esos productos a almacen2
                mover_entre_almacenes(producto['_id'], producto['total'], "5cbd3ce444f67600049431b9", "5cbd3ce444f67600049431bc")
    return

def despachar_producto(sku, cantidad):
    #cantidad que se ha envidado a despacho
    datos_bodegas = revisarBodega()
    capacidad_despacho = datos_bodegas[1]['totalSpace'] - datos_bodegas[1]['usedSpace']
    if capacidad_despacho == 0:
        return
    elif capacidad_despacho >= cantidad:
        cantidad_despachar = cantidad
    else:
        cantidad_despachar = capacidad_despacho
    #revisa si producto esta en pulmon
    lista_pulmon = ObtenerSkuconStock("5cbd3ce444f67600049431bd")
    for producto in lista_pulmon:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                # se tiene la cantidad que se necesita
                mover_entre_almacenes(sku, cantidad_despachar, "5cbd3ce444f67600049431bd", "5cbd3ce444f67600049431ba")
                return
            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], "5cbd3ce444f67600049431bd", "5cbd3ce444f67600049431ba")
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en almacen1
    lista_almacen1 = ObtenerSkuconStock("5cbd3ce444f67600049431bb")
    for producto in lista_almacen1:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                #se tiene la cantidad que se necesita
                mover_entre_almacenes(sku, cantidad_despachar, "5cbd3ce444f67600049431bb", "5cbd3ce444f67600049431ba")
                return
            elif producto['total'] < cantidad_despachar:
                #no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], "5cbd3ce444f67600049431bb", "5cbd3ce444f67600049431ba")
                cantidad_despachar -= producto['total']
            break
    #revisa si producto esta en almacen2
    lista_almacen2 = ObtenerSkuconStock("5cbd3ce444f67600049431bc")
    for producto in lista_almacen2:
        if producto['_id'] == sku:
            if producto['total'] >= cantidad_despachar:
                # se tiene la cantidad que se necesita
                mover_entre_almacenes(sku, cantidad_despachar, "5cbd3ce444f67600049431bc", "5cbd3ce444f67600049431ba")
                return
            elif producto['total'] < cantidad_despachar:
                # no se tiene la cantidad que se necesita, se manda lo que se tiene
                mover_entre_almacenes(sku, producto['total'], "5cbd3ce444f67600049431bc", "5cbd3ce444f67600049431ba")
                cantidad_despachar -= producto['total']
            break
    return
