import os

if os.path.exists("Weibo_cookie.txt"):
    os.remove("Weibo_cookie.txt")

while True:
    cookie = input("请输入您要存储的cookie:\n")
    with open("Weibo_cookie.txt", "a", encoding="utf-8") as f:
        f.write(f"{cookie}\n")
    print("cookie存储完毕!")
    select = input("是否继续进行存储？  y/n\n")
    if select == 'n':
        break
