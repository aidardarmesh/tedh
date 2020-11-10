import asyncpg
import socket

'''
crontab -e
* * * * *              /path/to/this/script/
* * * * * ( sleep 30 ; /path/to/this/script/ )
'''

a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def healthcheck(ip, port):
    return a_socket.connect_ex((ip, port)) == 0


def main():
    conn = await asyncpg.connect(user='postgres')
    data = await conn.execute("SELECT * FROM services")
    for row in data:
        ip, port = row['ip'], row['port']
        await conn.execute(f"UPDATE services SET available={healthcheck(ip, port)} WHERE ip='{ip}' AND port={port}")
    await conn.close()
