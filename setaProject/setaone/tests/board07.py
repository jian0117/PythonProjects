

if __name__ == '__main__':
    import concurrent.futures


    # 定义一个简单的函数
    def my_function(x):
        return x * x


    # 创建一个 ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 使用 map 方法并行执行 my_function
        results = executor.map(my_function, [1, 2, 3, 4, 5])

        # results 是一个迭代器，包含了每个函数调用的结果
        for result in results:
            print(result)
