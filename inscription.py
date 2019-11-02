import getopt
import os
import sys
import time
import threading

import requests

from login import login

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
jsession_id = os.getenv("JSESSION_ID")
inscribe_url = os.getenv("INSCRIBE_URL", "http://jornadas-tdn.org/virtual/ocupar")
login_url = os.getenv("LOGIN_URL", "http://jornadas-tdn.org/j_spring_security_check")


def inscribe(jsession_id, count):
    print(f"making requests {count}... {inscribe_url}")
    print(f"JSESSIONID: {jsession_id}")
    r = requests.get(inscribe_url, cookies={'JSESSIONID': jsession_id}, timeout=2)
    # print(r.text)
    if "error" in r.text.lower():
        print("error... ")
        return False
    if "lo sentimos" in r.text.lower():
        print("still closed...")
        return False
    if "<title>login</title>" in r.text.lower():
        print("JSESSIONID FAIL... change it!!!")
        return False
    if "enorabuena" in r.text.lower():
        print("¡¡¡DENTRO!!!")
        return True
    print("WTF!!!")
    print(r.text)
    print("\n\n")
    return False


def main(argv):
    global username, password, jsession_id
    try:
        opts, args = getopt.getopt(argv, "hu:p:j:", ["username=", "password=", "jsessionid="])
    except getopt.GetoptError:
        print('inscription.py -u <username> -p <password> -j <jsessionid>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('inscription.py -u <username> -p <password> -j <jsessionid>')
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-j", "--jsessionid"):
            jsession_id = arg

    print(f"username: {username}\npassword:{password}\njsessionid: {jsession_id}")

    if not jsession_id and (username and password):
        print("Trying to obtain a jsessionid")
        jsession_id = login(
            login_url=login_url,
            user_name=username,
            password=password
        )
        print(f"JSESSIONID obtained: {jsession_id}")

    if not jsession_id:
        print("ERROR: Need jsessionid!")
        sys.exit(2)
    count = 1
    while True:
        thread = threading.Thread(target=inscribe, args=(jsession_id, count, ))
        thread.start()
        count += 1
        time.sleep(0.5)


if __name__ == "__main__":
    main(sys.argv[1:])
