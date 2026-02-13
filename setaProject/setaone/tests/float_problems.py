if __name__ == '__main__':
    characters = {
        '摸': ['  ／^ ^＼  ', '／  ●  ●  ＼', '＼   -  -   ／', '  ＼＿＿／   '],
        '鱼': ['<`)))><  ', '(((,  )   ', '<`)))><  ', '(((  )>   '],
        '中': ['  ┏━━┓  ', '┃┃', '  ┗━━┛  ', '          ']
    }

    # 打印大字
    for i in range(4):
        for char in "摸鱼中":
            print(characters[char][i], end="  ")
        print()