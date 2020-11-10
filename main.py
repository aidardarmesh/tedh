from aiohttp import web
from routes import setup_routes

import json
import asyncpg


app = web.Application()
app.router.add_routes(
    [
        web.get(r'/{ip:[\w.]+}', read),
        web.get(r'/{ip:[\w.]+}/{port:\d+}', read),
        web.post('/create', create),
        web.get(r'/delete/{ip:[\w.]+}', delete),
        web.get(r'/delete/{ip:[\w.]+}/{port:\d+}', delete)
    ]
)
web.run_app(app, host='127.0.0.1', port=8080)


async def read(request):
    ip = request.match_info.get('ip')
    port = request.match_info.get('port')
    resp = []
    async with asyncpg.connect(user='postgres') as conn:
        data = conn.fetch(f"SELECT * FROM services WHERE ip={ip}")
        for row in data:
            resp.append({
                'ip': row['ip'],
                'port': row['port'],
                'available': row['available']
            })

    return web.Response(body=json.dumps(resp), content_type='application/json')


async def create(request):
    pass


async def delete(request):
    pass

