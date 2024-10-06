from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import csv


def logIn(driver):
    sess = 'https://sess.sku.ac.ir/'
    user_pass = []
    with open('user_pass.txt', 'r') as file:
        user_pass.append(file.readline())
        user_pass.append(file.readline())
    driver.get(sess)
    sleep(0.5)
    driver.find_element(By.NAME, "edId").send_keys(user_pass[0])
    driver.find_element(By.ID, "edPass").send_keys(user_pass[1])
    sleep(0.5)
    display = driver.find_element(By.ID, "edEnter")
    display.click()
    # [0] = Unit select | [1] = Other Actions | [2] = Exams | [3] = Sign up allowed check
    print(driver.find_elements(By.XPATH, "//*[@id=\'ParentForm\']/div[4]/section/div[2]/section/div/div[2]/div/div/div/div[3]"))
    driver.find_elements(By.XPATH, "//*[@id=\'ParentForm\']/div[4]/section/div[2]/section/div/div[2]/div/div/div/div[3]")[0].click()


def SemesterUnitListsPage(driver):
    # آموزشی
    sleep(1)
    driver.find_element(By.XPATH, "//label[@for=\'group-3\']").click()
    sleep(1)
    # لیست دروس نیمسال
    driver.find_elements(By.TAG_NAME, 'li')[28].click()


def ScrapeUnits(driver, fields, Departments):
    for Dep in Departments:
        dep_units = []
        Select(driver.find_element(By.ID, 'edSemester')
            ).select_by_visible_text('اول - 1403')
        Select(driver.find_element(By.ID, 'edDepartment')
            ).select_by_visible_text(Dep)
        driver.find_element(By.ID, 'edDisplay').click()
        sleep(0.5)
        doros = driver.find_elements(By.XPATH, "//td[@align=\'center\']")

        for i in range(1, len(doros)):
            doros[i].click()
            html = html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            dep_units.append([x.text for x in soup.find_all('div')[7:13]] +
                            [x.text for x in soup.find_all('div')[18:23]])
            driver.back()
            doros = driver.find_elements(By.XPATH, "//td[@align=\'center\']")

        CSVWriter(fields,dep_units,Dep)


def CSVWriter(fields, data, Dep):
    for i in data:
        with open('%s.csv' % Dep, 'w', encoding="utf-8-sig") as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(data)
