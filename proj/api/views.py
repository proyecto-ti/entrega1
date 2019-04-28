from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hashlib import sha1
import hmac
from .funciones_bodega import *


name_sku_dict = {"Sesamo": "1011",
                "Nori_Entero": "1016",
                "Camaron": "1006",
                "Azucar": "1003",
                "Arroz_Grano_Corto": "1001"}

class InventoriesView(APIView):
    def get(self, request):
        #ESTA ES LA FUNCIÓN QUE HAY QUE MODIFICAR PARA LOS GET
        #SOLO SE MUESTRAN PRODUCTOS DE ALMACEN DESPACHO, ALMACENES GENERALES Y PULMON
        print("prueba")
        stock_recepcion = ObtenerSkuconStock(almacen_id_dict['recepcion'])
        stock_almacen_1 = ObtenerSkuconStock(almacen_id_dict['almacen_1'])
        stock_almacen_2 = ObtenerSkuconStock(almacen_id_dict['almacen_2'])
        stock_pulmon = ObtenerSkuconStock(almacen_id_dict['pulmon'])

        print("prueba2")
        dict = update_dictionary_stocks({}, stock_recepcion)
        dict = update_dictionary_stocks(dict, stock_almacen_1)
        dict = update_dictionary_stocks(dict, stock_almacen_2)
        dict = update_dictionary_stocks(dict, stock_pulmon)

        print("prueba3")
        return Response(json.dumps(dict))


# Cuando hagan post con POSTMAN hay que ponerle un / al final de la URL, así:
# http://127.0.0.1:8000/api/orders/
class OrdersView(APIView):
    def post(self, request):
        #ESTA ES LA FUNCION QUE HAY QUE MODIFICAR PARA LOS POST
        sku = request.data.get("sku")
        cantidad = request.data.get("cantidad")
        almacenId = request.data.get("almacenId")
        if not sku or not cantidad or not almacenId:
            return Response({"Falta un parámetro obligatorio"})
        return Response({"message": "Pediste {} de productos!".format(cantidad)})
