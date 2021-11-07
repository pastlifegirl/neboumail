#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import base64
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate

# ここに設定を書く
FROM_NAME = "koganei matsuri <xxx@mail.com>"
MAIL_HOST = "mail.server.ne.jp"
USERNAME = "xxx@mail.com"
PASSWORD = "password"

if len(sys.argv) != 4:
  print("Usage: sendmail.py [target] [title] [content]")
  sys.exit()

main_text = sys.argv[3]
charset = "utf-8"
if charset == "utf-8":
    msg = MIMEText(main_text, "plain", charset)
elif charset == "iso-2022-jp":
    msg = MIMEText(base64.b64encode(main_text.encode(charset, "ignore")), "plain", charset)

msg.replace_header("Content-Transfer-Encoding", "base64")
msg["Subject"] = sys.argv[2]
msg["From"] = FROM_NAME
msg["To"] = sys.argv[1]
msg["Cc"] = ""
msg["Bcc"] = ""
msg["Date"] = formatdate(None,True)

nego_combo = ("starttls", 587) # メールサーバーによっては通信方式を変える

if nego_combo[0] == "no-encrypt":
    smtpclient = smtplib.SMTP(MAIL_HOST, nego_combo[1], timeout=10)
elif nego_combo[0] == "starttls":
    smtpclient = smtplib.SMTP(MAIL_HOST, nego_combo[1], timeout=10)
    smtpclient.ehlo()
    smtpclient.starttls()
    smtpclient.ehlo()
elif nego_combo[0] == "ssl":
    context = ssl.create_default_context()
    smtpclient = smtplib.SMTP_SSL(MAIL_HOST, nego_combo[1], timeout=10, context=context)
smtpclient.set_debuglevel(2)

smtpclient.login(USERNAME, PASSWORD)

smtpclient.send_message(msg)
smtpclient.quit()