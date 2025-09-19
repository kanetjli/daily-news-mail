import os, smtplib, datetime
from email.mime.text import MIMEText

# 设置邮件内容
subject = f'GitHub Actions 测试邮件 {datetime.date.today()}'
body = '恭喜您！这封邮件是来自您的 GitHub Actions 自动化工作流的测试邮件。'

msg = MIMEText(body, 'plain', 'utf-8')
msg['Subject'] = subject
msg['From'] = os.getenv('SMTP_USER')
msg['To'] = os.getenv('TO_MAIL')

try:
    with smtplib.SMTP_SSL(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as smtp:
        smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PWD'))
        smtp.send_message(msg)
        print('测试邮件已发送！')
except Exception as e:
    print(f"邮件发送失败：{e}")
    # 您还可以将错误信息写入文件或直接打印到日志中，以便在 GitHub Actions 中查看
    with open("error.log", "w") as f:
        f.write(str(e))
