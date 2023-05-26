import subprocess
import os
from time import sleep, localtime
Address = 'pikafish-avx2.exe'

def GetData(params1):

    ret = subprocess.Popen(Address, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, encoding="GBK")
    # 输入参数
    ret.stdin.write(params1 + "\n")
    ret.stdin.write("d\n")
    ret.stdin.write("go \n")
    ret.stdin.flush()
    sleep(3)

    # 输出数据
    ret.stdin.close()
    out = ret.stdout.read()
    ret.stdout.close()
    # print(out)
    stat = out.find("Fen")
    stat1 = out.find('Key')
    # print(stat1)
    # print('\n'+out[stat + 5:stat1-1])
    # 最优解
    Bestmove = out.find("bestmove")
    # print(out[Bestmove + 9:Bestmove + 13])
    ascii_values = []
    next_step = str(out[Bestmove + 9:Bestmove + 13])
    params1 = 'position fen ' + out[stat + 5:stat1-1] + ' moves'
    params1 = params1 + ' ' + next_step
    print(params1)

    for character in next_step:
        ascii_values.append(ord(character))

    ascii_values[0] = ascii_values[0] - 97
    ascii_values[1] = 9 - (ascii_values[1] - 48)
    ascii_values[2] = ascii_values[2] - 97
    ascii_values[3] = 9 - (ascii_values[3] - 48)
    print(ascii_values)

    return ascii_values, params1

def init_history(mode):
    path = './/history'
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径

    t = localtime()
    path = './/history//' + str(t.tm_mon) + '_' + str(t.tm_mday) + '_' + str(t.tm_hour) + '_' + str(t.tm_min) + '.txt'
    text = "time: " + str(t.tm_mon) + '/' + str(t.tm_mday) + ' ' + str(t.tm_hour) + '/' + str(t.tm_min) + '\n'
    text = text + 'step: 0\n'
    text = text + 'mode: ' + str(mode) + '\n'
    file = open(path, 'w')
    file.write(text)
    file.close()
    return path

def add_step(path, step): # old_col old_row new_col new_row
    file = open(path)
    content = file.readlines()
    file.close()
    c = content[1][6:]
    content[1] = "step: " + str(int(c)+1) + '\n'
    content.append(step)

    file = open(path, 'r+')
    str_c = "".join(content)
    str_c = str_c + '\n'
    file.write(str_c)
    file.close()
    return 0

def get_history(path,step_num):
    file = open(path)
    content = file.readlines()
    file.close()
    step = content[step_num+2]
    return step
def get_step_num(path):
    file = open(path)
    content = file.readlines()
    file.close()
    num = int(content[1][6:])
    return num
def main():
    path = init_history(2)
    add_step(path, 'abcd')
    add_step(path, 'abcd')
    add_step(path, 'abcd')
    add_step(path, 'abcd')
    return 0

if __name__ == '__main__':
    main()
