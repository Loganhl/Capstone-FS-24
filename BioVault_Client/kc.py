import keycloak
from keycloak import KeycloakOpenID
adapter = keycloak.connection.HTTPAdapter()
cont =adapter.get_connection('http://localhost:8080')

kconect = KeycloakOpenID('http://localhost:8080',realm_name='biovault',client_id='biovault-client',client_secret_key='VxW35Qjm8NEs2V9aoheEHTkvEVd3hVXv')

kconect.a_register_client('eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIzYjU1MTc4YS05ZTFkLTQxODctYjEwOC0yMWRlMjdiY2ZmZTQifQ.eyJleHAiOjE3MzA5MjM4MTQsImlhdCI6MTczMDc1MTAxNCwianRpIjoiMGQyNDcyZTQtNTlhZi00MjBjLTk0OTktYTAyM2Q2ODU5MmVjIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9iaW92YXVsdCIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MC9yZWFsbXMvYmlvdmF1bHQiLCJ0eXAiOiJJbml0aWFsQWNjZXNzVG9rZW4ifQ.Cv1C9LwG-HNfpQCYg7HbXzQX-osYUS7yPqss2ALkmf8SW1oqZTkZvn4ujrwejO_QTe40GsawjmaK5_Ne3HfXSA',
                          payload={'client_id':'biovault-client'})