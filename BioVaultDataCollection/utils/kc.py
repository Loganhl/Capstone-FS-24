from keycloak import keycloak_openid

def get_userid(username, password):
    kcoid = keycloak_openid.KeycloakOpenID('http://localhost:8080', 'biovault', 'biovault-client',client_secret_key='fy0OiDrL2BQ7zX26qdkywVrEdoiYHj9r')
    token = kcoid.token(username, password, grant_type='password')
    userinfo = kcoid.userinfo(token['access_token'])
    return userinfo['sub']
