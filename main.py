import json
import random
import re
import string
import time
import asyncio
import tiktoken
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from starlette.responses import StreamingResponse
import httpx
import logging

app = FastAPI()
authorization="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJiNDY3ZTE5Ny05ZjhiLTQ5OGQtYjAwMC1jNDMxYzNmZjJhOWYiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1NzU5MDk2LCJpYXQiOjE3MTQyMjMwOTZ9.94I1zvV2r4jv2-f38sTJ_10q2hM61s_iuqDYyEYjfjSBuCOyR-1tGsDiVn9ZMpKVuljjKRg03Ee0lT_lwsRLkQ"#对应信息
gtoken="03AFcWeA5GnmAGyxrpuDzrmyDQkT7J1DEcY9zAgdeITH91XIHWnzUFoFMDpuy1D3ghLZ4Msbi4_kb-1zl_VGz1c3R62AxgTILYcvYs-rPYxBgKVtyKBG0GDQcfpMqcMYgtd1gSM64qee9YE6zolYLPGGHbkrCV5w2gzz6CvZFjK3OqSPBX4dLvcdL0N88QtnB0UYvmNUdF6Q7Bbjk6-hMiUCGmCO-CTZMLEtWzNDpVCj8ZfY4N7R0WQEF7aCNUNfWk0UUAzI7uesbBDpKOhIFZgrIgvvyWK9EPCI-yKGpl8NKES-I7TrIRc4NjvdjEP2IOIJlwEXqoroJPNuQe0BffYGtiptrM7fXZa8tKQwamq77LGxiIUwi3zQvmToo3PolXA0LsNg3HVPMmo9OgBx7ZIySrS9QJIiVB_cLReENdw_sTN-2Xjy0YzB8RbAnBp0bCZcBNHZ1eYwFTJl8XIvTKdqihwfh8DPdiVM77ESTlZn2jwVNfpHX-N9Fv4KZJDzlWYFUtfbc7QSusc6AbuzeA3s8jsOcn0iz7d6CXRWb2FKwqRrXZRPtmfk0OCKYLo2QeWxP5udrlGGbYGx7vxeQhVHRxDXxMgAdwGvYU1ZSc-9GKAGdLT4qTFHJXG8Np5peYuu1i4S0oABnDHaYiIMAuAWxF0i7y8X_FYqyusE8xGFeUWD-RO_TqLzeRMPExW0nYkNQb25xiaxeNcKG8aSfMPiErhWczzDPGJdVVwzDEMCTuIksLBypXeSncha4RVZnuh-6fKONx9nMnRfyBzJFAPd7wv5x130NZpWlAYL5PExVx0dWeoMP_f7oMOTMd81A-uq59zGpz8PszTWTygNgLxVFe6dnTZLdLuGvO8dc6cl1B-EFcWdItEnFn9IHBtQ4E3SHhkn1KAZLIbgY40Eyj6FdQEbG0gwvozdFswqVoV9l6kfOY8RDcmFVLLZFQSivu2nLz5zYibHEn2bDN866DW1hTzA8o3ZYCZoVL0clw9nSLlk5GfwA52a_u91J38tKrE3qEDDDYRsDQIGHlBTJIL4VQEoEbCkA-qWWw_3WmCnV56-H1yqgyUBTKA5f-L2_j2pi-BbnAVoyIjosblBsYbTtst2MBOLZCaFk_V24wy7rgcPzzmIR3s8aP3XRznrbtSCdbloIpm6CE8Q_jgUDK9eYKN4XpvS3DOJO8QgTXNXfIiT-XGVjY2wLz_ch1Jke2V2kVpKHxvw7kZ9x9zG_1jwbQeG-Fp4ocyC3e817hW5ThsQqNNh2pAgmR22gbt-zPsyXyLSRmPpoDZ2_lks1ac7ptzItWaupKtcv0teitXfdf93isYDxV4YD-2trL3fFJWUDKTY7kL7dxrH1EDDY0KM0KgazImK6xJlQ7Ey3b1yquO29Z15UUxnZ4Q2Rlqip_YMepknTcyvliQJ-KVdZUlK_1uJEsih3zu7s_ITKmz1bIXgzbKXjseFukeySUu3OLqWweGKd0SbpCi-h9h0w3xnT3MEHKQG4aV_ELQSwqAsrr03kpfZv-WR8uruTKucuFZyalF2ijfnM_okFMux6F9I9FSl9gZuBpa4wZdnaiGfodM9e6waJRGM-efEa3qwJgCE42nzIG8DsHR5vP6Z9aGpMGWAqKnj0_ZKFsXbmu2uFIVooavWnUyXPMkrwFND7JBdsbTMZcDTVxxPqwifHTujZ9fhr8_elWbBMjIvv-SSWfVqcZy1HMiRgGmHuZgs0XEMChwblPNkw4nB7t9nTSoWGciuiI22dsWikXvq8_7GPIwC-8jyiGzC9vfmYXLG3C7Ba1elJT9_wMetM58LUB4W7cuPk0HfnstGYWmumBBSQvI3hZdhx7ZM1ES7m3kP8cPT7W5SjgHc0pkgTm9W_ZCrXAMtjnlVJQPyrJ_KnFmUj1kgzoeSTxukSGpIpHqDh92CJiXS7ZlCJ2jr50SjB3V3zUAiOmu69V5Euio1DvjtfpfxzDobNG4xM"
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count_token_messages(messages):
    # 给定一个消息列表，计算其总token数量
    count = 0
    for message in messages:
        content = message['content']
        count += content
    return count

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建 KeyManager 实例
logging.basicConfig(level=logging.INFO)


async def verify_key(authorization: str = Header(...)):
    try:
        prefix, token = authorization.split()
        if prefix.lower() != "bearer" or token != "123":
            raise HTTPException(status_code=400, detail="6")
    except ValueError:
        raise HTTPException(status_code=400, detail="6")


async def process_request(original_data):
    messages = original_data.get('messages', [])
    formatted_string = ','.join(f"{message['role']}:{message['content']}" for message in messages)
    new_data = {
        "isGetJson": True,
        "version": "1.3.6",
        "language": "zh-CN",
        "channelId": "7a77e2d4-a5c5-481a-ad9c-3c3edcb985ad",
        "message": "This dialogue record is crucial for your understanding and execution of tasks. In our interactions, you are the 'assistant', and I am the 'user'. The format is as follows: when 'user:' appears, it signifies my questions or statements; correspondingly, you do not need to start your replies with 'assistant:', just respond directly. This format will facilitate a more efficient dialogue between us." + formatted_string,
        "model":  "GPT-4",
        "messageIds": [],
        "improveId": None,
        "richMessageId": None,
        "isNewChat": None,
        "action": None,
        "isGeneratePpt": None,
        "isSlidesChat": False,
        "imageUrls": [],
        "roleEnum": None,
        "pptCoordinates": "",
        "translateLanguage": None,
        "docPromptTemplateId": None
    }
    return new_data


@app.post('/v1/chat/completions')
async def forward_request(request: Request):
    global authorization,gtoken
    request_data = await request.json()
    n = request_data.get('n', 1)
    messages = request_data.get('messages', [])
    total = ""
    for message in messages:
        total += message['content']
    prompt_tokens = num_tokens_from_string(total, "cl100k_base")
    models = request_data.get("model", "默认模型")
    request_data = await request.json()
    target_url = 'https://api.popai.pro/api/v1/chat/send'
    headers = {
        "accept": "text/event-stream",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,zh-HK;q=0.6",
        "app-name": "popai-web",
        "authorization": authorization,
        "content-type": "application/json",
        "device-info": "{web_id:k-s8Xp4S9LEmrHghBhT2m,baidu_id:18f1ff567e243687188711}",
        "gtoken": gtoken,
        "language": "en",
        "origin": "https://www.popai.pro",
        "priority": "u=1, i",
        "referer": "https://www.popai.pro/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",}

    should_stream = request_data.get("stream", False)
    messages = request_data.get('messages', [])
    formatted_string = ','.join(f"{message['role']}:{message['content']}" for message in messages)
    request_data = await process_request(request_data)
    if should_stream:
        response_data = handle_streaming_and_sending(request_data, formatted_string, models, headers, target_url)
        return StreamingResponse(response_data, media_type="application/json")
    else:
        response_data = await generate_non_streaming_response(request_data, models, headers,  prompt_tokens, n)
        return response_data


def get_random_string(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


async def generate_response(request_data, formatted_string, models, headers, target_url):
    retry_count = 0
    max_retries = 3
    delay = 0.035
    i = 0
    j = 1
    same_id = f'chatcmpl-{get_random_string(29)}'
    while retry_count < max_retries and not i == 1:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10, read=250), follow_redirects=True) as client:
                async with client.stream("POST", target_url, json=request_data, headers=headers) as res:
                    if res.status_code == 200:
                        async for line in res.aiter_lines():
                            try:
                                data = json.loads(line.lstrip("data:"))
                                if data:
                                    choices = data[0].get("content")
                                    if j :
                                        j=0
                                        continue
                                    result = {
                                        "id": same_id,
                                        "object": "chat.completion.chunk",
                                        "created": int(time.time()),
                                        "model": models,
                                        "system_fingerprint": "fp_a24b4d720c",
                                        "choices": [
                                            {"index": 0, "delta": {"content": choices}, "finish_reason": "null"}
                                        ],
                                    }
                                    json_result = json.dumps(result, ensure_ascii=False)
                                    yield f"data: {json_result}\n\n"
                                    await asyncio.sleep(delay)
                            except json.JSONDecodeError:
                                pass
                        yield f"data: {json.dumps({'id': same_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': models, 'system_fingerprint': 'fp_a24b4d720c', 'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n".encode(
                            'utf-8')
                        yield "data: [DONE]\n".encode('utf-8')
                        i=1

                    else:

                        logging.warning(f"Received non-200 status code {res.status_code}, retrying...")
                        retry_count += 1

        except (httpx.ReadTimeout, httpx.ConnectError) as e:
            error_message = f"Error during request: {e}"

            retry_count += 1

    return


async def generate_non_streaming_response(request_data, models, headers, prompt_tokens, n):
    target_url = 'https://api.popai.pro/api/v1/chat/send'
    """非流式生成响应"""
    same_id = f'chatcmpl-{get_random_string(29)}'
    choices = []
    delay = 1

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            semaphore = asyncio.Semaphore(5)
            async with semaphore:
                responses = await asyncio.gather(*[
                    client.post(url=target_url, json=request_data, headers=headers)
                    for _ in range(n)
                ])

            for i, response in enumerate(responses):
                data = ""
                response.raise_for_status()
                content_pattern = r'"content":"(.*?)"'
                content_matches = re.findall(content_pattern, response.text)

                if len(content_matches) > 1:
                    data = "".join(content_matches[1:])
                choice = {
                    "index": i,
                    "message": {
                        "role": "assistant",
                        "content": data
                    },
                    "finish_reason": "stop"
                }
                choices.append(choice)
                await asyncio.sleep(delay)

        prompt_tokens = prompt_tokens
        completion_tokens = sum(
            num_tokens_from_string(choice["message"]["content"], "cl100k_base") for choice in choices)
        total_tokens = prompt_tokens + completion_tokens

        response_data = {
            "id": same_id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": models,
            "choices": choices,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            },
        }
        return response_data

    except httpx.HTTPError as exc:
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


async def handle_streaming_and_sending(request_data, formatted_string, models, headers, target_url):
    data = ""
    async for item in generate_response(request_data, formatted_string, models, headers, target_url):
        yield item  # 将每个项作为流的一部分


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
