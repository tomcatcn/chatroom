import socket
import os
import sys
import signal

#信号处理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

HOST = '127.0.0.1'
PORT = 8845
ADDR =(HOST,PORT)

#负责发消息的子程序
def chat(s):
    while True:
        msg = input('聊天：')
        #退出
        if msg =='quit':
            msg = msg + ' '+'xxxx'
            s.sendto(msg.encode(),ADDR)
            break
        #发送聊天信息
        msg = 'S' + ' ' +msg
        s.sendto(msg.encode(),ADDR)

#父进程负责接受消息
def room(s):
    while True:
        data,addr = s.recvfrom(1024)
        if data == b'EXIT':
            sys.exit('聊天室退出')

        print(data.decode())




def main():
    #初始化，udp
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #循环接受，进入聊天室
    while True:
        #登录
        msg = input('name:')
        msg = 'L'+' '+msg
        s.sendto(msg.encode(),ADDR)
        data,addr = s.recvfrom(1024)
        #如果登录成功，进入聊天室
        if data == b'rigster success':
            #聊天室,不断收发
            print('进入聊天室成功')
            break
        else:
            print('用户名重复，请重新输入')
    #聊天室，创建子进程
    pid = os.fork()
    if pid < 0:
        os._exit(3)
    elif pid == 0:
        #子程序负责发消息
        chat(s)
    else:
        # 父程序负责接受消息
        room(s)

if __name__ == '__main__':
    main()


