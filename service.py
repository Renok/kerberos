from pyDes import des

SERVICE_SECRET_KEY = "service1"


def call_service(service_mandate, authenticator):
    print("SERVICE - Got request with service_mandate: ", service_mandate,
          " authenticator: ", authenticator)
    service_enc_client_id = service_mandate["service_enc_client_id"]
    service_enc_service_session_key = \
        service_mandate["service_enc_service_session_key"]

    client_id = des(SERVICE_SECRET_KEY).decrypt(service_enc_client_id)
    service_session_key = \
        des(SERVICE_SECRET_KEY).decrypt(service_enc_service_session_key)
    print("SERVICE - Service Secret Key: ", SERVICE_SECRET_KEY)
    print("SERVICE - Decrypt client_id from service mandate with Service "
          "Secret Key: ", client_id)
    print("SERVICE - Decrypt Service Session Key from service mandate with "
          "Service Secret Key: ", service_session_key)

    auth_client_id = des(service_session_key).decrypt(authenticator)
    print("SERVICE - Decrypt Client Id from authenticator with Service "
          "Session Key: ", client_id)

    print("SERVICE - Checking if Client Id form Authenticator and Service "
          "Mandate Match")
    if client_id == auth_client_id:
        print("SERVICE - Client Id matched")
        print("SERVICE - SERVICE CALLOUT")
    else:
        print("SERVICE - Client Id doesnt match")
