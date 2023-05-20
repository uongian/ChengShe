import subprocess
from time import sleep
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

    # 最优解
    Bestmove = out.find("bestmove")
    print(out[Bestmove + 9:Bestmove + 13])
    ascii_values = []
    next_step = str(out[Bestmove + 9:Bestmove + 13])

    params1 = params1 + ' ' + next_step
    print(params1)

    for character in next_step:
        ascii_values.append(ord(character))

    ascii_values[0] = ascii_values[0] - 97
    ascii_values[1] = 9 - (ascii_values[1] - 48)
    ascii_values[2] = ascii_values[2] - 97
    ascii_values[3] = 9 - (ascii_values[3] - 48)
    print(ascii_values)
    return ascii_values,params1