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

with open("api_key.txt", "r") as f:
    openai.api_key = f.read().strip()

class ExecutorBase(object):
    executor = ThreadPoolExecutor(4)

class HttpHelper(object):
    def jsonify(self, *args, **kwargs):
        #self.set_header("Content-Type", "text/json")
        indent = None
        separators = (",", ":")

        if args and kwargs:
            raise TypeError("jsonify() behavior undefined when passed both args and kwargs")
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs
        if data['type']=="ws":
            del data['type']
            self.write_message(json.dumps(data, ensure_ascii=False))
        else:
            self.write(json.dumps(data, indent=indent, separators=separators))

    def success(self, msg: str = "", data: dict = {}, type: str = "api"):
        """ 成功响应 默认值”成功“ """
        return self.jsonify(code=200, msg=msg, data=data, type=type)

    def fail(self, msg: str = "", data: dict = {}, type: str = "api"):
        """ 失败响应 默认值“失败” """
        return self.jsonify(code=0, msg=msg, data=data, type=type)
    
class WsCompletion(tornado.websocket.WebSocketHandler, ExecutorBase, HttpHelper):
    def check_origin(self, origin):
        """校验权限"""
        return True

    def open(self):
        """开启连接"""
        print("BaseWebsocket opened")

    @gen.coroutine
    def on_message(self, messages: str):
        """连接通信"""
        try:
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=messages,
                stream=True,
            )

            for event in response:
                self.success(data=event, type="ws")
        except:
            self.fail(msg='内部错误', type="ws")

    def on_close(self):
        """关闭连接"""
        print("BaseWebsocket closed")

    @run_on_executor
    def resp_time(self, request_data):
        # 异步执行延时操作 to do sth
        time.sleep(2)
        return time.time()

class WsChatCompletion(tornado.websocket.WebSocketHandler, ExecutorBase, HttpHelper):
    def check_origin(self, origin):
        """校验权限"""
        return True

    def open(self):
        """开启连接"""
        print("BaseWebsocket opened")

    @gen.coroutine
    def on_message(self, messages: str):
        """连接通信"""
        try:
            # 将messages转换为list
            messages = json.loads(messages)
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                stream=True,
            )

            for event in response:
                self.success(data=event, type="ws")
        except:
            self.fail(msg='内部错误', type="ws")

    def on_close(self):
        """关闭连接"""
        print("BaseWebsocket closed")

    @run_on_executor
    def resp_time(self, request_data):
        # 异步执行延时操作 to do sth
        time.sleep(2)
        return time.time()
       
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
                self.success(data=response)
            except:
                self.fail(msg='内部错误')
        else:
            self.fail(msg='参数错误')

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

            self.success(data=response)
        except:
            self.fail(msg='内部错误')

def make_app():
    """路由"""
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/api/Completion", ApiCompletion),
        (r"/api/ChatCompletion", ApiChatCompletion),
        (r"/websocket/Completion", WsCompletion),
        (r"/websocket/ChatCompletion", WsChatCompletion),
    ])


def start(port):
    """启动"""
    app = make_app()
    app.listen(port=port)
    IOLoop.current().start()

if __name__ == '__main__':
    print('--start--')
    start(8000)