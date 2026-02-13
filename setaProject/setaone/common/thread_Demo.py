import threading

def print_numbers():
    for i in range(5):
        print(i)

def print_letters():
    for letter in 'abcde':
        print(letter)

# 创建线程
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

# 启动线程
t1.start()
t2.start()

# 等待线程执行完毕
t1.join()
t2.join()
