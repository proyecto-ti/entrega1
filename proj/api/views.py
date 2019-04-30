from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hashlib import sha1
import hmac
from .funciones_bodega import *
from .datos import *

name_sku_dict = {"Sesamo": "1011",
                "Nori_Entero": "1016",
                "Camaron": "1006",
                "Azucar": "1003",
                "Arroz_Grano_Corto": "1001"}

class InventoriesView(APIView):
    def get(self, request):
        #ESTA ES LA FUNCIÓN QUE HAY QUE MODIFICAR PARA LOS GET
        #SOLO SE MUESTRAN PRODUCTOS DE ALMACEN DESPACHO, ALMACENES GENERALES Y PULMON

        lista = stock()
        return Response(json.dumps(lista,  sort_keys=True, ensure_ascii=False))



# Cuando hagan post con POSTMAN hay que ponerle un / al final de la URL, así:
# http://127.0.0.1:8000/api/orders/
class OrdersView(APIView):
    def post(self, request):
        #ESTA ES LA FUNCION QUE HAY QUE MODIFICAR PARA LOS POST
        sku = request.data.get("sku")
        cantidad = request.data.get("cantidad")
        almacenId = request.data.get("almacenId")
        if not sku or not cantidad or not almacenId:
            return Response(data="No se creó el pedido por un error del cliente en la solicitud", status.HTTP_400_BAD_REQUEST)

        inventario = get_inventories_grupox(2).json()
        if sku in inventario.keys():
            despachar_producto(sku, cantidad)
            envio = mover_entre_bodegas(sku, cantidad, almacen_id_dict["recepcion"], almacenId, precio=0, oc='')
            if envio.status_code == 200:
                dictionary = {"sku": sku, "cantidad": cantidad, "almacenId": almacenId, "grupoProveedor": "2", "aceptado": True, "despachado": True}
                return Response(json.dumps(dictionary))
            else
                return Response(data="error de nuestro grupo. Oops!", status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="Producto no se encuentra", status.HTTP_404_NOT_FOUND)
