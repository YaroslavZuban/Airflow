import requests as req
import pandas as pd
from datetime import datetime, timedelta
from datetime import date
from clickhouse_driver import Client
import os
from dotenv import load_dotenv
import json

load_dotenv()

KEY_API = os.getenv('KEY_API_EXCHANGE_RATE')
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

URL = f'https://v6.exchangerate-api.com/v6/{KEY_API}/latest/RUB'

CH_CLIENT = Client(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)


def extract_date(url, s_file):
    request = req.get(f"{url}")

    with open(s_file, 'w', encoding="utf-8") as tmp_file:
        tmp_file.write(request.text)


def transform_data(s_file, csv_file, today):
    rows = list()

    with open(s_file, 'r') as file:
        data = json.load(file)

    base_code = data['base_code']
    conversion_rates = data['conversion_rates']

    for currency, rate in conversion_rates.items():
        rows.append((base_code, currency, rate, today))

    date_frame = pd.DataFrame(
        rows,
        columns=["base_code", "conversion_rate", "rate", "today"]
    )

    date_frame['date'] = date

    date_frame.to_csv(csv_file, sep=",", encoding="utf-8", index=False)


def upload_data(csv_file, table_name, client):
    data_frame = pd.read_csv(csv_file)

    client.execute(
        f'CREATE TABLE IF NOT EXISTS {table_name} (base_code String, conversion_rate String, rate float, date String) ENGINE Log'
    )

    client.execute(f'INSERT INTO {table_name} VALUES ', data_frame.to_dict('records'))


def check_and_delete_data(table_name, client, today):
    query_check = f"SELECT COUNT(*) FROM {table_name} WHERE date='{today}'"

    result = client.execute(query_check)

    if result[0][0] > 0:
        query_delete = f"DELETE FROM {table_name} WHERE date='{today}'"
        client.execute(query_delete)


extract_date(URL, 'home_work_2/currency.json')

transform_data('home_work_2/currency.json', 'currency.csv')

check_and_delete_data(table_name='exchange_rate', client=CH_CLIENT)

upload_data(
    csv_file='home_work_2/currency.csv',
    table_name='exchange_rate',
    client=CH_CLIENT
)
