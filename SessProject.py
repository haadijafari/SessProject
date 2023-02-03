from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
driver.get(sess)
user_bar = driver.find_element(By.NAME, "edId")
user_bar.send_keys(user_pass[0])
pass_bar = driver.find_element(By.ID, "edPass")
pass_bar.send_keys(user_pass[1])
pass_bar.send_keys(Keys.ENTER)

# logIn_button = driver.find_element(By.ID, "edEnter")
# logIn_button._execute()

OtherActs_button = driver.find_elements(By.TAG_NAME, "h6")
# [0] = Unit select
# [1] = Other Actions
# [2] = Exams
# [3] = Sign up allowed check
OtherActs_button[1].click()

# آموزشی
sleep(2)
driver.find_element(By.XPATH, "//label[@for=\'group-3\']").click()
sleep(1)
# لیست دروس نیمسال
buttons = driver.find_elements(By.TAG_NAME, 'li')
buttons[28].click()

select_semester = Select(driver.find_element(By.ID, 'edSemester'))
select_semester.select_by_visible_text('دوم - 1401')

select_department = Select(driver.find_element(By.ID, 'edDepartment'))
select_department.select_by_visible_text('بخش علوم كامپيوتر')
# select_department.select_by_visible_text('بخش علوم كامپيوتر')
# select_department.select_by_visible_text('بخش رياضي كاربردي)

display = driver.find_element(By.ID, 'edDisplay')
display.click()

doros = driver.find_elements(By.CLASS_NAME, 'listOdd')
doros2 = driver.find_elements(By.CLASS_NAME, 'listEven')
doros += doros2
all_units = []
for i in range(len(doros)):
    doros[i].click()
    html = html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_units.append([x.text for x in soup.find_all('div')[7:13]] +
                     [x.text for x in soup.find_all('div')[18:23]])
    driver.back()
    doros = driver.find_elements(By.CLASS_NAME, 'listOdd')
    doros2 = driver.find_elements(By.CLASS_NAME, 'listEven')
    doros += doros2
fields = [
            'Unit name',
            'Unit count',
            'Unit code',
            'Group',
            'Class type',
            'Professor',
            'Time and Place',
            'Midterm date',
            'Midterm time',
            'Final date',
            'Final time'
        ]
for i in all_units:
    with open('Units.csv', 'w', encoding="utf-8-sig") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(all_units)