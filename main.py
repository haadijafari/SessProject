from SessProject import *
from selenium import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome()
    #driver.set_window_position(-10000, 0)

    Departments = [ 'بخش رياضي كاربردي', 'بخش معارف اسلامي']
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

            
    logIn(driver)
    SemesterUnitListsPage(driver)
    ScrapeUnits(driver, fields, Departments)
