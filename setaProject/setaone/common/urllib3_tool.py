# custom_http.py

import urllib3
import json

class CustomUrllib3:
    def __init__(self):
        # 初始化操作
        self.http = urllib3.PoolManager()
        self.get_header = {'Cookie':'YX_OPENID_SESS=LeNkqIh/8dIGMrUt5SsHQiSTrDkPH4AK1k6+Wal3gVOniPV488ljzwczEtN5bKgVnhcwfpG1FL992b0prab8iOX6bCZvmBMUFZM73SuPtoJa0WJ1RKvLZ/DxFxc5gXyIivBxkIM8tnO+BHur5I7oJTKbFpnaooV01T1nFZyiieU=; YX_CSRF_TOKEN=b25dd68286a22768597b8888d607b1c3; yx_username=grp.yxtest7%40corp.netease.com; yx_name=%E8%91%9B%E7%90%B3%E7%90%B3; tiger:sess=eyJfZXhwaXJlIjoxNzEzOTU0Mzg1ODQxLCJfbWF4QWdlIjo4NjQwMDAwMCwidGlnZXI6c2Vzc2lvbjpvbGRfZmxhc2hlcyI6W10sInRpZ2VyOnNlc3Npb246bmV3X2ZsYXNoZXMiOltdfQ==; mail_psc_fingerprint=32f44ae05f0cb0efcb60bbbf676c0f99; yx_stat_seesionId=32f44ae05f0cb0efcb60bbbf676c0f991713922178935'}
        self.post_header = {'Cookie':'YX_OPENID_SESS=LeNkqIh/8dIGMrUt5SsHQiSTrDkPH4AK1k6+Wal3gVOniPV488ljzwczEtN5bKgVnhcwfpG1FL992b0prab8iOX6bCZvmBMUFZM73SuPtoJa0WJ1RKvLZ/DxFxc5gXyIivBxkIM8tnO+BHur5I7oJTKbFpnaooV01T1nFZyiieU=; YX_CSRF_TOKEN=b25dd68286a22768597b8888d607b1c3; yx_username=grp.yxtest7%40corp.netease.com; yx_name=%E8%91%9B%E7%90%B3%E7%90%B3; tiger:sess=eyJfZXhwaXJlIjoxNzEzOTU0Mzg1ODQxLCJfbWF4QWdlIjo4NjQwMDAwMCwidGlnZXI6c2Vzc2lvbjpvbGRfZmxhc2hlcyI6W10sInRpZ2VyOnNlc3Npb246bmV3X2ZsYXNoZXMiOltdfQ==; mail_psc_fingerprint=32f44ae05f0cb0efcb60bbbf676c0f99; yx_stat_seesionId=32f44ae05f0cb0efcb60bbbf676c0f991713922178935'}

    def get(self, url, params_combination):
        if str(params_combination).startswith('?='):
            url_combination = url + params_combination
        else:
            url_combination = url + '?=' + params_combination
        response = self.http.request('GET', url_combination, self.get_header)
        return response.data

    def post(self, url, postBody_to_encode_json):
        encode_body = json.dumps(postBody_to_encode_json).encode('utf-8')
        response = self.http.request('POST', url, encode_body, self.post_header)
        return response.data

