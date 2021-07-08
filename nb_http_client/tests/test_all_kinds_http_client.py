import typing
from http.client import HTTPConnection
import time
import decorator_libs
import requests
import urllib3
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


def test_by_nb_http_client():
    with http_pool.get() as conn:  # type: typing.Union[HttpOperator,HTTPConnection]  # http对象池的请求速度暴击requests的session和直接requests.get
        r1 = conn.request_and_getresponse('GET', '/')
        print(r1.text[:10], )


if __name__ == '__main__':
    with decorator_libs.TimerContextManager():
        for x in range(30000):
            # time.sleep(5)  # 这是测试是否是是智能节制新建对象，如果任务不密集，不需要新建那么多对象。
            thread_pool.submit(test_by_nb_http_client, )  # TOOD 这里换成不同的函数来测试，然后在控制台搜索时分秒就能看到每一秒的响应个数了。
        thread_pool.shutdown()
    time.sleep(10000)  # 这个可以测试nb_http_client的连接长时间不使用，能自动摧毁
