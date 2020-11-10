from aiohttp import web

import json
import asyncpg


async def read(request):
    ip = request.match_info.get('ip')
    port = request.match_info.get('port')
    query = f"SELECT * FROM services WHERE ip={ip}"
    if port:
        query = f"SELECT * FROM services WHERE ip='{ip}' AND port={int(port)}"
    
    resp = []
    conn = await asyncpg.connect(user='postgres')
    data = await conn.fetch(query)
    await conn.close()
    for row in data:
        resp.append({
            'ip': row['ip'],
            'port': row['port'],
            'available': row['available']
        })

    return web.Response(body=json.dumps(resp), content_type='application/json')


async def create(request):
    query = "INSERT INTO services (ip, port, available) VALUES ({}, {}, {})"
    data = await request.json()
    async with asyncpg.connect(user='postgres') as conn:
        conn.execute(query.format(data['ip'], data['port'], data['available']))

    return web.Response(body=json.dumps({'success': True}), content_type='application/json')


async def delete(request):
    query = f"DELETE * FROM services WHERE ip={ip}"
    ip = request.match_info.get('ip')
    port = request.match_info.get('port')
    if port:
        query = f"DELETE * FROM services WHERE ip={ip} AND port={int(port)}"

    return web.Response(body=json.dumps({'success': True}), content_type='application/json')


async def init_db(app):
    conn = await asyncpg.connect(user='postgres')
    await conn.execute(
        '''
            CREATE TABLE IF NOT EXISTS services (
                id serial NOT NULL,
                ip varchar NOT NULL,
                port integer NOT NULL,
                available boolean NOT NULL,
                PRIMARY KEY (id)
            )
            '''
    )
    await conn.close()


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
app.on_startup.extend([init_db])
web.run_app(app, host='127.0.0.1', port=8080)
