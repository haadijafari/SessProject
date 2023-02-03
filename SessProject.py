from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv

sess = 'https://sess.sku.ac.ir/'
user_pass = []
with open('user_pass.txt', 'r') as file:
    user_pass.append(file.readline())
    user_pass.append(file.readline())

driver = webdriver.Chrome()
driver.set_window_position(-10000, 0)
driver.get(sess)
driver.find_element(By.NAME, "edId").send_keys(user_pass[0])
driver.find_element(By.ID, "edPass").send_keys(user_pass[1])
driver.find_element(By.ID, "edEnter")._execute()
# [0] = Unit select | [1] = Other Actions | [2] = Exams | [3] = Sign up allowed check
driver.find_elements(By.TAG_NAME, "h6")[1].click()

# آموزشی
sleep(1)
driver.find_element(By.XPATH, "//label[@for=\'group-3\']").click()
sleep(1)
# لیست دروس نیمسال
driver.find_elements(By.TAG_NAME, 'li')[28].click()

Departments = ['بخش علوم كامپيوتر', 'بخش رياضي كاربردي', '']
for Dep in Departments:
    Select(driver.find_element(By.ID, 'edSemester')
           ).select_by_visible_text('دوم - 1401')
    Select(driver.find_element(By.ID, 'edDepartment')
           ).select_by_visible_text(Dep)
    driver.find_element(By.ID, 'edDisplay').click()
    doros = driver.find_elements(
        By.CLASS_NAME, 'listOdd') + driver.find_elements(By.CLASS_NAME, 'listEven')

    all_units = []
    for i in range(len(doros)):
        doros[i].click()
        html = html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        all_units.append([x.text for x in soup.find_all('div')[7:13]] +
                         [x.text for x in soup.find_all('div')[18:23]])
        driver.back()
        doros = driver.find_elements(
            By.CLASS_NAME, 'listOdd') + driver.find_elements(By.CLASS_NAME, 'listEven')

    fields = ['Unit name',
              'Unit count',
              'Unit code',
              'Group',
              'Class type',
              'Professor',
              'Time and Place',
              'Midterm date',
              'Midterm time',
              'Final date',
              'Final time']
    for i in all_units:
        with open('Units.csv', 'a', encoding="utf-8-sig") as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(all_units)