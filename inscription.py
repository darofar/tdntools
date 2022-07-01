import getopt
import os
import sys
import time
import threading

import requests

from login import login

USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
JSESSIONID = os.getenv("JSESSION_ID")
INSCRIBE_URL = os.getenv("INSCRIBE_URL", "http://jornadas-tdn.org/virtual/ocupar")
LOGIN_URL = os.getenv("LOGIN_URL", "http://jornadas-tdn.org/j_spring_security_check")

# Class of different styles
COLORS = {
    'BLACK':        "\033[30m",
    'RED':          "\033[31m",
    'GREEN':        "\033[32m",
    'YELLOW':       "\033[33m",
    'BLUE':         "\033[34m",
    'MAGENTA':      "\033[35m",
    'CYAN':         "\033[36m",
    'WHITE':        "\033[37m",
    #    'UNDERLINE':    "\033[4m",
    #    'RESET':        "\033[0m",
    #    'END':          "\033[0m"
}
COLOR_END = "\033[0m"


class InscriptionError(Exception):
    pass


def get_color(count):
    return list(COLORS.values())[count % len(COLORS)]


def inscribe(jsessionid, count):
    color = get_color(count)
    print(f"{color}making requests {count}... {INSCRIBE_URL}{COLOR_END}")
    print(f"{color}JSESSIONID: {jsessionid}{COLOR_END}")
    r = requests.get(INSCRIBE_URL, cookies={'JSESSIONID': jsessionid}, timeout=2)
    print(r.text)
    if "error" in r.text.lower():
        print(f"{color}error... {COLOR_END}")
        return False
    if "lo sentimos" in r.text.lower():
        print(f"{color}still closed...{COLOR_END}")
        return False
    if "<title>login</title>" in r.text.lower():
        print(f"{color}JSESSIONID FAIL... change it!!!{COLOR_END}")
        return False
    if "enhorabuena" in r.text.lower():
        print(f"{color}¡¡¡DENTRO!!!{COLOR_END}")
        return True
    print(f"{color}WTF!!!{COLOR_END}")
    print(f"{color}{r.text}{COLOR_END}")
    print("\n\n")
    return False


def main(argv):
    user_name = USER_NAME
    password = PASSWORD
    jsessionid = JSESSIONID

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
            user_name = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-j", "--jsessionid"):
            jsessionid = arg

    if jsessionid is None and (user_name is None or password is None):
        raise InscriptionError("You must provide user_name/password or jsessionid.")

    print(f"username: {user_name}\npassword:{password}\njsessionid: {jsessionid}")

    if not jsessionid and (user_name and password):
        print("Trying to obtain a jsessionid")
        jsessionid = login(
            login_url=LOGIN_URL,
            user_name=user_name,
            password=password
        )
        print(f"JSESSIONID obtained: {jsessionid}")

    if not jsessionid:
        print("ERROR: Need jsessionid!")
        sys.exit(2)
    count = 1
    while True:
        thread = threading.Thread(target=inscribe, args=(jsessionid, count,))
        thread.start()
        count += 1
        time.sleep(0.5)


if __name__ == "__main__":
    main(sys.argv[1:])
