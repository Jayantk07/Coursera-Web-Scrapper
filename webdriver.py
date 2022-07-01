from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from datetime import date
import sys


course_title = []
course_organization = []
course_URL =[]
course_Certificate_type = []
course_rating = []
course_difficulty = []
course_students_enrolled = []
course_image_URL = []
course_image_name=[]

def find_courses(source):
    pgcn = BeautifulSoup(source, 'html.parser')
    if pgcn is None:
        print("Page not found")
    else:
        courses = pgcn.find_all("li", {'class': 'ais-InfiniteHits-item'})
        for course in courses:
            try:
                # Course Title
                ct = course.h2.get_text()
                course_title.append(ct)

                # Course Organization
                co = course.find('span', {'class': 'css-1cxz0bb'}).get_text()
                course_organization.append(co)

                # Course URL
                cu = course.find('a', {'class': 'result-title-link'})
                course_URL.append("https://www.coursera.org" + cu.get('href'))

                # Course Certification Type
                cc = course.find('span', {'class': 'css-yg35ph'})
                course_Certificate_type.append(cc)

                # Course Rating
                cr = course.find('span', {'class': 'ratings-text'}).get_text()
                course_rating.append(cr)

                # Course Difficulty
                cd = course.find('span', {'class': 'difficulty'}).get_text()
                course_difficulty.append(cd)


                # Course Enrollment
                ce = course.find('span', {'class': 'enrollment-number'}).get_text()
                course_students_enrolled.append(ce)


                # Course Image URL
                ci = course.find('img')
                course_image_URL.append("" + ci.get('src'))


                # Course Image Alt
                cn = course.find('img')
                course_image_name.append("" + cn.get('alt'))


                print(f"Course Title: \t {ct}")
                print(f"Course Organization: \t {co}")
                print(f"Course URL: \t {cu}")
                print(f"Course Certification Type: \t {cc}")
                print(f"Course Rating: \t {cr}")
                print(f"Course Difficulty: \t {cd}")
                print(f"Course Enrollment: \t {ce}")
                print(f"Course Image URL: \t {ci}")
                print(f"Course Image Name: \t {cn}")


                print('\n' + '|' + ('<' * 3) + ('-' * 7) + ' New Course ' + ('-' * 7) + ('>' * 3) + '|' + '\n')
            except:
                print("Something went wrong when printing the courses")

keyword = ["recruiter"]
url = "https://www.coursera.org/search?query="+keyword+"&index=prod_all_launched_products_term_optimization"


locationOfWebdriver = "E:/Downloads/Web Driver/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(locationOfWebdriver)
driver.get(url)
driver.implicitly_wait(10)
for i in range(6):
    element = driver.find_element_by_xpath('//button[@aria-label = "Next Page"]')
    ActionChains(driver).move_to_element(element).perform()
    find_courses(driver.page_source)
    ActionChains(driver).click().perform()
    driver.implicitly_wait(10)
driver.quit()



# print(len(course_title))
# print(len(course_organization))
# print(len(course_URL))
# print(len(course_Certificate_type))
# print(len(course_rating))
# print(len(course_difficulty))
# print(len(course_students_enrolled))
# print(len(course_image_URL))
# print(len(course_image_name))

# creating a dataframe gathering the list
coursera_df = pd.DataFrame.from_dict({'course_title': course_title,
                            'course_organization': course_organization,
                            'course_URL': course_URL,
                            'course_Certificate_type' : course_Certificate_type,
                            'course_rating': course_rating,
                            'course_difficulty': course_difficulty,
                            'course_students_enrolled': course_students_enrolled,
                            'course_icon': course_image_URL,
                            'image_name': course_image_name}, orient='index')
coursera_df= coursera_df.transpose()


coursera_df.to_csv('Recruiter_Coursera_catalog.csv')