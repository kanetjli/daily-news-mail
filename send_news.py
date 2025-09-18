import os, smtplib, requests, datetime
from email.mime.text import MIMEText

KEY = '89b89f6d8ca841ac98ad1dbe6af33d8b'
url = f'https://newsapi.org/v2/top-headlines?country=cn&apiKey={KEY}&pageSize=5'
data = requests.get(url, timeout=10).json()
titles = [n['title'] for n in data['articles']]
body = '今日国内头条：\n\n' + '\n'.join(f'• {t}' for t in titles)

msg = MIMEText(body, 'plain', 'utf-8')
msg['Subject'] = f'GitHub 每日新闻 {datetime.date.today()}'
msg['From'] = os.getenv('SMTP_USER')
msg['To'] = os.getenv('TO_MAIL')

with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as smtp:
    smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PWD'))
    smtp.send_message(msg)
print('邮件已发送!')
