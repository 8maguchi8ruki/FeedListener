import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

def send(name,email,text):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login('feedlyreadly2021@gmail.com','F11d2021')

    msg = MIMEText(text)
    msg['Subject'] = name
    msg['From'] = email
    msg['To'] = 'feedlyreadly2021@gmail.com'
    msg['Date'] = formatdate()
    print(msg)
    smtpobj.sendmail(email, "feedlyreadly2021@gmail.com", msg.as_string())
    smtpobj.close()
    database.contact_user(name,email,text)