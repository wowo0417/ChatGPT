import time
import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop
from tornado import gen
import tornado.options
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import openai
import json
from asyncio import sleep 

with open("api_key.txt", "r") as f:
    openai.api_key = f.read().strip()

class ExecutorBase(object):
    executor = ThreadPoolExecutor(4)

class HttpHelper(object):
    def success(self, msg: str = "", data: dict = {}):
        return json.dumps({"code":200, "msg":msg, "data":data})
    
    def fail(self, msg: str = "", data: dict = {}):
        return json.dumps({"code":0, "msg":msg, "data":data})

class SseCompletion(tornado.web.RequestHandler, HttpHelper):

    def on_finish(self):
        print('close connection')
        return super().on_finish()
    
    async def post(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Access-Control-Allow-Origin', "*")  
        self.set_header("Access-Control-Allow-Headers","*") 

        # 获取参数，如果没有置为空
        model = self.get_argument('model', 'text-davinci-003')
        prompt = self.get_argument('prompt', '')
        temperature = self.get_argument('temperature', 0.5)
        max_tokens = self.get_argument('max_tokens', 4000)
        top_p = self.get_argument('top_p', 1.0)
        frequency_penalty = self.get_argument('frequency_penalty', 0.0)
        presence_penalty = self.get_argument('presence_penalty', 0.0)
        
        if prompt:
            try:
                response = openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stream=True,
                )
                for event in response:
                    self.write("data:" + self.success(data=event) + "\n\n")
                    self.flush()
            except:
                self.write("data:" + self.fail("内部错误") + "\n\n")
                self.flush()
        else:
            self.write("data:" + self.fail("参数错误") + "\n\n")
            self.flush()

class SSeChatCompletion(tornado.web.RequestHandler, HttpHelper):
    def on_finish(self):
        print('close connection')
        return super().on_finish()
    
    async def post(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Access-Control-Allow-Origin', "*")  
        self.set_header("Access-Control-Allow-Headers","*") 

        # 获取参数，如果没有置为空
        model = self.get_argument('model', 'gpt-3.5-turbo')
        messages = self.get_argument('messages', '')
        temperature = self.get_argument('temperature', 0.5)
        max_tokens = self.get_argument('max_tokens', 4000)
        top_p = self.get_argument('top_p', 1.0)
        frequency_penalty = self.get_argument('frequency_penalty', 0.0)
        presence_penalty = self.get_argument('presence_penalty', 0.0)
        
        try:
            # 将messages转换为list
            messages = json.loads(messages)

            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stream=True,
            )

            for event in response:
                self.write("data:" + self.success(data=event) + "\n\n")
                self.flush()
        except:
            self.write("data:" + self.fail("内部错误") + "\n\n")
            self.flush()
       
class ApiCompletion(tornado.web.RequestHandler, HttpHelper):

    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin","*")

        # 获取参数，如果没有置为空
        model = self.get_argument('model', 'text-davinci-003')
        prompt = self.get_argument('prompt', '')
        temperature = self.get_argument('temperature', 0.5)
        max_tokens = self.get_argument('max_tokens', 1000)
        top_p = self.get_argument('top_p', 1.0)
        frequency_penalty = self.get_argument('frequency_penalty', 0.0)
        presence_penalty = self.get_argument('presence_penalty', 0.0)
        
        if prompt:
            try:
                response = openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                )
                write_msg = self.success(data=response)
            except:
                write_msg = self.fail(msg='内部错误')
        else:
            write_msg = self.fail(msg='参数错误')

        self.write(write_msg)

class ApiChatCompletion(tornado.web.RequestHandler, HttpHelper):

    def post(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin","*")

        # 获取参数，如果没有置为空
        model = self.get_argument('model', 'gpt-3.5-turbo')
        messages = self.get_argument('messages', '')
        temperature = self.get_argument('temperature', 0.5)
        max_tokens = self.get_argument('max_tokens', 1000)
        top_p = self.get_argument('top_p', 1.0)
        frequency_penalty = self.get_argument('frequency_penalty', 0.0)
        presence_penalty = self.get_argument('presence_penalty', 0.0)
        
        try:
            # 将messages转换为list
            messages = json.loads(messages)

            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )

            write_msg = self.success(data=response)
        except:
            write_msg = self.fail(msg='内部错误')

        self.write(write_msg)

def make_app():
    """路由"""
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/api/Completion", ApiCompletion),
        (r"/api/ChatCompletion", ApiChatCompletion),
        (r"/sse/Completion", SseCompletion),
        (r"/sse/ChatCompletion", SSeChatCompletion),
    ])


def start(port):
    """启动"""
    app = make_app()
    app.listen(port=port)
    IOLoop.current().start()

if __name__ == '__main__':
    print('--start--')
    start(8001)