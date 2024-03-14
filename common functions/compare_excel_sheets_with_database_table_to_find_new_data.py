import sys
import pandas as pd
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine 

host = 'localhost'
user = 'root'
password = 'root'
database = 'sebi'
auth_plugin = 'mysql_native_password'

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    auth_plugin=auth_plugin

)
log_cursor = connection.cursor()

current_date = datetime.now().strftime("%Y-%m-%d")


def find_new_data(excel_file_path, db_table_name, type_sebi_text):
    global log_list
    try:
        database_uri = f'mysql://{user}:{password}@{host}/{database}?auth_plugin={auth_plugin}'
        engine = create_engine(database_uri)

        columns_to_select = ['date_of_order', 'title_of_order', 'link_to_order', 'type_of_order']
        select_query = f"SELECT {', '.join(columns_to_select)} FROM {db_table_name} WHERE type_of_order = 'Settlement Order';"
        database_table_df = pd.read_sql(select_query, con=engine)

        excel_columns_mapping = {'Date': 'date_of_order', 'Title': 'title_of_order', 'Link': 'link_to_order', 'type': 'type_of_order'}
        excel_columns_to_select = list(excel_columns_mapping.keys())

        excel_data_df = pd.read_excel(excel_file_path, usecols=excel_columns_to_select)
        excel_data_df.rename(columns=excel_columns_mapping, inplace=True)

        merged_df = pd.merge(excel_data_df, database_table_df, how='left', indicator=True)
        missing_rows = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

        if not missing_rows.empty:
            print("Rows from Excel Data not in Database Table")
            print(missing_rows)
            new_excel_file_path = rf"C:\Users\mohan.7482\Desktop\SEBI\incremental_excel_sheets\Missing_Data_{current_date}.xlsx"
            missing_rows.to_excel(new_excel_file_path, index=False)
            print(f"Missing rows saved to {new_excel_file_path}")

    except Exception as e:
        sys.exit("script error")

excel_file_path = r"C:\Users\mohan.7482\Desktop\SEBI\orders_Settlementorder_output.xlsx"
db_table_name = "sebi_orders"
find_new_data(excel_file_path, db_table_name)