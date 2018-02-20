from pyDes import des

TGS_SECRET_KEY = "tgs_key1"
SERVICE_SECRET_KEY = "service1"
SERVICE_SESSION_KEY = "serv_ses"


def make_tgs_response(service_id, enc_tgt, authenticator):
    print("TGS - got request with service_id: ", service_id, " enc_tgt: ",
          enc_tgt, " authenticator: ", authenticator)
    tgt_enc_client_id = enc_tgt["tgt_enc_client_id"]
    tgt_enc_tgs_session_key = enc_tgt["tgt_enc_tgs_session_key"]

    print("TGS - TGS secret key: ", TGS_SECRET_KEY)
    tgt_client_id = des(TGS_SECRET_KEY).decrypt(tgt_enc_client_id)
    tgs_session_key = des(TGS_SECRET_KEY).decrypt(tgt_enc_tgs_session_key)
    print("TGS - Decrypt client_id from TGT with TGS secret key: ",
          tgt_client_id)
    print("TGS - Decrypt TGS session key from TGT with TGS secret key: ",
          tgs_session_key)

    # Decrypt authenticator with TGS_SESSION_KEY
    auth_client_id = des(tgs_session_key).decrypt(authenticator)
    print("TGS - Decrypt client_id from authenticator with TGS session key: ",
          auth_client_id)

    if tgt_client_id == auth_client_id:
        print("TGS - client_id from TGT and Authenticator matched")

        service_enc_client_id = des(SERVICE_SECRET_KEY).encrypt(tgt_client_id)
        service_enc_service_session_key = des(SERVICE_SECRET_KEY).encrypt(
            SERVICE_SESSION_KEY)
        print("TGS - Service Secret Key: ", SERVICE_SECRET_KEY)
        print("TGS - Encrypt client_id with Service Secret Key: ",
              service_enc_client_id)
        print("TGS - Service Session Key: ", SERVICE_SESSION_KEY)
        print("TGS - Encrypt Service Session Key with Service Secret Key: ",
              service_enc_service_session_key)

        service_mandate = {"service_enc_client_id": service_enc_client_id,
                           "service_enc_service_session_key":
                               service_enc_service_session_key}
        print("TGS - Making Service Mandate: ", service_mandate)

        enc_service_session_key = des(tgs_session_key).encrypt(
            SERVICE_SESSION_KEY)
        print("TGS - Encrypt Service Session Key with TGS Session Key: ",
              enc_service_session_key)

        response = {"service_mandate": service_mandate,
                    "enc_service_session_key": enc_service_session_key}
        print("TGS - Sending response: ", response)
        return response

    print("TGT - client_id from TGT and authenticator doesnt match")
    return