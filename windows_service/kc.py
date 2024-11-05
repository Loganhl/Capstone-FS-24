from keycloak import KeycloakAdmin, KeycloakOpenID
import time
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/",
                                  client_id="biovault-client",
                                  realm_name="biovault",
                                  client_secret_key="VxW35Qjm8NEs2V9aoheEHTkvEVd3hVXv")
token = keycloak_openid.token('gar7mn',password='Wand4511',grant_type='password'),

def get_userid(access_token):
    useinfo = keycloak_openid.userinfo(access_token)
    user_id = useinfo['sub']
    return user_id


class KC_OID(KeycloakOpenID):
    def __init__(self,username,password, server_url, realm_name, client_id, client_secret_key=None, verify=True, custom_headers=None, proxies=None, timeout=60, cert=None, max_retries=1):
        super().__init__(username,password,server_url, realm_name, client_id, client_secret_key, verify, custom_headers, proxies, timeout, cert, max_retries)
        self.usertoken = self.token(username,password,"password")
    def get_user_id(self):
        userinfo = self.userinfo(self.usertoken)
        userid = userinfo['sub']
        return userid

