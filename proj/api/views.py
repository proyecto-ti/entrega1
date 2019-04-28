from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hashlib import sha1
import hmac
import base64


api_key = 'A#soL%kRvHX2qHm'
api_url_base = 'https://integracion-2019-dev.herokuapp.com/bodega/'

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
    print(encoded)
    return encoded


headers = {'Content-Type': 'application/json',
           'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request('GET'))}


# Tutorial sacado de:
# http://polyglot.ninja/django-rest-framework-getting-started/

class InventoriesView(APIView):
    def get(self, request):
        #ESTA ES LA FUNCIÓN QUE HAY QUE MODIFICAR PARA LOS GET
        #SOLO SE MUESTRAN PRODUCTOS DE ALMACEN DESPACHO, ALMACENES GENERALES Y PULMON

        result = requests.get('{}almacenes/'.format(api_url_base), headers=headers).json()


        return Response({"message": "Hello World!"})


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
