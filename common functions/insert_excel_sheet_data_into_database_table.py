import pandas as pd
import mysql.connector


host = 'localhost'
user = 'root'
password = 'root'
database = 'sebi'
auth_plugin = 'mysql_native_password'



connection = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = database,
    auth_plugin = auth_plugin
)


cursor = connection.cursor()


def insert_excel_data_to_mysql(final_excel_sheets_path, cursor):
    try:
        df = pd.read_excel(final_excel_sheets_path)

        table_name = "sebi_orders"
        
        df = df.where(pd.notnull(df), None)
        
        
      
        for index, row in df.iterrows():
            insert_query = f"""
                INSERT INTO {table_name} (date_of_order, title_of_order, type_of_order, link_to_order, pdf_file_path, pdf_file_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
           
            values = (row[0], row[1], row[3], row[2], row[6], row[4])

         
            cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(e)


final_excel_sheets_path = r"C:\Users\mohan.7482\Desktop\SEBI\pdfdownload\ed_cgm\processed.xlsx"
insert_excel_data_to_mysql(final_excel_sheets_path, cursor)