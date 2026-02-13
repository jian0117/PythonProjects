from selenium import webdriver

# 设置浏览器驱动路径
driver_path = "path_to_your_driver not_install"

# 创建一个浏览器实例
driver = webdriver.Chrome(executable_path=driver_path)  # 如果使用Chrome浏览器
# driver = webdriver.Firefox(executable_path=driver_path)  # 如果使用Firefox浏览器

# 打开网页
driver.get('https://www.example.com')

# 找到页面上的元素并与之交互
element = driver.find_element_by_name('q')  # 通过name属性查找元素
element.send_keys('Selenium Python')  # 在搜索框中输入文本

# 提交表单
element.submit()

# 等待一段时间
driver.implicitly_wait(10)  # 隐式等待10秒

# 关闭浏览器
driver.quit()