import asyncio
import time

import rubikai
import json

from rubikai import version
model_api_key = "RBbNKRkaNaOu78agDa03055224864b88A071067fA99177Fb"
model_api_base = "https://brain.thundersoft.com/brain"
#
# knowledge_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJhcGlLZXlcIjpcIkV0b0k4VFR1MkpwYXZ5OVAyOUYzQjlEMzQ5M2Y0Y0FjODVGNjNhODMxZjY5ODk0NlwiLFwiY3JlYXRlVGltZVwiOlwiMFwiLFwiZW1haWxcIjpcIlwiLFwiaWRcIjozNzUsXCJtb2JpbGVcIjpcIjEzMDExMDMzNzk2XCIsXCJwYXNzd29yZFwiOlwiXCIsXCJwd2RUaW1lXCI6XCIyMDIzMDgyNjA5NTEzMVwiLFwicmVtYXJrXCI6XCJcIixcInJvbGVzXCI6W3tcImlkXCI6MyxcIm5hbWVcIjpcIuaZrumAmueUqOaIt1wifV0sXCJzdGF0dXNcIjowLFwidGVuYW50SWRcIjowLFwidGVuYW50TmFtZVwiOlwiXCIsXCJ0eXBlXCI6XCJ1c2VyXCIsXCJ1c2VyTm9cIjpcIlUxMzAxMTAzMzc5NlwiLFwidXNlcm5hbWVcIjpcIuWnmuW7uua4oFwiLFwid2FybmluZ1wiOlwiMFwiLFwiZ2VuX3RpbWVcIjoxNzA3MTI1MDU3OTcyfSIsImV4cCI6MTcwOTcxNzA1N30.cmbhBvbo-QH21MlrC6agyjhcZ_cupySx-Bu8SOixcgY"
# knowledge_api_base = "https://brain.thundersoft.com/brain"

knowledge_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJhcGlLZXlcIjpcIm45aG1NTFc0WXNMdUNJSDZFMTU1RmQ4MEI3MWQ0YzZhQThEZUMzQzk5NzhiQTU3NlwiLFwiY3JlYXRlVGltZVwiOlwiMFwiLFwiZW1haWxcIjpcIlwiLFwiaWRcIjoyODcsXCJtb2JpbGVcIjpcIjEzMDExMDMzNzk2XCIsXCJwYXNzd29yZFwiOlwiXCIsXCJwd2RUaW1lXCI6XCIxNzAxNDE4Nzk4MzgxXCIsXCJyZW1hcmtcIjpcIlwiLFwicm9sZXNcIjpbe1wiaWRcIjozLFwibmFtZVwiOlwi5pmu6YCa55So5oi3XCJ9XSxcInN0YXR1c1wiOjEsXCJ0ZW5hbnRJZFwiOjAsXCJ0ZW5hbnROYW1lXCI6XCJcIixcInR5cGVcIjpcInVzZXJcIixcInVzZXJOb1wiOlwidTEzMFwiLFwidXNlcm5hbWVcIjpcIuWnmuW7uua4oFwiLFwid2FybmluZ1wiOlwiMFwiLFwiZ2VuX3RpbWVcIjoxNzA5NTM5MjM2NDY2fSIsImV4cCI6MTcxMjEzMTIzNn0.J2KH3PhbkIJ4ViQpZcnRY7QN-eWuJgX40p__A41dLwQ"
knowledge_api_base = "http://10.0.36.13:8888/brain"
stream = True
#基于模型聊天
chat_model_kwargs = {
        "api_key": model_api_key,
        "api_base": model_api_base,
        "object_name": "billing.v1.chat.completions",
        "model": "rubik6-chat",
        "messages": [
            {
                "role": "user",
                "content": "魔方大脑有什么功能？",
            }
        ],
        "temperature": 0,
        "stream": stream
    }
#获取模型列表
list_model_kwargs = {
        "api_key": model_api_key,
        "api_base": model_api_base,
        "object_name": "billing.v1.models.available",
        "method": "GET",
    }

#知识库聊天
chat_knowledge_kwargs = {
        "api_key": knowledge_api_key,
        "api_base": knowledge_api_base,
        "object_name": "knowledge.api.chat.chat",
        "model": "rubik6-chat",
        "messages": [
            # {
            #     "role": "user",
            #     "content": "你是什么模型？",
            # }
        ],
        "question": "项目经理的职责是什么？",
        "knowledge_ids": [1764950893469499393],
        "select_type": 0,
        "res_json": 0 if version.VERSION == '1.3' else 1,
        "temperature": 0,
        "stream": stream
    }

async def await_test():
    start_time = time.time()
    is_first = True
    async for response in await rubikai.BrainOsCompletion.acreate(**chat_model_kwargs):
        if is_first:
            is_first = False
            end_time = time.time()
            print("-----首字耗时 {:.2f}秒".format(end_time - start_time))
        print(response)



async def test():
   await await_test()

if __name__ == '__main__':

    #模型聊天
    #asyncio.run(await_test())  # asyncio.run(test())  #都可以
    # response = rubikai.ChatCompletion.create(**chat_model_kwargs)
    # for chunk in response:
    #     print(f"{json.dumps(chunk,ensure_ascii=False)}")
    #获取模型列表
    # response = rubikai.ChatCompletion.dealRequest(**list_model_kwargs)
    # data = json.loads(response)
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    # print(json_data)

    # 基于知识库聊天
    response = rubikai.ChatCompletion.dealRequest(**chat_knowledge_kwargs)
    if stream:
        for chunk in response:
            print(f"{json.dumps(chunk, ensure_ascii=False)}")
    else:
            print(response)
            #print(json.dumps(response, ensure_ascii=True))
            #json.dumps(response, ensure_ascii=False)

