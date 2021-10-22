from json import dumps, loads

from requests import session

sess = session()
login_json = {
    "email": "user@example.com",
    "password": "string"
}

change_json = {
    "password": "string"
}

name_change = dumps({"full_name": "Ishan Mitra",
                     "gender": "female",
                     "email": "ishanmitra020@gmail.com",
                     "profile_pic_url": "http://cloudinary.com",
                     "recovery_email": "ishanmitra020@gmail.com"})

login_json = dumps(login_json)
change_json = dumps(change_json)

register_json = dumps({
    "email": "user@example.com",
    "full_name": "string",
    "disabled": False,
    "password": "string",
    "profile_pic_url": "http://cloudinary.com",
    "gender": "male",
    "recovery_email": "ishanmitra020@gmail.com"
})

print(sess.post("https://user-auth-ishan.herokuapp.com/register", data=register_json,
                headers={"Content-Type": "application/json"}).text)

res = sess.post("https://user-auth-ishan.herokuapp.com/login", data=login_json,
                headers={"Content-Type": "application/json"}, allow_redirects=True).text

print(res)

token = loads(res)['access_token']

print(sess.get("https://user-auth-ishan.herokuapp.com/users/me", headers={
      'Authorization': f'Bearer {token}'}, allow_redirects=True).text)

print(sess.post("https://user-auth-ishan.herokuapp.com/users/me/change-password", data=change_json,
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

print(sess.post("https://user-auth-ishan.herokuapp.com/users/me/change", data=name_change,
      headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)

"""print(sess.post("https://user-auth-ishan.herokuapp.com/users/me/delete-user",
     headers={"Content-Type": "application/json", 'Authorization': f'Bearer {token}'}).text)"""
