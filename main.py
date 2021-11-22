import subprocess
import sqlite3
from datetime import datetime

from fastapi import FastAPI
from pypika import Query, Column
from pydantic.dataclasses import dataclass


conn = sqlite3.connect('results.db', check_same_thread=False)
create = Query.create_table('results').columns(
    Column('timestamp', 'text', nullable=False),
    Column('server', 'text', nullable=False),
    Column('latency', 'text', nullable=False),
    Column('download', 'text', nullable=False),
    Column('upload', 'text', nullable=False)
).if_not_exists()
conn.execute(str(create))


app = FastAPI()


@dataclass
class Results:
    timestamp: str
    server: str
    latency: str
    download: str
    upload: str


def insert_results(result: Results):
    insert = Query.into('results').insert(
        result.timestamp, result.server, result.latency, result.download, result.upload
    )
    conn.execute(str(insert))
    conn.commit()


def run_speedtest() -> Results:
    out = subprocess.run(['speedtest-cli'], capture_output=True)
    output = out.stdout.decode().split('\n')

    server, latency = output[4].split(': ')
    download = output[6].split(': ')[1]
    upload = output[8].split(': ')[1]
    timestamp = datetime.now().isoformat()
    return Results(timestamp, server, latency, download, upload)


@app.get('/run-test')
async def run_and_insert():
    try:
        res = run_speedtest()
        insert_results(res)
        return {'success': True, 'results': res}
    except Exception as err:
        return {'success': False, 'error': str(err)}


@app.get('/get-all-results')
async def get_all_results() -> dict[str, list[Results]]:
    cursor = conn.cursor()
    cursor.execute('select * from results;')
    results = [Results(*res) for res in cursor.fetchall()]
    cursor.close()
    return {'results': results}
