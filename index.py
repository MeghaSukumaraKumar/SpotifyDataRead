import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
CLIENT_ID= os.getenv('CLIENT_ID')
CLIENT_SECRET= os.getenv('CLIENT_SECRET')

#CREATE A TOKEN FOR SPOTIFY
def access_token():
    try:
    #combine client id and secret (itcan be applied only when it os single  string)
        credentials= f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response= requests.post(
            url='https://accounts.spotify.com/api/token',
            headers= {'Authorization': f'Basic {encoded_credentials}'},
            data= {'grant_type': 'client_credentials'}
        )  
        # print(response) 
#uRL IS data HIS IS  spotify's token endpoint the url where you requests access token
    #Headers are used to tell spotify who you are ,basic indicates we're using basic authendication
    #data informs spotify which authendication flow you are using, client_credentials means an app 
    #requesting access to public data(not user specific data)
        print("Token Generated Completely")
        return response.json()['access_token']
    except Exception as e:
        print('Error in Token Generation..',e)

access_token()

# latest release in spotify
def get_new_release(): 
    try:
        token = access_token()
        header = {'Authorization': f'Bearer {token}'}
        param = {'limit':50}
        response = requests.get(url='https://api.spotify.com/v1/browse/new-releases',
                           headers=header, params=param)
        print(response)
        if response.status_code == 200:
        #     print(response.json())
            data = response.json()
            release = []
            albums = data['albums']['items']
            for i in albums:
                a = {
                   'album_name':i['name'],
                   'Release_date':i['release_date']
             
                }
                print(a)
    except Exception as e:
        print('Error in latest release..',e)

get_new_release()