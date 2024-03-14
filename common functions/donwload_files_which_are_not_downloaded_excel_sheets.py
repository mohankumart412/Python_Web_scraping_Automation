import os
import time
import traceback
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_path = "pdfdownload"

sub_path = "settlementorder_pdf"



download_folder = r"C:\Users\mohan.7482\Desktop\SEBI\downloaded_files\settlement_order_files"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--disable-notifications")  
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})








def download_pdf(link):

    # file_name = " "

    try:
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(link)
        time.sleep(5)
        browser.maximize_window()
    except Exception as e:
        traceback.print_exc()
        value = "None"
        return value


    try:
        iframe_tag = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe"))
        )

        src_value = iframe_tag.get_attribute("src")
        file_name = src_value.split("/")[-1]
        print(file_name)
    

        browser.switch_to.frame(iframe_tag)
        time.sleep(5)
        download_button = browser.find_element(By.XPATH, '//*[@id="download"]')
        time.sleep(5)
        download_button.click()
        time.sleep(10)
        print(f"File {file_name} downloaded.")
        browser.quit()
    except Exception as e:
        traceback.print_exc()
        return "There is no pdf file to download"
    return file_name



def process_excel_data(excel_file_path):
    excel_data = pd.read_excel(excel_file_path)
    df = pd.DataFrame(excel_data)
    for index, row in df.iterrows():
        if pd.isna(row['pdf_file_name']) or pd.isna(row['pdf_path']):
            link = row['Link']
            try:
                pdf_file_name = download_pdf(link)
                df.at[index, 'pdf_file_name'] = pdf_file_name
                if pdf_file_name == "There is no pdf file to download":
                    df.at[index, 'pdf_path'] = "There is no pdf file to download"
                elif pdf_file_name == "None":
                    df.at[index, 'pdf_path'] = "None"
                else:
                    df.at[index, 'pdf_path'] = os.path.join(base_path, sub_path, pdf_file_name)
                print(row)
                type_sebi_text = "settlement_order_pdf_files"
                final_excel_name = f'final_excel_sheet_{type_sebi_text}.xlsx'
                final_excel_file_with_pdf_path = fr"C:\Users\mohan.7482\Desktop\SEBI\additonal excel sheets\{final_excel_name}"
                df.to_excel(final_excel_file_with_pdf_path, index=False)
            except Exception as e:
                print(f"Failed to download file for row {index}: {e}")
                continue



excel_file_path = r"C:\Users\mohan.7482\Desktop\SEBI\final_excel_sheets\final_excel_sheet_Settlement Order.xlsx"
process_excel_data(excel_file_path)
    

