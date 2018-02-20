from auth import make_auth_response
from tgs_server import make_tgs_response
from service import call_service

from pyDes import des

CLIENT_ID = "client_1"
CLIENT_PASSWORD = "password"
SERVICE_ID = "print_service"

print("CLIENT - Make auth request with client_id: ", CLIENT_ID)
auth_response = make_auth_response(CLIENT_ID)
print("CLIENT - Auth response: ", auth_response)
enc_tgs_session_key = auth_response["enc_tgs_session_key"]
enc_tgt = auth_response["enc_tgt"]

tgs_session_key = des(CLIENT_PASSWORD).decrypt(enc_tgs_session_key)
print("CLIENT - Client password: ", CLIENT_PASSWORD)
print("CLIENT - Decrypted with password tgs_session-key: ", tgs_session_key)

tgs_authenticator = des(tgs_session_key).encrypt(CLIENT_ID)
print("CLIENT - Make encrypted with tgs_session_key client_id "
      "(tgs_authenticator): ", tgs_authenticator)

print("CLIENT - Make TGS request")
tgs_response = make_tgs_response(SERVICE_ID, enc_tgt, tgs_authenticator)
print("CLIENT - TGS response: ", tgs_response)

enc_service_session_key = tgs_response["enc_service_session_key"]
service_mandate = tgs_response["service_mandate"]

service_session_key = des(tgs_session_key).decrypt(enc_service_session_key)
print("CLIENT - Decrypted with tgs_session_key service_session_key: ",
      service_session_key)

service_authenticator = des(service_session_key).encrypt(CLIENT_ID)
print("CLIENT - Make encrypted with service_session_key client id"
      "(service_authenticator): ", service_authenticator)

print("CLIENT - Calling service")
call_service(service_mandate, service_authenticator)
