#!usr/bin/env
import json
import csv
import requests # для отримання html-коду веб-сторінки за її URL'ом
from urllib.request import urlopen

import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Отримуємо код html-сторінки
def get_html(url):
    header_s = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    r = requests.get(url, headers = header_s) # Response    
    return r.text # повертає html-код сторінки (за адресою url)


# # # -------------------------------------------------------
# Декоратор для заміру часу виконання функції

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Функція {func.__name__} виконалася за {execution_time} секунд")
        return result
    return wrapper

# -------------------------------------------------------
# Декоратор для перехоплення та обробки винятків

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Помилка: {str(e)}")
            # Додаткові дії для обробки помилки

    return wrapper

# # -------------------------------------------------------

# @handle_exceptions
# @timer
# def data_processing(func):
#     def wrapper():
#         new_collection = func()
#         # Тут опрацьовуємо колекцію даних new_collection
#         pass
#     return wrapper

# # ---------------------------------------------------------

#     # GET

# # # Дістаємо дані з XML-файлу, через GET-запит
# # @data_processing
# # def get_xml_data(url):
# #     response = requests.get(url)
# #     return xmltodict.parse(response.content)


# # Дістаємо дані з JSON-файлу, через GET-запит
# @data_processing
# def get_json_data(url):
#     response = urlopen(url)
#     return json.loads(response.read())


# # Дістаємо дані з CSV-файлу, за адресою
# @data_processing
# def get_csv_data(url):
#     with open(url) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         return csv_reader


# # Прочитаємо дані з JSON-файлу
# def read_list_from_json_file(json_file_out):
#     with open(json_file_out, encoding="utf8") as write_file:
#         data = json.load(write_file)
#     return data

# # ---------------------------------------------------------

    # SAVE

# Зберігаємо дані до txt-файлу
def save_data_to_txt_file(name_file_txt, data):
    with open(name_file_txt, 'at') as txt_file:
        txt_file.write(data)


# Запишемо зпарсені дані до JSON-файлу
def save_data_to_json_file(some_data, json_file_in):
    with open(json_file_in, "a", encoding="utf8") as write_file:
        json.dump(some_data, write_file, indent=4, ensure_ascii=False)

# ---------------------------------------------------------

# def create_obj_bs4(base_url):
#     html_doc = get_html(base_url)
#     soup = BeautifulSoup (html_doc, 'html.parser')
#     return soup


def get_size_of_file_before_downloading(url):
    size_file = int(requests.head(url).headers['Content-Length'])
    return size_file # in Mb


# Завантажуємо один pdf-файл
def pdf_file_to_save(url_dis_pdf, new_name_file):
    response = requests.get(url_dis_pdf)
    with open(new_name_file, 'wb') as f:
        f.write(response.content)



# Сортування словника dictionary
def get_sortedDict(dictionary):
	return sorted(dictionary.items(), key = lambda kv:(kv[1], kv[0]))



# # -------------------------------------------------------
# Декоратор для обмеження частоти виклику функції

def throttle(wait_time):
    def decorator(func):
        last_excecution_time = 0

        def wrapper(*args, **kwargs):
            nonlocal last_excecution_time
            current_time = time.time()
            if current_time - last_excecution_time > wait_time:
                last_excecution_time = current_time
                return func(*args, **kwargs)
            else:
                print("Зачекайте, поки мине часовий інтервал")
        return wrapper
    return decorator

# # -------------------------------------------------------

@throttle(5) # Обмеження виклику раз на 5 секунд
def send_input(driver, city, attr_txt_box):
    # tbox = driver.find_element("class name", "ui-autocomplete-input")   # identify text box
    tbox = driver.find_element("name", attr_txt_box)   # identify text box
    tbox.send_keys(city)   # send input
    tbox.send_keys(Keys.RETURN)   # send keyboard input



# ---------------------------------------------------------------------------

def main():
    driver = webdriver.Chrome()
    base_url = 'https://booking.uz.gov.ua/'    
    driver.get(base_url)   # open link
    
    # # tbox = driver.find_element("class name", "ui-autocomplete-input")   # identify text box
    # tbox = driver.find_element("name", "from-title")   # identify text box
    # tbox.send_keys("Київ")   # send input
    # tbox.send_keys(Keys.RETURN)   # send keyboard input

    # tbox = driver.find_element("name", "to-title")   # identify text box
    # tbox.send_keys("Львів")   # send input
    # tbox.send_keys(Keys.RETURN)   # send keyboard input

    city = "Київ"
    attr_txt_box = "from-title"
    send_input(driver, city, attr_txt_box)

    city = "Львів"
    attr_txt_box = "to-title"
    send_input(driver, city, attr_txt_box)
    
    # scroll down
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
               
    # # Знаходимо кнопку за атрибутами data-from-code та data-to-code
    # # button = driver.find_element_by_css_selector('button[data-from-code="2200001"][data-to-code="2218000"]')
    # button = driver.find_element_by_css_selector(button['submit'])

    # # Натискаємо на кнопку
    # button.click()

    # Закриваємо драйвер
    driver.quit()
    
# ===========================================================================================


if __name__ == '__main__':
    main()