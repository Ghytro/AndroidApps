import pymysql
from pymysql.cursors import DictCursor

chatname = str(input("Chat name: "))
avatar_source = str(input("Avatar source: "))

print("Input members (last member - NULL)")

username = int(input())
members = []

while username != 0:
    members.append(username)
    username = int(input())

connection = pymysql.connect(host='localhost', user='root', password='123', db='python_chat', charset='utf8mb4')

with connection:
    cur = connection.cursor()
    try:
        req = cur.execute("SELECT * FROM ChatInfo")
    except pymysql.err.ProgrammingError:
        cur.execute("CREATE TABLE `ChatInfo`(`id` INT NOT NULL AUTO_INCREMENT, `name` VARCHAR(256) NOT NULL, `avatar_source` VARCHAR(256) NOT NULL, `creation_date` DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`))")
    
    query = "INSERT INTO ChatInfo (name, avatar_source) values('" + chatname + "', '" + avatar_source + "')"
    cur.execute(query)
    cur.execute("SELECT MAX(`id`) FROM `ChatInfo`")
    chatID = cur.fetchone()[0]

    cur.execute("CREATE TABLE `Chat" + str(chatID) + "members`(`user_id` INT NOT NULL, PRIMARY KEY (`user_id`))")
    for i in members:
        cur.execute("INSERT INTO Chat" + str(chatID) + "members (user_id) values ('" + str(i) + "')")
        cur.execute("INSERT INTO MainScreen" + str(i) + " (chat_id) values (" + str(chatID) + ")")

    cur.execute("CREATE TABLE `Chat" + str(chatID) + "messages`(`id` INT NOT NULL AUTO_INCREMENT, `messagetext` TEXT NOT NULL, `attachmentpic_source` VARCHAR(256) NOT NULL, `sender_id` INT NOT NULL, `sendtimedate` DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`))")

connection.close()
