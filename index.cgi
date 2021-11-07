#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import subprocess
import io,sys,os
os.environ["LANG"]="en_US.UTF-8"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/html\n\n")
print("<html>")
print("<head>")
print("<meta charset=\"utf-8\">")
print("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")

print("<title>寝坊メール送信</title>")
print("</head>")
print("<body>")
print("<h1><a href=\"?\">寝坊メール送信</a></h1>\n<hr>")

cgitb.enable()
cnt = 0
form = cgi.FieldStorage()

# 以下を環境に合わせて書き換え
input_key = r"PASSWORD"

default_target = "hogehoge@mail.com"
default_subject = "小金井です。本日時間給を取得します"
default_content = "私用のため。10時出社です"

file_path = "path_to_this_file/"
# ここまで

target = form.getvalue('target',"")
subject = form.getvalue('subject', "")
content = form.getvalue('content', "")
key = form.getvalue('key',"")

if target != "" and content != "" and subject != "":
	if key != input_key:
		print("キーが違います<hr>")
	else:
		subject = subject.encode('utf-8')
		content = content.encode('utf-8')
		cp = subprocess.run(["python3", file_path + "sendmail.py", target, subject, content], encoding='utf-8')
		if cp.returncode != 0:
			print(cp)
			print("<hr>")
		else:
			print("送信に成功しました<hr>")

print("<form action=\"?\" method=\"post\">")

print("宛先:<input type=\"text\" name=\"target\" size=\"50\" value=\"" + default_target + "\"><br>")
print("件名:<input type=\"text\" name=\"subject\" size=\"50\" value=\"" + default_subject + "\"><br>")
print("内容:<textarea name=\"content\" rows=\"5\" cols=\"60\">" + default_content + "</textarea><br>")
print("パス:<input type=\"password\" name=\"key\">")
print("<input type=\"submit\" value=\"送信\">")
print("</form>")

print("</body>\n</html>")
