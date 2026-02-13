#抓表情包存到picts
import requests
from bs4 import BeautifulSoup
import os
import re
import urllib3
import time
from urllib.parse import urlparse
from datetime import datetime


if __name__ == '__main__':

    #cookie = input('请输入您抓的cookie：')
    # 设置请求头和Cookie
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Cookie":"_xsrf=DcIBhsN3rI34mP23RVASBSx5uOgOSrgD; _zap=9818e575-45b7-4c5d-9d7f-fa40afaa459c; d_c0=AADSzThdDRmPTjZaVXbWZPryE8OdD0Qh_zc=|1723173582; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1723173584; HMACCOUNT=D575788A45916BF5; captcha_session_v2=2|1:0|10:1723173585|18:captcha_session_v2|88:VktpTFFGbzRWejdHMEpYWXM0Wmlxa1RUUFpqTG4rMmN4RGppNU5NVGozaXd3eWZ1czdvUGZVVStlNzZJNU5reA==|28a9d34d94cf14c6b62c6bfe9826491c069de336e6a1bb0793dbdffabe4799a2; q_c1=fb8859d9793a4928a25a10f7b8547c45|1723173615000|1723173615000; z_c0=2|1:0|10:1723173617|4:z_c0|92:Mi4xVjl0aEJBQUFBQUFBQU5MTk9GME5HU1lBQUFCZ0FsVk42dGlpWndBNEg0SEk5RjU5OFV3MXdodk1KUWhpTnM1eDln|eb6bbfb98927a3c1eec7d0bacb7328442200cf7ed62deb3a4487a4dbab8053ee; __zse_ck=001_vdWtRNEEwIRKVAykZVBIfWL2FIfPIQQZCtY0XoT90a2+jJ3maq1Sz3WO1gj83gypg/Jf55pF/L68mjN=gEAM9P5wp+39qyixxXcz9AUa0uVVDjBiE55jzPQL3cl9swIO; tst=r; SESSIONID=wb1Ge3ICUIIYtZ1vmjBCAd2MLAzGqaYRHJKSZq3IcPV; JOID=VFoVAE0HlntD0HdYEwLC75zqL1EMdPZJAbVAE1NS2zAZoS1tZ0nGuCDUcVkVS8QRi4B5E143Z_mC3pr_OlqAS6A=; osd=Vl0WAkwFkXhB0XVfEADD7ZvpLVAOc_VLALdHEFFT2TcaoyxvYErEuSLTclsUScMSiYF7FF01ZvuF3Zj-OF2DSaE=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1724234128; BEC=d892da65acb7e34c89a3073e8fa2254f"
    }

    # 发送请求获取页面内容
    url = input('请输入url：')
    response = requests.get(url, headers=headers)
    html = response.text
    parsed_url = urlparse(url)
    url_p_list = parsed_url.path.split('/')
    project_name = url_p_list[-1]

    # 解析页面内容
    soup = BeautifulSoup(html, "html.parser")

    # 提取所有图片链接，包括 GIF 图片
    image_tags = soup.find_all("img")
    image_urls = [tag["src"] for tag in image_tags if "src" in tag.attrs]

    # 下载图片和 GIF
    save_directory = "D:\\emoticon_pictures\\zhihu_" + project_name + '_' + str(datetime.now().date())
    os.makedirs(save_directory, exist_ok=True)

    for index, image_url in enumerate(image_urls):
        # 检查是否是 GIF 图片
        if image_url.endswith(".gif"):
            image_response = requests.get(image_url)
            with open(os.path.join(save_directory, f"image{index}.gif"), "wb") as f:
                f.write(image_response.content)
        else:
            # 排除 data:image 类型的图片
            if not image_url.startswith("data:image"):
                image_response = requests.get(image_url)
                with open(os.path.join(save_directory, f"image{index}.jpg"), "wb") as f:
                    f.write(image_response.content)
    if os.listdir(save_directory):
        print("success")