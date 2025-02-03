import requests, json, re, os

session = requests.session()
# 配置用户名（一般是邮箱）
# email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
# passwd = os.environ.get('PASSWD')
# 从设置的环境变量中的Variables多个邮箱和密码 ,分割
emails = os.environ.get('EMAIL', '').split(',')
passwords = os.environ.get('PASSWD', '').split(',')

# server酱
SCKEY = os.environ.get('SCKEY')
# PUSHPLUS
Token = os.environ.get('TOKEN')
def push(content):
    if SCKEY and SCKEY != '1':
        url = f"https://sctapi.ftqq.com/{SCKEY}.send?title=ikuuu签到&desp={content}"
        response = requests.post(url)
        print(f'推送完成: {response.text}')
    elif Token != '1':
        headers = {'Content-Type': 'application/json'}
        data = {"token": Token, 'title': 'ikuuu签到', 'content': content, "template": "json"}
        response = requests.post(f'http://www.pushplus.plus/send', json=data, headers=headers).json()
        print(f'push+推送成功' if response['code'] == 200 else f'push+推送失败: {response}')
    else:
        print('未使用消息推送推送！')

# 会不定时更新域名，记得Sync fork

login_url = 'https://ikuuu.one/auth/login'
check_url = 'https://ikuuu.one/user/checkin'
info_url = 'https://ikuuu.one/user/profile'

header = {
        'origin': 'https://ikuuu.one',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

for email, passwd in zip(emails, passwords):
    session = requests.session()
    data = {
        'email': email,
        'passwd': passwd
    }
    try:
        print(f'[{email}] 进行登录...')
        response = json.loads(session.post(url=login_url,headers=header,data=data).text)
        print(response['msg'])
        # 获取账号名称
        # info_html = session.get(url=info_url,headers=header).text
        # info = "".join(re.findall('<span class="user-name text-bold-600">(.*?)</span>', info_html, re.S))
        # 进行签到
        result = json.loads(session.post(url=check_url,headers=header).text)
        print(result['msg'])
        content = result['msg']
        # 进行推送
        push(content)
    except:
        content = '签到失败'
        print(content)
        push(content)
