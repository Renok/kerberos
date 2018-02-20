from pyDes import des

TGS_SECRET_KEY = "tgs_key1"
TGS_SESSION_KEY = "tgs_sess"


def make_auth_response(client_id):
    print("AUTH - Got request with client_id: ", client_id)
    print("AUTH - Checking database for client_id match")
    with open("db.txt", "r") as clients:
        for row in clients.readlines():
            credentials = row.strip("\n").split(" ")
            client, password = credentials[0], credentials[1]

            if client_id == client:
                print("AUTH - client found: ", credentials)

                enc_tgs_session_key = des(password).encrypt(
                    TGS_SESSION_KEY)
                print("AUTH - TGS session key: ", TGS_SESSION_KEY)
                print("AUTH - Make encrypt tgs_session_key with client"
                      " password: ", enc_tgs_session_key)

                print("AUTH - Making TGT...")
                print("AUTH - TGS secret key: ", TGS_SECRET_KEY)
                print("AUTH - Encrypt client_id and tgs_session_key with"
                      " TGS secret key")
                tgt_enc_client_id = des(TGS_SECRET_KEY).encrypt(client_id)
                tgt_enc_tgs_session_key = des(TGS_SECRET_KEY).encrypt(
                    TGS_SESSION_KEY)
                enc_tgt = {"tgt_enc_client_id": tgt_enc_client_id,
                           "tgt_enc_tgs_session_key": tgt_enc_tgs_session_key}
                print("AUTH - TGT done: ", enc_tgt)

                print("AUTH - Response enc_session_key and tgt to client")
                response = {"enc_tgs_session_key": enc_tgs_session_key,
                            "enc_tgt": enc_tgt}
                print("AUTH - response: ", response)
                return response
        print("AUTH - No DB client_id match")
    return
