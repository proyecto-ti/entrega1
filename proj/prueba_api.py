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
           'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request('GET5cbd3ce444f67600049431b9'))}

print(headers['Authorization'])

result = requests.get('{}/stock?almacenId=5cbd3ce444f67600049431b9/'.format(api_url_base), headers=headers).json()

for item in result:
    print(item)


headers = {'Content-Type': 'application/json',
           'Authorization': 'INTEGRACION grupo2:{}'.format(sign_request('PUT100110'))}

print(headers['Authorization'])

result = requests.get('{}fabrica/fabricarSinPago/'.format(api_url_base), headers=headers)
print(result)