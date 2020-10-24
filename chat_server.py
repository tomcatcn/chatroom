# 功能 ： 类似qq群功能
# 【1】 有人进入聊天室需要输入姓名，姓名不能重复
# 【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
# 【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
# 【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
# 【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx

import socket

#全局变量
HOST = '0.0.0.0'
PORT = 8845
ADDR =(HOST,PORT)

#用户资料,字典保持，方便查找
users = {} #{username:address}

#通知所有人
def send_all(s,msg):
    for name,addr in users.items():
        s.sendto(msg.encode(), addr)

#进入聊天室
def log_in(s,name,addr):
    #如果用户在用户列表内，则给全部人发发提示信息
    if name in users:
        for user in users:
            msg = name+'进入了聊天室'
            send_all(s,msg)
    # 用户不在用户列表内，则添加进列表，并通知所有人，返回用户注册成功
    users[name] = addr
    #返回用户注册成功
    s.sendto(b'rigster success',addr)


#与所有人聊天
def chat_all(s,msg,addr):

    #根据地址匹配用户姓名
    for username,address in users.items():
        #找到用户匹配地址
        if address == addr:
            chat_msg = username + ':' + msg
            send_all(s,chat_msg)
            break


#退出
def quit(s,addr):

    # 根据地址匹配用户姓名
    for username, address in users.items():
        if address == addr:
            msg = username + ':' '退出'
            send_all(s, msg)
            # 给用户发信息，让客户端父进程退出
            s.sendto(b'EXIT', addr)
            # 给所有用户发送退出
            send_all(s, msg)
            break



#处理请求
def handle(s,data,addr):
    data = data.decode()
    #消息头
    head = data.split(' ')[0]
    #数据
    msg = data.split(' ')[1]
    #进入聊天室
    if head == 'L':
        log_in(s,msg,addr)
    #聊天
    elif head == 'S':
        chat_all(s,msg,addr)
    #退出
    elif head == 'quit':
        quit(s,addr)


def main():
    #搭建网络
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(ADDR)
    while True:
        print('waiting')
        data,addr = s.recvfrom(1024)
        print(data,addr)
        handle(s,data,addr)

if __name__ == '__main__':
    main()
