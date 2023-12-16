#credits: devislunar#0 & mooncrusherrr#0

try:
    import requests
    import os
    import rapidjson as json
    import asyncio
    import time
    from colorama import Fore, Style
    from functools import cache

except ModuleNotFoundError:
   print('Módulos ainda não instalados...\ninstalando agora...')
   os.system('pip install requests python-rapidjson colorama functools')

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# check version
requests.packages.urllib3.disable_warnings()
version = '1.3.0'
response = requests.get('https://pastebin.com/raw/rjHPdkHN').text

if response != version:
    print(Fore.LIGHTRED_EX, f'[{response}] New version, please update :p', Style.RESET_ALL)
    exit(0)
else:
    print(Fore.LIGHTBLACK_EX, 'Starting Grimm Sniper..', Style.RESET_ALL)

# Files
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except:
    exit(Fore.LIGHTBLACK_EX, 'Something went wrong while reading bytes...', Style.RESET_ALL)

# other stuff
title = f"""  ▄████  ██▀███   ██▓ ███▄ ▄███▓ ███▄ ▄███▓
 ██▒ ▀█▒▓██ ▒ ██▒▓██▒▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒
▒██░▄▄▄░▓██ ░▄█ ▒▒██▒▓██    ▓██░▓██    ▓██░
░▓█  ██▓▒██▀▀█▄  ░██░▒██    ▒██ ▒██    ▒██ 
░▒▓███▀▒░██▓ ▒██▒░██░▒██▒   ░██▒▒██▒   ░██▒
 ░▒   ▒ ░ ▒▓ ░▒▓░░▓  ░ ▒░   ░  ░░ ▒░   ░  ░
  ░   ░   ░▒ ░ ▒░ ▒ ░░  ░      ░░  ░      ░
░ ░   ░   ░░   ░  ▒ ░░      ░   ░      ░   
      ░    ░      ░         ░          ░   
                                           \nGrimm's Sniper | v{version}"""

@cache
class Snipe: # sniper
    def __init__(self):
        # Init data
        self.accname = 'N/A'
        self.item_index = 0
        self.item_name = 'N/A'
        self.productId = 0
        self.task = 'N/A'
        self.speed = 0
        self.buys = 0
        self.total_errors = 0
        self.clear = 'cls' if os.name == 'nt' else 'clear'

    def get_username(self, cookie):
        headers = {
        "Cookie": f".ROBLOSECURITY={cookie}"
    }
        response = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers, verify=True)
        data = response.json()
        if 'name' in data:
            name = data['name']
            self.accname = name
        else:
            print(Fore.LIGHTRED_EX, '[TokenError] Provide a valid token.', Style.RESET_ALL)
            exit(0)

    async def get_xcsrf_token(self, cookie):
        headers = {
            "Cookie": f".ROBLOSECURITY={cookie}"
        }
        res = requests.post('https://auth.roblox.com/v1/usernames/validate', headers=headers, verify=True)
        csrftoken = res.headers['x-csrf-token']
        return csrftoken

    async def buy_item_v1(self, cookie, csrf, bundleid):
        try:
            time = asyncio.get_event_loop().time()
            print(Fore.LIGHTRED_EX, f"Buying {self.item_name}...", Style.RESET_ALL)
            csrf = await self.get_xcsrf_token(config['accounts']['token'])
            headers = {
            "Cookie": f".ROBLOSECURITY={cookie}",
            "x-csrf-token": csrf
           }
            payload = {
            "expectedCurrency": 1,
            "expectedPrice": 0,
            "expectedSellerId": 1,
            }
            while True:
                await asyncio.sleep(config['MISC']['SPEED'][0], config['MISC']['SPEED'][1])
                res = requests.post(f'https://economy.roblox.com/v1/purchases/products/{self.productId}', headers=headers, data=payload, verify=True)

                if res.status_code == 200:
                    if 'reason' in res.json() and res.json()['reason'] == 'AlreadyOwned':
                        print(res.json()['errorMsg'], flush=True)
                        await asyncio.sleep(0, 5)
                        self.item_index += 1
                        break
                    if 'purchased' in res.json() and res.json()['purchased'] == True:
                        print(Fore.LIGHTBLACK_EX, 'Bought new item!', Style.RESET_ALL, flush=True)
                        await asyncio.sleep(0, 5)
                        self.buys += 1
                        self.item_index += 1
                        break
                else:
                    if 'errors' in res.json() and res.json()['errors'][0]['code'] == 0:
                        print(Fore.LIGHTRED_EX, f'[RateLimit] Evitando ratelimit...', Style.RESET_ALL, flush=True)
                        self.total_errors += 1
                        await asyncio.sleep(30)
                        break
                    if 'errors' in res.json() and res.json()['errors'][0]['code'] == 27:
                        print(Fore.LIGHTRED_EX, f'[RateLimit] Evitando ratelimit...', Style.RESET_ALL, flush=True)
                        self.total_errors += 1
                        await asyncio.sleep(30)
                        break
        except Exception as e:
            print(e, flush=True)
            self.total_errors += 1
            await asyncio.sleep(0, 1)
        self.speed = round(asyncio.get_event_loop().time() - time, 3)

    async def update_stats(self) -> None:
        print(Fore.RED + title +Style.RESET_ALL, flush=True)
        print('╰┈➤ accounts: ',  Fore.LIGHTBLACK_EX, f'[ {self.accname} ]', Style.RESET_ALL, '\n╰┈➤ buys: ', Fore.LIGHTBLACK_EX, f'[ {self.buys} ]', Style.RESET_ALL, '\n╰┈➤ task: ', Fore.LIGHTBLACK_EX, f'[ {self.task} ]', Style.RESET_ALL, '\n╰┈➤ speed: ', Fore.LIGHTBLACK_EX, f'[ {self.speed} ]', Style.RESET_ALL, '\n╰┈➤ errors: ', Fore.LIGHTBLACK_EX, f'[ {self.total_errors} ]', Style.RESET_ALL, flush=True)

    async def search_v2(self):
        self.task = 'Checking...'
        os.system(self.clear)
        await self.update_stats()

        cookie = config['accounts']['token']
        x_csrf_token = await self.get_xcsrf_token(cookie)

        cursor = ""
        while cursor is not None:
            while True:
                res = requests.get('https://catalog.roblox.com/v2/search/items/details', params={"Category": "Accessories", "Subcategory": 19, "Limit": 120, "MaxPrice": 0, "SortType": 6, "cursor": cursor}, verify=config['MISC']['SSL-VERIFY'])
                if res.status_code == 200:
                    items = res.json()['data']
                    total_items = len(items)
                                   
                    for i in range(self.item_index, total_items):
                        self.task = 'New buy started!'
                        self.productId = items[self.item_index]['productId']
                        self.item_name = items[self.item_index]['name']
                        await asyncio.sleep(0, 1)
                        os.system(self.clear)
                        await self.update_stats()
                        await self.buy_item_v1(cookie, x_csrf_token, items[i]['id'])
                        await self.update_stats()
                        if i == 119:
                            cursor = res.json()['nextPageCursor']
                            print(Fore.LIGHTBLACK_EX, f'current cursor: {cursor}', Style.RESET_ALL)
                            await asyncio.sleep(0, 1)
                            self.item_index = 0
                            continue
                        continue

    async def main(self) -> None:
        token = config['accounts']['token']
        os.system(self.clear)
        self.get_username(token)
        await self.update_stats()
        await self.search_v2()

asyncio.get_event_loop().run_until_complete(Snipe().main())