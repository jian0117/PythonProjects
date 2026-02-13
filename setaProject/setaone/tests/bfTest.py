import requests
import concurrent.futures
import json


def make_request(cookie, payload):
    url = 'https://test.yx.mail.netease.com/ops-portal/prom-ops/xhr/registration/sku/config/submit'
    url_list = 'https://test.yx.mail.netease.com/ops-portal/prom-ops/xhr/registration/sku/list'
    u3 = 'https://test.yx.mail.netease.com/ops-portal/prom-ops/xhr/activity/activityList'
    payload3 = {"name": "百亿", "startTimePoint": 1725033600000, "endTimePoint": 1725119999999, "status": 0,
                "searchType": 0, "pageParam": {"page": 1, "size": 10}}
    headers = {'Content-Type': 'application/json', 'Cookie': cookie}
    try:
        response = requests.post(url=u3, json=json.dumps(payload3), headers=headers, timeout=5)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")

if __name__ == '__main__':
    cookie1 = 'hb_MA-93E2-9647F5DD033F_source=login.netease.com; yx_username=wb.guojian03%40mesg.corp.netease.com; yx_name=%E9%83%AD%E5%81%A5; mail_psc_fingerprint=e70cb4441e8494d0c4c5f6e91d91125a; yx_csrf=5d4fea7e1f256054a821d1985778ecc7; hb_MA-A4D4-E99480416052_source=login.netease.com; hb_MA-89F6-A71EC58B127E_source=login.netease.com; hb_MA-B87E-44FCB2772963_source=yx.mail.netease.com; JSESSIONID_CUSTOM=27893eeb-4634-4f02-9f52-0eba65240b39; YX_OPENID_SESS=bub3IRG9wCop5BCvVgdkcM6qflqhYhntM99jGO9QuqyjyA6rqz36DSe/rUTw290hEClLfDEQqONvwPxc3X2yB2G2QhWBAkLQ5mSxUXnNzMRIEgrj7Yc+0Qvenf6LlrMbHTvBAxe0AqFIKyMLZISUNJ+RogeXgHKfNj1WHrTqlmQ=; YX_CSRF_TOKEN=5b4a9877555aac50040870b41757e7e8; tiger:sess=eyJfZXhwaXJlIjoxNzI1MDc1MTQ1MTI1LCJfbWF4QWdlIjo4NjQwMDAwMCwidGlnZXI6c2Vzc2lvbjpvbGRfZmxhc2hlcyI6W10sInRpZ2VyOnNlc3Npb246bmV3X2ZsYXNoZXMiOltdfQ==; yx_stat_seesionId=e70cb4441e8494d0c4c5f6e91d91125a1724996389677; LOGIN_IDENTITY="wb.guojian03@mesg.corp.netease.com#test"; solarSession=e11d0bc2-4bc2-420d-ad8e-435254a7f3b7'
    cookie2 = ''

    goapi_cookie = 'hb_MA-93E2-9647F5DD033F_source=login.netease.com; route=27288215bd87629ed2268e0afd0d8078; hb_MA-A4D4-E99480416052_source=login.netease.com; hb_MA-89F6-A71EC58B127E_source=login.netease.com; hb_MA-B87E-44FCB2772963_source=yx.mail.netease.com; solarSession=e11d0bc2-4bc2-420d-ad8e-435254a7f3b7'

    payload1 = {"registrationId": 200019, "skuId": 472316418, "price": "8", "costPayer": 1,
                "addOpt": {"2024-08-30": [472316418]}, "deleteOpt": {}}
    payload2 = {"registrationId": 200019, "skuId": 472316419, "price": "8", "costPayer": 1,
                "addOpt": {"2024-08-30": [472316419]}, "deleteOpt": {}}

    payload3 = {"name":"百亿","startTimePoint":1725033600000,"endTimePoint":1725119999999,"status":0,"searchType":0,"pageParam":{"page":1,"size":10}}
    make_request(cookie1, payload3)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #    executor.map(make_request, [(cookie1, payload1),(cookie2, payload2)])
