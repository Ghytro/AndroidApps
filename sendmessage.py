import pymysql
from pymysql.cursors import DictCursor

chat_id = int(input("Chat id: "))
text = str(input("Message text: "))
attachment = str(input("Attachment source: "))
sender_id = int(input("Sender id: "))

connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')
with connection:
    cur = connection.cursor()
    cur.execute("INSERT INTO Chat" + str(chat_id) + "messages (message_text, attachmentpic_source, sender_id) values('" + text + "', '" + attachment + "', " + str(sender_id) + ")")

connection.close()
