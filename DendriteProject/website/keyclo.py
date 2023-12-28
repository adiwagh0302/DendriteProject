from keycloak import KeycloakOpenID, KeycloakAdmin

# Create a keycloak client object
keycloak_client = KeycloakOpenID(server_url="https://keycloak-server.com",
                                 client_id="client-id",
                                 realm_name="realm",
                                 client_secret_key="your-client-secret")

# Create a keycloak admin object
keycloak_admin = KeycloakAdmin(server_url="https://keycloak-server.com",
                               username="admin-username",
                               password="admin-password",
                               realm_name="realm",
                               verify=True)
