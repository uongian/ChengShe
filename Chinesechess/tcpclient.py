import socket
import pygame

# 服务端的IP地址和端口号
HOST = '127.0.0.1'  # 这里假设服务端运行在本机上
PORT = 6666

# 初始化Pygame
pygame.init()

# 设置屏幕大小和标题
screen_width, screen_height = 750, 667
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("中国象棋")

# 加载棋盘图片
board_image = pygame.image.load("images/bg.png")

# 加载棋子图片
chess_images = {
    "r_c": pygame.image.load("images/r_c.png"),
    "r_m": pygame.image.load("images/r_m.png"),
    "r_x": pygame.image.load("images/r_x.png"),
    "r_s": pygame.image.load("images/r_s.png"),
    "r_j": pygame.image.load("images/r_j.png"),
    "r_p": pygame.image.load("images/r_p.png"),
    "b_c": pygame.image.load("images/r_p.png"),
    "b_m": pygame.image.load("images/b_m.png"),
    "b_x": pygame.image.load("images/b_x.png"),
    "b_s": pygame.image.load("images/b_s.png"),
    "b_j": pygame.image.load("images/b_j.png"),
    "b_p": pygame.image.load("images/b_p.png"),
    "b_z": pygame.image.load("images/b_z.png"),
    "r_z": pygame.image.load("images/r_z.png"),
    "": None,  # 空格子对应的棋子图片为None
}

# 字体设置
font = pygame.font.SysFont("simhei", 20)

# 创建一个socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 建立连接
client_socket.connect((HOST, PORT))

# 发送消息
client_socket.sendall(b'Hello, World!')

# 接收消息
data = client_socket.recv(1024)

# 解析接收到的数据
board = eval(data.decode())
print(board)

# 发送消息
client_socket.sendall(b'Hello, World!')

# 关闭连接
client_socket.close()

# 画棋盘
screen.blit(board_image, (0, 0))

# 画棋子
for i in range(10):
    for j in range(9):
        piece = board[i][j]
        if piece != "":
            piece_image = piece_images[piece]
            piece_rect = piece_image.get_rect()
            piece_rect.topleft = (60 + j * 57 - piece_rect.width // 2, 60 + i * 57 - piece_rect.height // 2)
            screen.blit(piece_image, piece_rect)

# 刷新屏幕
pygame.display.flip()

# 游戏循环
while True:
    pygame.time.delay(100)  # 添加延迟，降低CPU使用率

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # 点击关闭按钮退出游戏

