from requests import session

sess = session()

print(sess.post("http://127.0.0.1:8000/token", data="grant_type=&username=johndoe&password=secret&scope=&client_id=&client_secret=",
      headers={"content-type": "application/x-www-form-urlencoded"}, allow_redirects=True).text)

print(sess.get("http://127.0.0.1:8000/users/me", headers={"content-type": "application/x-www-form-urlencoded",
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjMyNDE2OTA2fQ.pFKwNgNYU71kKyFOG_vWmSYbw5xvl6iw0CIQSvCv65s'}, allow_redirects=True).text)
