import os
import smtplib
import requests
import datetime
from email.mime.text import MIMEText

# --- 核心诊断逻辑 ---
# 邮件正文和主题，初始为空
body = ""
subject = ""
success = False # 标记新闻获取是否成功

try:
    # 步骤 1: 获取 NewsAPI Key
    # 这是一个硬编码的Key，因为您没有使用Secrets。
    # 强烈建议您使用 GitHub Secrets 来存储Key。
    key = 'a1972d21bb604c15b54a07b7c491c6cd'
    
    # 步骤 2: 构建并发送请求
    url = f'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={key}&pageSize=5'
    response = requests.get(url, timeout=15)
    
    # 步骤 3: 检查 HTTP 响应状态码
    response.raise_for_status() # 如果状态码不是200，则抛出异常
    data = response.json()
    
    # 步骤 4: 检查 NewsAPI 响应状态
    if data.get('status') == 'ok':
        lines = []
        for article in data['articles']:
            lines.append(f'• {article["title"]}')
            lines.append(f'  阅读原文：{article["url"]}')
        body = 'BBC 今日头条：\n\n' + '\n'.join(lines)
        subject = f'GitHub 每日新闻 {datetime.date.today()}'
        success = True
    else:
        # API 响应不是 'ok'
        error_message = data.get('message', '未知API错误')
        body = f"获取新闻失败，NewsAPI返回错误：\n{error_message}"
        subject = f'GitHub 每日新闻失败报告 {datetime.date.today()}'

except requests.exceptions.RequestException as e:
    # 请求异常，如网络连接问题或超时
    body = f"网络请求失败，请检查网络连接或URL：\n{e}"
    subject = f'GitHub 每日新闻失败报告 {datetime.date.today()}'

except Exception as e:
    # 捕获其他所有异常
    body = f"脚本运行时发生未知错误：\n{e}"
    subject = f'GitHub 每日新闻失败报告 {datetime.date.today()}'

# --- 发送邮件（无论是否成功获取新闻） ---
try:
    # 如果主体和正文在获取新闻时没有被设置，则设置默认值
    if not subject:
        subject = f'GitHub 每日新闻 {datetime.date.today()}'
    if not body:
        body = '脚本已成功运行，但未能获取新闻内容。'
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = os.getenv('SMTP_USER')
    msg['To'] = os.getenv('TO_MAIL')
    
    with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as smtp:
        smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PWD'))
        smtp.send_message(msg)
    
    print("邮件已发送！")
    
except Exception as e:
    print(f"邮件发送失败，请检查邮箱配置或权限：{e}")
