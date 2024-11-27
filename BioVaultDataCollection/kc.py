from keycloak import keycloak_openid,KeycloakConnectionError,KeycloakAuthenticationError
# returns the user id whne passed to to database
def get_userid(username,password):
    try:
        kcoid= keycloak_openid.KeycloakOpenID('http://localhost:8080','biovault','biovault-client',client_secret_key='fy0OiDrL2BQ7zX26qdkywVrEdoiYHj9r')
        token = kcoid.token(username,password,grant_type='password')
        userinfo = kcoid.userinfo(token['access_token'])
        userid = userinfo['sub']
        return userid
    except KeycloakConnectionError:
        print('Error Connecting to Keycloak')
        exit(1)

    except KeycloakAuthenticationError:
        print('Invalid Username or Password')
        exit(1)