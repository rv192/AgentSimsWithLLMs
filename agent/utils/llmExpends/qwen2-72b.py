from typing import List, Dict, Any
import os
import json
import traceback
import openai
from agent.utils.llmExpends.BasicCaller import BasicCaller

abs_path = os.path.dirname(os.path.realpath(__file__))

class Qwen2-72bCaller(BasicCaller):
    def __init__(self) -> None:
        self.model = "qwen2-72b"
        self.api_key = ""
        with open(os.path.join(abs_path, "..", "..", "..", "config", "api_key.json"), "r", encoding="utf-8") as api_file:
            api_keys = json.loads(api_file.read())
            self.api_key = api_keys["qwen2-72b"]
        openai.api_key = self.api_key
        openai.proxy = {
            "https": "https://api.72live.com"
        }
        if not self.api_key:
            raise ValueError("Api key not found")
    
    async def ask(self, prompt: str) -> str:
        counter = 0
        result = "{}"
        while counter < 3:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                result = response.choices[0].message['content']
                return result
            except Exception as e:
                print(e)
                counter += 1

        try:
            traceback.print_exc()
            print(response.json())
        except:
            pass
        __import__('remote_pdb').set_trace()
