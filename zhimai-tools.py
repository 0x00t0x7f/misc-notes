import smtplib
import random
import string
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up email server and login credentials\
smtp_server = 'smtp.qq.com'
smtp_port = 587
smtp_username = 'your_email@qq.com'
smtp_password = 'secret'


# 生成验证码
def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# 创建简单邮件正文
def create_email(sender, receiver, subject, body):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    return message


# 发送邮件
def send_email(sender, receiver, message):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, message.as_string())
        print("验证码发送成功!")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False
    finally:
        server.quit()


# 校验发送验证码
def verify_code(user_code, generated_code, expiration_time):
    if user_code == generated_code and datetime.now() < expiration_time:
        return True
    return False


class EmailVerification:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.verification_code = None
        self.expiration_time = None

    def generate_code(self, length=6):
        self.verification_code = generate_verification_code(length)
        self.expiration_time = datetime.now() + timedelta(minutes=5)
        return self.verification_code

    def send_verification_email(self, receiver_email):
        subject = "职麦AI注册邮箱验证码"
        body = f"感谢您注册职麦AI，您的邮箱验证码是: {self.verification_code}\n将于10分钟后过期。"
        message = create_email(self.smtp_username, receiver_email, subject, body)
        return send_email(self.smtp_username, receiver_email, message)

    def verify_code(self, user_code):
        if self.verification_code is None:
            return False
        return verify_code(user_code, self.verification_code, self.expiration_time)


# 调用示例
# 创建EmailVerification实例
email_verification = EmailVerification(smtp_server, smtp_port, smtp_username, smtp_password)

# 生成验证码
verification_code = email_verification.generate_code()

# 发送验证码邮件
receiver_email = 'noreply@zhimai.com'
email_verification.send_verification_email(receiver_email)

# 验证用户输入的验证码
