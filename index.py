import base64
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv('.env')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# CREATE A TOKEN FOR SPOTIFY
def access_token():
    try:
        # combine client id and secret
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"

        encoded_credentials = base64.b64encode(
            credentials.encode()
        ).decode()

        response = requests.post(
            url='https://accounts.spotify.com/api/token',

            # ✅ FIXED HEADER
            headers={
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },

            data={'grant_type': 'client_credentials'}
        )

        # ✅ DEBUG RESPONSE
        print(response.status_code)
        print(response.text)

        # ✅ CHECK TOKEN SUCCESS
        if response.status_code == 200:
            print("Token Generated Completely")
            return response.json()['access_token']
        else:
            print("Token Generation Failed")

    except Exception as e:
        print('Error in Token Generation..', e)

access_token()

# latest release in spotify
def get_new_release():

    try:
        token = access_token()

        header = {
            'Authorization': f'Bearer {token}'
        }

        param = {
            'limit': 50
        }

        response = requests.get(
            url='https://api.spotify.com/v1/browse/new-releases',
            headers=header,
            params=param
        )

        # ✅ DEBUG RESPONSE
        print(response.status_code)
        print(response.text)

        if response.status_code == 200:

            data = response.json()

            albums = data['albums']['items']

            for album in albums:

                print(album)

                # ✅ FIXED external_urls SPELLING
                info = {
                    'album_name': album['name'],
                    'artist_name': album['artists'][0]['name'],
                    'release_date': album['release_date'],
                    'album_type': album['album_type'],
                    'total_tracks': album['total_tracks'],
                    'spotify_url': album['external_urls']['spotify'],
                    'album_image': album['images'][0]['url'] if album['images'] else None
                }

                print(json.dumps(info,indent=2))

    except Exception as e:
        print('Error in latest release..', e)

get_new_release()