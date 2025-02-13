import requests as req
import pandas as pd
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from clickhouse_driver import Client

URL = 'http://www.cbr.ru/scripts/XML_daily.asp'
DATE = '01/01/2024'

CH_CLIENT = Client(
    host='localhost',
    user='default',
    password='default',
    database='default'
)


def extract_date(url, date, s_file):
    request = req.get(f"{url}?date_req={date}")

    with open(s_file, 'w', encoding="utf-8") as tmp_file:
        tmp_file.write(request.text)


def transform_data(s_file, csv_file, date):
    rows = list()

    parser = ET.XMLParser(encoding='utf-8')

    tree = ET.parse(s_file, parser=parser).getroot()

    for child in tree.findall("Valute"):
        num_code = child.find("NumCode").text
        char_code = child.find("CharCode").text
        nominal = child.find("Nominal").text
        name = child.find("Name").text
        value = child.find("Value").text

        rows.append((num_code, char_code, nominal, name, value))

    date_frame = pd.DataFrame(
        rows,
        columns=["num_code", "char_code", "nominal", "name", "value"]
    )

    date_frame['date'] = date

    date_frame.to_csv(csv_file, sep=",", encoding="utf-8", index=False)


def upload_data(csv_file, table_name, client):
    data_frame = pd.read_csv(csv_file)

    client.execute(
        f'CREATE TABLE IF NOT EXISTS {table_name} (num_code Int64, char_code String, nominal Int64, name String, value String, date String) ENGINE Log'
    )

    client.execute(f'INSERT INTO {table_name} VALUES ', data_frame.to_dict('records'))


def check_and_delete_data(date, table_name, client):
    query_check = f"SELECT COUNT(*) FROM {table_name} WHERE date='{date}'"

    result = client.execute(query_check)

    if result[0][0] > 0:
        query_delete = f"DELETE FROM {table_name} WHERE date='{date}'"
        client.execute(query_delete)


extract_date(URL, DATE, 'currency')

transform_data('currency', 'currency.csv', DATE)

check_and_delete_data(date=DATE, table_name='currency_data', client=CH_CLIENT)

upload_data(
    csv_file='currency.csv',
    table_name='currency_data',
    client=CH_CLIENT
)
