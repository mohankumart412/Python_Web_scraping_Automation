import os
import shutil
import pandas as pd



main_folder_path = r"C:\Users\mohan.7482\Desktop\SEBI\pdfdownload\settlementorder_pdf"

existing_so_file_path = r"C:\Users\mohan.7482\Desktop\SEBI data\SO_order\SO_order_pdf_files"
print(existing_so_file_path)
excel_file_path = r"C:\Users\mohan.7482\Desktop\SEBI\orders_Settlementorder_output.xlsx"

excel_data = pd.read_excel(excel_file_path)

df = pd.DataFrame(excel_data)

years = set()

months = set()

final_rows = set()


def save_to_excel():
    new_df = pd.DataFrame(final_rows)
    new_excel_file_path = os.path.join(main_folder_path, "processed.xlsx")
    new_df.to_excel(new_excel_file_path, index=False)





# def move_files(selected_month_rows, year_folder_path, month, year):
#     files = set()
#     for row in selected_month_rows:
#         files.add(row[4])
#     print(files, f"these are the files{month}{year}")
#     month_folder_path = os.path.join(year_folder_path, month)  # Moved outside the loop
#     if not os.path.exists(month_folder_path):  # Check if the month directory exists
#         os.makedirs(month_folder_path)
#     else:
#         print(month, "it is already exists")
#     for file in files:
#         old_file_path = os.path.join(old_files_path, file)
#         new_file_path = os.path.join(month_folder_path, file)
#         print(new_file_path, "file path")
#         shutil.move(old_file_path, new_file_path)



def move_files(selected_month_rows, year_folder_path, month, year):
    for row in selected_month_rows:
        file = row[5]
        month_folder_path = os.path.join(year_folder_path, month) 
        print(month_folder_path) # Moved outside the loop
        if not os.path.exists(month_folder_path):  # Check if the month directory exists
            os.makedirs(month_folder_path)
        else:
            print(month, "it is already exists")

        print(existing_so_file_path,'old file path')
        old_file_path = os.path.join(existing_so_file_path,file)
        print(old_file_path,"after join")
        new_file_path = os.path.join(month_folder_path,file)
        print(new_file_path, "newe file path after join")

        
        shutil.move(old_file_path, new_file_path)
        _,_,relative_path = new_file_path.partition('SEBI')
        relative_path = relative_path.replace('\\','/')
        final_rows.add(row + (relative_path,))



def create_year_folders(selected_year_rows,year,months):
    year_folder_path = os.path.join(main_folder_path,year)
    if not os.path.exists(year_folder_path):
        os.makedirs(year_folder_path)
    else:
        print(year,"the folder is already exists")
    for month in months:
        selected_month_rows = set()   
        for row in selected_year_rows:
            if month in row[0]:
                selected_month_rows.add(row)
                # print(row)
        # print(selected_month_rows)
        move_files(selected_month_rows,year_folder_path,month,year)



def select_year_wise(months,years):
    for year in years:
        selected_year_rows = set()
        for index, row in df.iterrows():
            if year in row['Date']:
                selected_year_rows.add(tuple(row))
        print(year)
        # print(selected_year_rows)
        create_year_folders(selected_year_rows,year,months)
    save_to_excel()



for index, row in df.iterrows():
    month_year = row['Date'] 
    parts = month_year.split(", ")
    year = parts[-1]
    years.add(year)
    month = parts[0].split()[0]  
    months.add(month)
select_year_wise(months,years)

print(months,"months in ewxcel sheets")
print(years,"years in the excel sheets")