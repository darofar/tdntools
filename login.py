import requests


class LoginError(Exception):
    pass


def login(login_url, user_name, password):
    print(f"Login on {login_url} for \nuser_name: {user_name}\npassword: {password}")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"
    }
    payload = {
        'j_username': user_name,
        'j_password': password
    }
    r = requests.post(login_url, data=payload, headers=headers)
    if not 'JSESSIONID' in r.request._cookies or not r.request._cookies.get('JSESSIONID'):
        message = f"response status: {r.status_code}\nresponse text: {r.text}"
        raise LoginError(f"Cannot login into the application\n{message}")
    return r.request._cookies.get('JSESSIONID')
