from bs4 import BeautifulSoup

import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
import os
from dotenv import load_dotenv
import certifi


load_dotenv()

def send_email_alert(subject, message):
    smtp_password = os.getenv("SMTP_NUMBER")
    qq_email = os.getenv("QQ_EMAIL")
    receiver = os.getenv("NOTIFY_EMAIL")

    # 打印调试信息
    print("调试信息：")
    print(f"发件人: {qq_email}")
    print(f"接收人: {receiver}")
    print(f"SMTP授权码是否存在: {'是' if smtp_password else '否'}")

    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = qq_email
    msg["To"] = receiver

    try:
        context = ssl.create_default_context(cafile=certifi.where())

        try:
            with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
                smtp.set_debuglevel(1)
                smtp.login(qq_email, smtp_password)
                smtp.sendmail(qq_email, [receiver], msg.as_string())
        except smtplib.SMTPResponseException as e:
            if e.smtp_code == -1 and e.smtp_error == b'\x00\x00\x00':
                print("⚠️ 邮件发送成功，但关闭连接时服务器返回了无效响应，可忽略。")
            else:
                raise e

    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    send_email_alert("测试通知", "这是一条来自Python脚本的测试邮件！")