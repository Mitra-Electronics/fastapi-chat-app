from requests import session
from json import loads, dumps

sess = session()
login_json = {
    "username": "string",
    "password": "password"
}

change_json = {
    "password": "password"
}

res = sess.post("http://127.0.0.1:8000/login", data=dumps(login_json),
                headers={"Content-Type": "application/json"}, allow_redirects=True).text

print(res)

token = loads(res)['access_token']

print(sess.get("http://127.0.0.1:8000/users/me", headers={"content-type": "application/x-www-form-urlencoded",
      'Authorization': f'Bearer {token}'}, allow_redirects=True).text)

print(sess.post("http://127.0.0.1:8000/users/me/change-password", data=dumps(change_json),
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)
