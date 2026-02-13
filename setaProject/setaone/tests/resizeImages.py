import os
from PIL import Image


def resize_images_in_directory(directory_path, new_width, new_height):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".jpg", ".png")):
            image_path = os.path.join(directory_path, filename)
            try:
                img = Image.open(image_path)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                img = img.convert("RGB")  # 转换为RGB模式，以确保保存为JPEG格式的兼容性
                img.save(image_path)  # 保存到原始文件路径
            except Exception as e:
                print(f"处理 {filename} 时出错：{e}")


if __name__ == '__main__':
    # 示例用法
    directory_path = "D:/emoticon_pictures/test_upload_pics"
    new_width = 800
    new_height = 800
    resize_images_in_directory(directory_path, new_width, new_height)
