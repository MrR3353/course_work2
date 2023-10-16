import datetime
import os
import random
import string
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv

load_dotenv()

CHROME_DRIVER = os.environ.get('CHROME_DRIVER')


def register(login, password, email):
    login_input = driver.find_element(By.ID, 'form2Example1')
    login_input.clear()
    login_input.send_keys(login)

    email_input = driver.find_element(By.ID, 'form2Example2')
    email_input.clear()
    email_input.send_keys(email)

    password_input = driver.find_element(By.ID, 'form2Example3')
    password_input.clear()
    password_input.send_keys(password)

    repeat_password_input = driver.find_element(By.ID, 'form2Example4')
    repeat_password_input.clear()
    repeat_password_input.send_keys(password)

    driver.find_element(By.XPATH, '//button[text()="Регистрация"]').click()


def change_task(old_title, title, description, category, is_complete, starts):
    task_link = driver.find_element(By.LINK_TEXT, old_title)
    task_link.click()
    task_id = task_link.get_attribute('data-mdb-target')[1:]

    time.sleep(2)

    modal = driver.find_element(By.ID, task_id)
    title_input = modal.find_element(By.NAME, 'title')
    title_input.clear()
    title_input.send_keys(title)

    description_input = modal.find_element(By.NAME, 'description')
    description_input.clear()
    description_input.send_keys(description)

    category_input = Select(modal.find_element(By.CLASS_NAME, 'form-select'))
    category_input.select_by_visible_text(category)

    if is_complete:
        modal.find_element(By.NAME, 'is_complete').click()

    starts_input = modal.find_element(By.NAME, 'starts')
    driver.execute_script(f"arguments[0].value = '{starts}';", starts_input)

    time.sleep(1)
    save_button = WebDriverWait(modal, 1).until(EC.element_to_be_clickable((By.NAME, 'save-btn')))
    save_button.click()


def settings(tg_chat_id):
    dropdown = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown')))
    dropdown.click()
    driver.find_element(By.LINK_TEXT, "Настройки").click()

    is_notifications = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, 'is_notifications')))
    driver.execute_script("arguments[0].scrollIntoView();", is_notifications)
    time.sleep(1)
    is_notifications.click()
    time.sleep(1)
    tg_chat_id_input = driver.find_element(By.NAME, 'tg_chat_id')
    tg_chat_id_input.clear()
    tg_chat_id_input.send_keys(tg_chat_id)

    driver.find_element(By.XPATH, '//button[text()="Сохранить"]').click()


s = Service(executable_path=CHROME_DRIVER)
driver = webdriver.Chrome(service=s)


try:
    # driver.maximize_window()
    driver.get('http://localhost:8000')

    driver.find_element(By.LINK_TEXT, "Зарегистрироваться").click()
    login = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + "@gmail.com"

    register(login, password, email)
    settings(tg_chat_id=1377998876)

    task_manager_page = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.LINK_TEXT, "Менеджер задач")))
    task_manager_page.click()

    for i in range(1, 5):
        new_task_input = driver.find_element(By.ID, 'form2')
        new_task_input.send_keys(f'Task {i}')
        new_task_input.send_keys(Keys.ENTER)

    time.sleep(1)

    task_starts = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
    change_task('Task 1', 'Task 1', 'Some description', 'Новые', True, task_starts)
    time.sleep(1)

    task_starts = (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M")
    change_task('Task 3', 'Completed Task 3', 'Some description', 'Новые', True, task_starts)
    time.sleep(1)

    task_starts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
    change_task('Task 4', 'Updated Task 4', 'Some description', 'Срочные', False, task_starts)
    time.sleep(1)

    tab = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.LINK_TEXT, 'СРОЧНЫЕ')))
    tab.click()
    time.sleep(1)

    task_manager_page = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.LINK_TEXT, "Статистика")))
    task_manager_page.click()
    time.sleep(1)

    myDoughnutChart = driver.find_element(By.ID, "myDoughnutChart")
    driver.execute_script("arguments[0].scrollIntoView();", myDoughnutChart)

    time.sleep(5)
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()


