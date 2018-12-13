#多线程例子
from time import sleep
import threading

def move():
    print("123")
    sleep(5)

def move2():
    print("123")
    sleep(5)

def move3():
    print("123")
    sleep(5)

def music():
    print("456")
    sleep(5)

#创建线程数组
threads = []

#创建线程t1，并添加到线程数组
t1 = threading.Thread(target=music)
threads.append(t1)

#创建线程t2，并添加到线程数组
t2 = threading.Thread(target=move)
threads.append(t2)

t3 = threading.Thread(target=move2)
threads.append(t3)

t4 = threading.Thread(target=move3)
threads.append(t4)

if __name__ == '__main__':
    for i in threads:
        i.start()

    for i in threads:
        i.join()

    print("执行线程后的动作")