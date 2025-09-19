import os, smtplib, requests, datetime
from email.mime.text import MIMEText

KEY = '89b89f6d8ca841ac98ad1dbe6af33d8b'
url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=' + KEY + '&pageSize=5'

try:
    data = requests.get(url, timeout=10).json()

    # 检查API返回的'status'字段，确保成功
    if data.get('status') == 'ok':
        lines = []
        for n in data['articles']:
            lines.append(f'• {n["title"]}')
            lines.append(f'  阅读原文：{n["url"]}')
        body = 'BBC 今日头条：\n\n' + '\n'.join(lines)
    else:
        # 如果API返回错误信息，则将其作为邮件内容
        error_message = data.get('message', '未知API错误')
        body = f"获取新闻失败，NewsAPI返回错误：{error_message}"
        print(f"获取新闻失败：{error_message}")

except requests.exceptions.RequestException as e:
    # 处理网络请求错误
    body = f"获取新闻失败，网络请求异常：{e}"
    print(f"网络请求异常：{e}")

except Exception as e:
    # 处理其他所有可能的错误
    body = f"获取新闻时发生未知错误：{e}"
    print(f"未知错误：{e}")

# 构建并发送邮件
msg = MIMEText(body, 'plain', 'utf-8')
msg['Subject'] = f'GitHub 每日新闻 {datetime.date.today()}'
msg['From'] = os.getenv('SMTP_USER')
msg['To'] = os.getenv('TO_MAIL')

try:
    with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as smtp:
        smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PWD'))
        smtp.send_message(msg)
    print('邮件已发送!')
except Exception as e:
    print(f"邮件发送失败：{e}")
