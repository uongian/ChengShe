import socket

HOST = 'localhost'  # 这里用 localhost 表示本机 IP 地址
PORT = 8000  # 指定一个端口号，用于通信

# 创建一个 socket 对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定 socket 到本机 IP 地址和指定端口
server_socket.bind((HOST, PORT))

# 开始监听客户端的连接请求
server_socket.listen(2)  # 最多允许两个客户端连接

print('等待玩家连接...')

# 等待第一个客户端的连接请求
player1_socket, player1_addr = server_socket.accept()
print('玩家1已连接：', player1_addr)

# 等待第二个客户端的连接请求
player2_socket, player2_addr = server_socket.accept()
print('玩家2已连接：', player2_addr)

# 进入游戏循环
while True:
    # 玩家1发送消息给玩家2
    message_from_player1 = player1_socket.recv(1024)
    if message_from_player1:
        player2_socket.sendall(message_from_player1)

    # 玩家2发送消息给玩家1
    message_from_player2 = player2_socket.recv(1024)
    if message_from_player2:
        player1_socket.sendall(message_from_player2)