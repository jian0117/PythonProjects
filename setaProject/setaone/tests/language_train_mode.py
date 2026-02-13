# -*- coding:utf-8 -*-
import random
import spacy
import re

def extract_coupon_info(text):
    pattern_category = r'直减类型|直减券'  # 匹配优惠券类型的模式
    pattern_price = r'(\d+)元'  # 匹配优惠金额的模式

    category_match = re.search(pattern_category, text)
    price_match = re.search(pattern_price, text)

    if category_match:
        coupon_category = category_match.group(0)
    else:
        coupon_category = None

    if price_match:
        reduce_price = int(price_match.group(1))
    else:
        reduce_price = None

    return {"couponCategory": coupon_category, "reducePrice": reduce_price}




if __name__ == '__main__':

    nlp = spacy.load("zh_core_web_sm")

    text = "创建一个直减券，满1000打5折"
    doc = nlp(text)

    # 打印词性标注和实体识别结果
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

    print(extract_coupon_info(text))