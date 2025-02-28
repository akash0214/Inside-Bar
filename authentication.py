from fyers_apiv3 import fyersModel
import json

# Extracting client details
apiCredFile = open('./apiCred.json')
apiCredObject = json.load(apiCredFile)

client_id = apiCredObject['client_id']
secret_key = apiCredObject['secret_key']
redirect_uri = apiCredObject['redirect_uri']

# Creating a client session
session = fyersModel.SessionModel(
    client_id = client_id,
    secret_key = secret_key,
    redirect_uri = redirect_uri,
    grant_type = "authorization_code",
    response_type = "code"
)
url = session.generate_authcode()
print(url)

auth_code = input("Enter the auth code: ")
session.set_token(auth_code)
token_response = session.generate_token()

# Saving token in separate json file
token_response_object = json.dumps(token_response, indent=4)
with open('access_token.json', 'w') as token:
    token.write(token_response_object)