import os, smtplib, requests, datetime
from email.mime.text import MIMEText

# --- 邮件配置和内容 ---
subject = f'GitHub 每日新闻 {datetime.date.today()}'
body = ""

# --- 新闻获取 ---
try:
    KEY = 'a1972d21bb604c15b54a07b7c491c6cd'
    url = 'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=' + KEY + '&pageSize=5'
    response = requests.get(url, timeout=10)
    response.raise_for_status() # 如果状态码不是200，则抛出异常
    data = response.json()

    if data.get('status') == 'ok':
        lines = []
        for n in data['articles']:
            lines.append(f'• {n["title"]}')
            lines.append(f'  阅读原文：{n["url"]}')
        body = 'BBC 今日头条：\n\n' + '\n'.join(lines)
        print("成功获取新闻。")
    else:
        # API 返回了非 'ok' 状态
        error_message = data.get('message', '未知API错误')
        body = f"获取新闻失败，NewsAPI返回错误：{error_message}"
        print(f"获取新闻失败：{error_message}")

except requests.exceptions.RequestException as e:
    # 处理网络请求错误，如超时、DNS解析失败等
    body = f"获取新闻失败，网络请求异常：{e}"
    print(f"网络请求异常：{e}")

except Exception as e:
    # 处理所有其他未预料的错误
    body = f"获取新闻时发生未知错误：{e}"
    print(f"获取新闻时发生未知错误：{e}")


# --- 邮件发送 ---
try:
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = os.getenv('SMTP_USER')
    msg['To'] = os.getenv('TO_MAIL')

    with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as smtp:
        smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PWD'))
        smtp.send_message(msg)
    print("邮件已发送！")
except Exception as e:
    print(f"邮件发送失败，请检查邮件配置：{e}")
