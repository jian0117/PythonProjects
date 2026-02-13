# -*- coding: utf-8 -*-
import requests
import json
import setaone.common.funs

def fetch_and_parse_data():
    # 发送 POST 请求
    url = 'https://chat-ws.baidu.com/aichat/api/conversation'
    payload = {"message":{"inputMethod":"keyboard","isRebuild":False,"lastMsgId":"b4142752-59f1-42b4-a481-ad6035fea4dc","lastMsgIndex":0,"source":"input","content":{"query":"提问测试","qtype":0,"customes":[],"botQuery":{},"autoQuery":False,"pluginQuery":{},"pageInfo":{},"containerInfo":{"containerType":0,"isDegrade":0},"pluginInfo":[]},"from":""},"sessionId":"bd895d90-afc4-4386-bbb8-41ec072832e6","aisearchId":"17960601259158877701","pvId":"10661747845519583198","newTopic":False}  # 这里添加需要发送的数据
    cookie = 'BAIDUID=086DDE7206FE6EF2AA65394C512132C9:FG=1; BDUSS=FNLXEtdmJjQXFVdVc3NGlHN1BMMWhSZnB-cUhxTFZ6ZUNuaVczeHJIdERUMFJtSVFBQUFBJCQAAAAAAAAAAAEAAAABj0k3bWluaW1hbGRheQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEPCHGZDwhxmRG; BDUSS_BFESS=FNLXEtdmJjQXFVdVc3NGlHN1BMMWhSZnB-cUhxTFZ6ZUNuaVczeHJIdERUMFJtSVFBQUFBJCQAAAAAAAAAAAEAAAABj0k3bWluaW1hbGRheQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEPCHGZDwhxmRG; BIDUPSID=086DDE7206FE6EF2AA65394C512132C9; PSTM=1713160792; H_WISE_SIDS_BFESS=60289_60299_60327; MCITY=-179%3A; H_PS_PSSID=60327_60339; BAIDUID_BFESS=086DDE7206FE6EF2AA65394C512132C9:FG=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=5; BA_HECTOR=8404ah818h2g24al2kala484a0ckfm1j6v4ue1v; ZFY=:AsOOO0GGavA9MdLCrD:BPxyrpVk0OWIPOiPkwZhEen:BQ:C; RT="z=1&dm=baidu.com&si=bd59c780-ca31-49b9-a0fb-ee4de143d0b4&ss=lxiceppa&sl=2&tt=21c&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=5wn&ul=w4ha&hd=w4hp"; H_WISE_SIDS=60327_60339; ET_WHITELIST=etwhitelistintwodays; BDRCVFR[Gm3feW4UKgs]=mbxnW11j9Dfmh7GuZR8mvqV'
    headers = {
        'Content-Type': 'application/json',
        'Cookie': cookie
    }

    response = requests.post(url, data=json.dumps(payload, ensure_ascii=False), headers=headers)

    if response.status_code == 200:
        # 解析返回的数据
        response_data = response.text
        jsons = setaone.common.funs.extract_json_data(response_data)
        texts = [item["content"]["generator"]["text"] for item in jsons.get("event", []) if "content" in item and "generator" in item["content"] and "text" in item["content"]["generator"]]

        # 组成新的文章
        new_article = "\n".join(texts)
        return new_article
    else:
        return "Failed to fetch data"

# 调用方法并输出结果
if __name__ == '__main__':
    result_article = fetch_and_parse_data()
    print(result_article)