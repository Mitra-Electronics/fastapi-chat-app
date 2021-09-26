from requests import session
from json import loads

sess = session()

res = sess.post("http://127.0.0.1:8000/login", data="grant_type=&username=string&password=pass&scope=&client_id=&client_secret=",
      headers={"content-type": "application/x-www-form-urlencoded"}, allow_redirects=True).text

print(res)

token = loads(res)['access_token']

print(sess.get("http://127.0.0.1:8000/users/me", headers={"content-type": "application/x-www-form-urlencoded",
      'Authorization': f'Bearer {token}'}, allow_redirects=True).text)
