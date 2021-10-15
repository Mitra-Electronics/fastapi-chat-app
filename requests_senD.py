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

name_change = dumps({"full_name": "Ishan Mitra",
                     "gender": "female",
                    "email": "ishanmitra020@gmail.com",
                     "profile_pic_url": "http://cloudinary.com",
                     "recovery_email":"ishanmitra020@gmail.com"})

login_json = dumps(login_json)
change_json = dumps(change_json)

register_json = dumps({
      "username": "string2",
      "email": "user@example.com",
      "full_name": "string",
      "disabled": False,
      "password": "string",
      "profile_pic_url": "http://cloudinary.com",
      "gender": "male",
      "recovery_email":"ishanmitra020@gmail.com"
      })

print(sess.post("http://127.0.0.1:8000/register", data=register_json,
                  headers={"Content-Type": "application/json"}).text)

res = sess.post("http://127.0.0.1:8000/login", data=login_json,
                headers={"Content-Type": "application/json"}, allow_redirects=True).text

print(res)#

token = loads(res)['access_token']

print(sess.get("http://127.0.0.1:8000/users/me", headers={
      'Authorization': f'Bearer {token}'}, allow_redirects=True).text)

print(sess.post("http://127.0.0.1:8000/users/me/change-password", data=change_json,
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

print(sess.post("http://127.0.0.1:8000/users/me/change", data=name_change,
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

"""print(sess.post("http://127.0.0.1:8000/users/me/delete-user",
     headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)"""

