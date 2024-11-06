from keycloak import keycloak_openid
# returns the user id whne passed to to database
def get_userid(username,password):
    kcoid= keycloak_openid.KeycloakOpenID('http://localhost:8080','biovault','biovault-client',client_secret_key='fy0OiDrL2BQ7zX26qdkywVrEdoiYHj9r')
    token = kcoid.token(username,password,grant_type='password')
    userid = token['sub']
    return userid