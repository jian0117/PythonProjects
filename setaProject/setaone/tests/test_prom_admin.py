from setaone.common import custom_urllib3
from setaone.constants import prom_admin_constants

def test_ab_list():
    endpoint = '/xhr/priceControl/ab/list'
    url = prom_admin_constants.TEST_HOST + endpoint
    data = '{"carrierIds":[470209143],"pageParam":{"page":1,"size":10}}'
    res = custom_urllib3.post(url=url, postBody_to_encode_json=data)
    print('coder'+ res.status)
    print(res.data)
    assert res.status == 200

def test_bdfy():
    res = custom_urllib3.get(url='https://fanyi.baidu.com/mtpe/v2/project/list?_=1714372867283&page=1&perPage=100000', params_combination=None)
    print(res.data)


class AdminConstans:
    TEST_HOST = 'http://10.131.71.238:8020'



if __name__ == '__main__':
    test_bdfy()