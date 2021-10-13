from requests import session
from json import loads, dumps

sess = session()
login_json = {
    "username": "string2",
    "password": "string"
}

change_json = {
    "password": "string"
}

name_change = dumps({"full_name":"Ishan Mitra"})

login_json = dumps(login_json)
change_json = dumps(change_json)

register_json = dumps({
    "username": "string2",
    "email": "user@example.com",
    "full_name": "string",
    "disabled": False,
    "password": "string",
    "profile_pic_url": "http://cloudinary.com",
    "gender": "male"
})

print(sess.post("http://127.0.0.1:8000/register", data=register_json,
                headers={"Content-Type": "application/json"}).text)

res = sess.post("http://127.0.0.1:8000/login", data=login_json,
                headers={"Content-Type": "application/json"}, allow_redirects=True).text

print(res)

token = loads(res)['access_token']

print(sess.get("http://127.0.0.1:8000/users/me", headers={"content-type": "application/x-www-form-urlencoded",
      'Authorization': f'Bearer {token}'}, allow_redirects=True).text)

print(sess.post("http://127.0.0.1:8000/users/me/change-password", data=change_json,
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

print(sess.post("http://127.0.0.1:8000/users/me/change-name", data=name_change,
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

print(sess.post("http://127.0.0.1:8000/users/me/delete-user",
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

import httpx
from pathlib import Path
import asyncio

async def async_post_file_req(url: str, filepath: Path):    
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(write=None, read=None, connect=None, pool=None)) as client:
        r = await client.post(
            url, 
            files={
                'pic': (filepath.name, filepath.open('rb'), 'image/jpeg')
            },
            headers={
                'accept': 'application/json',
                'Content-Type': 'multipart/form-data',
            }
        )

if __name__ == '__main__':
    url = 'http://127.0.0.1:8000'
    asyncio.run(
        async_post_file_req(
            f'{url}/upload',            
            Path('Git logo.jpg')
    ))

"""register_json = dumps({
    "username": "string2",
    "email": "user@example.com",
    "full_name": "string",
    "disabled": False,
    "password": "string",
    "profile_pic_url": "http://cloudinary.com"
})

print(sess.post("http://127.0.0.1:8000/register", data=register_json,
                headers={"Content-Type": "application/json"}).text)"""
