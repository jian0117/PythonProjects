import urllib3
import json

http = urllib3.PoolManager(timeout=3.0)
test_cookie = {
    'Cookie': 'YX_OPENID_SESS=LeNkqIh/8dIGMrUt5SsHQiSTrDkPH4AK1k6+Wal3gVOniPV488ljzwczEtN5bKgVnhcwfpG1FL992b0prab8iOX6bCZvmBMUFZM73SuPtoJa0WJ1RKvLZ/DxFxc5gXyIivBxkIM8tnO+BHur5I7oJTKbFpnaooV01T1nFZyiieU=; YX_CSRF_TOKEN=b25dd68286a22768597b8888d607b1c3; yx_username=grp.yxtest7%40corp.netease.com; yx_name=%E8%91%9B%E7%90%B3%E7%90%B3; tiger:sess=eyJfZXhwaXJlIjoxNzEzOTU0Mzg1ODQxLCJfbWF4QWdlIjo4NjQwMDAwMCwidGlnZXI6c2Vzc2lvbjpvbGRfZmxhc2hlcyI6W10sInRpZ2VyOnNlc3Npb246bmV3X2ZsYXNoZXMiOltdfQ==; mail_psc_fingerprint=32f44ae05f0cb0efcb60bbbf676c0f99; yx_stat_seesionId=32f44ae05f0cb0efcb60bbbf676c0f991713922178935'}

def get(url, params_combination):
    url_combination = ''
    if params_combination:
        if str(params_combination).startswith('?='):
            url_combination = url + params_combination
        else:
            url_combination = url + '?=' + params_combination
    response = http.request(method='GET', url=url_combination, headers=test_cookie)
    return response


def post(url, postBody_to_encode_json):
    #encode_body = json.load(str(postBody_to_encode_json))
    healders = {'Content-Type':'application/json'}
    healders.update(test_cookie)
    response = http.request('POST', url=url, body=postBody_to_encode_json, headers=healders)
    return response
