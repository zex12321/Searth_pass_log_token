import os
import re
import pandas as pd
import json
from docx import Document
from tqdm import tqdm

# Путь к папке с данными
data_path = 'leak_data'
results = []

# Папка для сохранения результатов
output_folder = 'extracted_results'
os.makedirs(output_folder, exist_ok=True)

# регулярные выражения для поиска логинов и паролей
login_password_pattern = re.compile(r'login:\s*(\S+),\s*password:\s*(\S+)')
token_pattern = re.compile(r'"token":\s*"(\S+)"')

# Функция для извлечения данных из текстовых (txt), CSV, JSON, DOCX, MD и XLSX файлов
def extract_data(file_path):
    if file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                matches = login_password_pattern.findall(content)
                for match in matches:
                    results.append({'login': match[0], 'password': match[1], 'token': None})
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
                matches = login_password_pattern.findall(content)
                for match in matches:
                    results.append({'login': match[0], 'password': match[1], 'token': None})

    elif file_path.endswith('.csv'):
        try:
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                login = row.get('login')
                password = row.get('password')
                if login and password:
                    results.append({'login': login, 'password': password, 'token': None})
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    elif file_path.endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                for entry in json_data:
                    if 'login' in entry and 'password' in entry:
                        results.append({'login': entry['login'], 'password': entry['password'], 'token': entry.get('token')})
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    elif file_path.endswith('.docx'):
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                matches = login_password_pattern.findall(para.text)
                for match in matches:
                    results.append({'login': match[0], 'password': match[1], 'token': None})
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    elif file_path.endswith('.md'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                matches = login_password_pattern.findall(content)
                for match in matches:
                    results.append({'login': match[0], 'password': match[1], 'token': None})
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
                matches = login_password_pattern.findall(content)
                for match in matches:
                    results.append({'login': match[0], 'password': match[1], 'token': None})

    elif file_path.endswith('.xlsx'):
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                login = row.get('login')
                password = row.get('password')
                if login and password:
                    results.append({'login': login, 'password': password, 'token': None})
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Проходим через все файлы в папке
for filename in os.listdir(data_path):

    file_path = os.path.join(data_path, filename)
    if os.path.isfile(file_path) and (filename.endswith('.txt') or filename.endswith('.csv') or filename.endswith('.json') or 
                                       filename.endswith('.docx') or filename.endswith('.md') or filename.endswith('.xlsx')):
        extract_data(file_path)

# Проверка, были ли найдены результаты
if results:
    results_df = pd.DataFrame(results)

# Проверка, были ли найдены результаты
if results:
    results_df = pd.DataFrame(results)

    # Запись результатов в отдельный TXT файл в новой папке
    output_file_path = os.path.join(output_folder, 'extracted_data.txt')
    with open(output_file_path, 'w') as output_file:
        for index, row in tqdm(results_df.iterrows(), total=results_df.shape[0], desc="Сохранение данных"):
            output_file.write(', '.join(map(str, row.values)) + '\n')
    
    print(f"Results saved to {output_file_path}")
else:
    print("No data found in the specified files.")