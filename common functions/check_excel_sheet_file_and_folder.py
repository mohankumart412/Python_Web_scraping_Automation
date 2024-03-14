import os
import pandas as pd



excel_file_path = r"C:\Users\mohan.7482\Desktop\common functions\final_excel_sheet_AO 6001 to 7000.xlsx"
folder_path = r"C:\Users\mohan.7482\Desktop\SEBI data\AO_order\AO_order_pdf_files\Ao_order_pdf_files_6001_to_7000"

def find_file_in_excel_sheet():
    excel_data = pd.read_excel(excel_file_path)

    df = pd.DataFrame(excel_data)

    files_in_excel_sheet = set()

    for index, row in df.iterrows():
        files_in_excel_sheet.add(row['pdf_file_name'])

    # print(files_in_excel_sheet)
    return files_in_excel_sheet




def find_files_in_folder():

    files_in_folder = set()

    for _,_,files in os.walk(folder_path):
        for file in files:
            files_in_folder.add(file)

    # print(files_in_folder)
    return files_in_folder



def check_files():
    files_in_excel_sheets = find_file_in_excel_sheet()
    files_in_folder = find_files_in_folder()

    missing_files_in_folder = set()

    for file in files_in_excel_sheets:
        if not file in files_in_folder:
            missing_files_in_folder.add(file)
        
    if missing_files_in_folder:
        print(missing_files_in_folder,"missing files")
        print(len(missing_files_in_folder),"number of files missing in the folder")
    else:
        print("all the files in excel sheet are in the folder")


check_files()

