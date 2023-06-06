import pygame
import pygame_menu
import Chinesechess
import main

def start_game():
    Chinesechess.start_game()
    
def main2():
        main.main()

def quit_game():
    pygame.quit()
    quit()

def start_menu():
    # 创建菜单
    menu = pygame_menu.Menu('start', 800, 600, theme=pygame_menu.themes.THEME_BLUE)
   

    # 添加菜单选项
    menu.add.label('chinesechess')
    menu.add.button('gamemode1', start_game)
    menu.add.button('gamemode2', main2)
    menu.add.button('quit', quit_game)
    

    # 渲染菜单
    menu.mainloop(window_surface)

if __name__ == '__main__':
    # 初始化 Pygame
    pygame.init()

    # 设置窗口尺寸
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('chinseschess')

    # 启动游戏开始界面的菜单
    start_menu()