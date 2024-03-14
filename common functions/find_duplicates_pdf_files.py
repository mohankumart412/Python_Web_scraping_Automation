import os
import hashlib

def find_duplicate_files_and_remove(folder_path):
    hash_dict = {}
    duplicate_files = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in hash_dict:
                duplicate_files.append(file_path)
            else:
                hash_dict[file_hash] = file_path

    for duplicate_file in duplicate_files:
        os.remove(duplicate_file)

    unique_files_count = len(hash_dict)
    duplicate_files_count = len(duplicate_files)

    return unique_files_count, duplicate_files_count, duplicate_files

folder_path = r'C:\Users\mohan.7482\Desktop\SEBI data\AO_order\AO_2000_4000\AO_2000_4000'
unique_count, duplicate_count, duplicates = find_duplicate_files_and_remove(folder_path)

print("Number of unique files:", unique_count)
print("Number of duplicate files:", duplicate_count)

if duplicates:
    print("Duplicate files removed:")
    for file in duplicates:
        print(file)
else:
    print("No duplicate files found in the folder.")
