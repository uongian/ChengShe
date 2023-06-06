
import sys

import socket
import pygame
import threading
from Chinesechess import *
pygame.init()

class ChessServe:

    def __init__(self, host="127.0.0.1", port=6666):
        pygame.init()
        self.screen = pygame.display.set_mode((750, 667))
        # ...
        self.chess_board = ChessBoard(self.screen)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.clients = []
        self.client_sockets = set()
        # 创建棋盘对象和游戏对象

        self.game = Game(self.screen)
        self.is_my_turn = True
       # self.position = None  # 添加 position 属性
       # self.Dot = Dot(self.screen, self.position)
        self.game.get_player(1)  # 1表示红方先行
        self.clients = []  # 客户端socket列表
        self.turn = 0  # 当前走棋方，0表示等待两名玩家加入，1表示红方先行，2表示黑方先行
        self.client_names = set()
        self.position = (0, 0)
        self.Dot=Dot(self.screen, self.position)
        self.clock = pygame.time.Clock()
        self.valid_moves = set()  # 初始化 valid_moves 属性为空集合
        self.ClickBox = ClickBox(screen, row, col, team)

    def start(self):
        # 开启服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 6688))
        server_socket.listen(2)
        print('等待两名玩家加入游戏...')
        while True:
            client_socket, address = server_socket.accept()
            print('有玩家加入游戏！')
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            if len(self.clients) == 2:
                # 两名玩家加入游戏，可以开始游戏了
                print('两名玩家已加入游戏，开始游戏！')
                self.turn = 1
                break

    def handle_client(self, client_socket):
        while True:
            try:
                # 接收客户端发来的数据
                data = client_socket.recv(1024)
                if data:
                    # 处理客户端的数据
                    self.process_data(client_socket, data)
                else:
                    # 客户端断开连接
                    self.clients.remove(client_socket)
                    client_socket.close()
                    print('有玩家退出游戏！')
                    break
            except:
                # 出现异常，关闭连接
                self.clients.remove(client_socket)
                client_socket.close()
                print('有玩家退出游戏！')
                break

    def process_data(self, conn, data):
        # 获取发送消息的客户端socket对象和昵称
#        client_socket, client_name = self.get_socket_name(client_socket=conn, client_name=data.decode())
        # 将接收到的消息发送给其他客户端
        if data == "generate_board":
            # 调用生成棋局的函数
            print("board")
            board = generate_board()
        for socket_, name in zip(self.client_sockets, self.client_names):
            if socket_ != client_socket:
                try:
                    socket_.sendall(f"{client_name}: {data}".encode())
                except:
                    # 如果发送消息失败，说明客户端已经断开连接，从列表中删除该客户端
                    index = self.client_sockets.index(socket_)
                    self.client_sockets.pop(index)
                    self.client_names.pop(index)
                    print(f"Client {name} disconnected.")
                    socket_.close()
            else:
                # 将接收到的消息发送给其他客户端
                for socket_, name in zip(self.client_sockets, self.client_names):
                    if socket_ != client_socket:
                        try:
                            socket_.sendall(f"{client_name}: {data}".encode())
                        except:
                            # 如果发送消息失败，说明客户端已经断开连接，从列表中删除该客户端
                            index = self.client_sockets.index(socket_)
                            self.client_sockets.pop(index)
                            self.client_names.pop(index)
                            print(f"Client {name} disconnected.")
                            socket_.close()



    def get_socket_name(self, client_socket, client_name):
        """获取客户端socket对象和昵称"""
        # 如果客户端socket不在列表中，则添加到列表中
        if client_socket not in self.client_sockets:
            self.client_sockets.add(client_socket)
            self.client_names.add(client_name)
        return client_socket, client_name

    def listen_server(self):
        """监听服务器端数据"""
        # 监听所有客户端的消息
        for client_socket, client_name in zip(self.client_sockets, self.client_names):
            try:
                # 接收客户端消息
                data = client_socket.recv(1024)
                if data:
                    self.process_data(client_socket, data)
            except ConnectionResetError:
                # 如果连接中断，从列表中移除该客户端的socket对象和昵称
                print(f"客户端{client_name}已经断开连接")
                self.client_sockets.remove(client_socket)
                self.client_names.remove(client_name)

    '''def send_to_client(self, client_socket, message):
        # 将消息转换为字符串并发送给客户端
        client_socket.sendall(str(message).encode())'''

    def run(self):
        print("等待客户端连接...")
        self.socket.listen()
        conn, addr = self.socket.accept()
        print(f"已连接客户端：{addr}")

        while True:
            # 接收客户端消息
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            self.process_data(conn, message)

            # 处理完消息后检查是否游戏结束
            '''if self.game.is_game_over():
                print("游戏结束")
                break'''

            # 监听键盘事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_my_turn:
                        pos = pygame.mouse.get_pos()
                        x, y = pos
                        row, col = self.chess_board.get_clicked_position(x, y)
                        clicked_chess = self.chess_board.get_chess_at(row, col)

                        if clicked_chess and clicked_chess.color == self.game.current_player.color:
                            self.selected_chess = clicked_chess
                            self.valid_moves = self.chess_board.get_valid_moves(self.selected_chess)
                        elif (row, col) in self.valid_moves:
                            self.chess_board.move(self.selected_chess, row, col)
                            self.game.next_turn()
                            self.is_my_turn = not self.is_my_turn
                            self.selected_chess = None
                            self.valid_moves = set()

            # 显示棋盘和棋子
            self.chess_board.show()

            # 显示选中棋子和可走位置
            self.ClickBox.show()
            self.Dot.show()
            # 显示游戏信息
            self.game.show()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    server = ChessServe()
    server.run()
