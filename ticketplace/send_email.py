import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail Sign In
import threading

sender = 'help@ticketplace.net'
gmail_server = 'smtp.gmail.com'
port = 587
gmail_passwd = 'h@110w0r1d'


def send_email(to, subject, text, html=False):
    """
    이메일을 보냄
    쓰레딩을 사용해서 unblocking 작동한다.
    :param to: 이메일 보낼 주소
    :param subject: 이메일 제목
    :param text: 이메일 내용
    :param html: html내용. 주어질 경우 MIMEType이 HTML이메일로 변경
    """
    def send_email_threaded(to, subject, text, html):

        # smtp 서버 로그인
        server = smtplib.SMTP(gmail_server, port)
        server.ehlo()
        server.starttls()
        server.login(sender, gmail_passwd)

        # MIME 타입 설정
        if html:
            msg = MIMEMultipart('alternative')
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
        else:
            msg = MIMEText(text, 'plain')

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to

        try:
            server.sendmail(sender, [to], msg.as_string())
            print('email sent to %s' % to)
        except:
            print('error sending mail :')

        server.quit()

    # Spawn nonblocking thread
    thread = threading.Thread(target=send_email_threaded, args=(to, subject, text, html))
    thread.start()
