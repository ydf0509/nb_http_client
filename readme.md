# nb_http_client 是 python 史上性能最强的http客户端

## 0. 安装 pip install nb_http_client

## 1.测试比较环境为 win10 + python3.7 + 2.5ghz主频 + 单进程 + 线程池

```
e5 2678v3 主频很差，cpu架构很落后，如果用最新的13代i9超频最高可以达到6ghz，测试指标有可能可以提高100%。
但是不同的请求客户端都是跑在同一个2.5ghz主频上，所以是公平的比较。
```


## 2.不同的请求客户端，请求同一个server服务端，测试结果
```
线程池 + requests  390次每秒
线程池 + requests 同一个session 420次每秒
线程池 + urllib3    1070次每秒
线程池 + nb_http_client  2500次每秒，(最新的amd r7 5800H 4.2ghz 单核可以达到5100次每秒。)
asyncio + aiohttp    1480次每秒
线程池 + pycurl 30次每秒
```


## 3.测试代码

### 3.1服务端

```python
from aiohttp import web
"""
主要是用来测试http客户端池的最牛性能。不能让服务端成为客户端测试性能的瓶颈。
"""
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, aio")

app = web.Application()
app.add_routes(routes)
web.run_app(app,port=5678)
```


### 3.2.1 线程池 + 各种请求客户端
```python
import typing
from http.client import HTTPConnection
import time
import decorator_libs
import requests
import urllib3
import pycurl
from io import BytesIO
from nb_http_client import ObjectPool, HttpOperator
from threadpool_executor_shrink_able import BoundedThreadPoolExecutor

http_pool = ObjectPool(object_type=HttpOperator, object_pool_size=50, object_init_kwargs=dict(host='127.0.0.1', port=5678),
                       max_idle_seconds=30)
requests_session = requests.session()
urllib3_pool = urllib3.PoolManager(100)

thread_pool = BoundedThreadPoolExecutor(50)


def test_by_requets():
    # 这个连接池是requests性能5倍。 headers = {'Connection':'close'} 为了防止频繁报错 OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。
    resp = requests.get('http://127.0.0.1:5678/', headers={'Connection': 'close'})
    print(resp.text)


def test_by_requests_session():
    resp = requests_session.get('http://127.0.0.1:5678/', headers={'Connection': 'close'})
    print(resp.text)


def test_by_urllib3():
    resp = urllib3_pool.request('get', 'http://127.0.0.1:5678/', headers={'Connection': 'close'})  # urllib3 第二快，次代码手动实现的http池是第一快。
    print(resp.data)


def test_by_pycurl():
    # 这个号称c库，性能是最差的
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://127.0.0.1:5678/')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    print(body.decode())


def test_by_nb_http_client():
    with http_pool.get() as conn:  # type: typing.Union[HttpOperator,HTTPConnection]  # http对象池的请求速度暴击requests的session和直接requests.get
        r1 = conn.request_and_getresponse('GET', '/')
        print(r1.text[:10], )




if __name__ == '__main__':
    with decorator_libs.TimerContextManager():
        for x in range(30000):
            # time.sleep(5)  # 这是测试是否是是智能节制新建对象，如果任务不密集，不需要新建那么多对象。
            thread_pool.submit(test_by_pycurl, )  # TOOD 这里换成不同的函数来测试，然后在控制台搜索时分秒就能看到每一秒的响应个数了。
        thread_pool.shutdown()
    time.sleep(10000)  # 这个可以测试nb_http_client的连接长时间不使用，能自动摧毁


```
