import requests
import json

# 脚本启动随机等待20-50秒
import time
import random
print('脚本等待启动...')
start_wait = random.randint(20, 50)
time.sleep(start_wait)
print( str(start_wait)+'秒后开始执行脚本')
print('开始执行')

# cookies字典 - 邮箱:cookie
cookies = {
    "6666669rr@gmail.com": "koa:sess=eyJ1c2VySWQiOjUyMjEzNCwiX2V4cGlyZSI6MTc4MDk4Njc5MjcxOCwiX21heEFnZSI6MjU5MjAwMDAwMDB9;koa:sess.sig=KNx-he9AzxJ4RhI0-aDFFsRXn8Y;"
}

# glados账号cookie检查
if not cookies:
    print('未获取到COOKIE变量')
    exit(0)


def start():    
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    for index, (email_key, cookie) in enumerate(cookies.items(), 1):
        print(f'正在处理第{index}个账号({email_key})...')
        try:
            checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
            state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
        #--------------------------------------------------------------------------------------------------------#
            if state.status_code == 200 and 'data' in state.json():
                days_left = state.json()['data']['leftDays']
                days_left = days_left.split('.')[0]
                actual_email = state.json()['data']['email']
                if 'message' in checkin.text:
                    mess = checkin.json()['message']
                    print(f'账号{index}({email_key})----{mess}----剩余({days_left})天')  # 日志输出
                    print(f'实际邮箱: {actual_email}')
                else:
                    print(f'账号{index}({email_key})----需要更新cookie')
            else:
                print(f'账号{index}({email_key})----获取状态失败，可能cookie已失效')
        except Exception as e:
            print(f'账号{index}({email_key})----处理失败: {str(e)}')
        print('-' * 50)

        # 如果不是最后一个账号，等待15-20秒再处理下一个
        if index < len(cookies):
            wait_time = random.randint(15, 20)
            print(f'等待{wait_time}秒后处理下一个账号...')
            time.sleep(wait_time)
     #--------------------------------------------------------------------------------------------------------#


def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()
