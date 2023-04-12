import socket
from message import *

# 连接服务器
host = '127.0.0.1'
port = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# 发送玩家姓名
player_name = input('请输入您的姓名：')
name_message = NameMessage(player_name)
sock.send(name_message.pack())

# 接收玩家颜色和游戏状态
while True:
    message_type, message_body = receive_message(sock)
    if message_type == MessageType.START:
        start_message = StartMessage.unpack(message_body)
        print(f'您执{start_message.color}方')
        break
    elif message_type == MessageType.ERROR:
        error_message = ErrorMessage.unpack(message_body)
        print(f'错误：{error_message.message}')

# 开始游戏循环
while True:
    # 等待对手落子
    message_type, message_body = receive_message(sock)
    if message_type == MessageType.MOVE:
        move_message = MoveMessage.unpack(message_body)
        print(f'{move_message.src} -> {move_message.dest}')
    elif message_type == MessageType.END:
        end_message = EndMessage.unpack(message_body)
        print(f'游戏结束，胜利者是{end_message.winner}')
        break
    elif message_type == MessageType.ERROR:
        error_message = ErrorMessage.unpack(message_body)
        print(f'错误：{error_message.message}')

    # 玩家落子
    src = int(input('请输入起始位置：'))
    dest = int(input('请输入目标位置：'))
    move_message = MoveMessage(src, dest)
    sock.send(move_message.pack())

# 关闭网络连接
sock.close()

