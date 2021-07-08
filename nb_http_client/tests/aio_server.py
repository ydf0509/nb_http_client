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
