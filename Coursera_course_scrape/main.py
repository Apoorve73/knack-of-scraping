from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

def get_courses(path):

    # data dictionary
    data = {}
    # Time of Start of Code
    start = time.time()


    data['courses'] = list()

    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")

    page = 1
    url = f'https://www.coursera.org/search?query=python&page={page}&index=prod_all_products_term_optimization'

    driver = webdriver.Chrome(executable_path=path, options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # Open the website in the chromedriver
        driver.get(url)
        time.sleep(5)

        try:
            course_class = driver.find_element_by_class_name('ais-InfiniteHits')
            #print(course_class.text)
        except Exception as e:
            print(f'course_class error: {e}')

        try:
            uo_list = course_class.find_element_by_tag_name('ul')
            #print(uo_list.text)
        except Exception as e:
            print(f'uo_list error: {e}')

        try:
            list_items = uo_list.find_elements_by_tag_name('li')
        except Exception as e:
            print(f'list_items error: {e}')

        num = len(list_items)
        count = 0

        for item in list_items:

            try:
                item_card = item.find_element_by_class_name('card-info')
                #print(item_card.text)
            except Exception as e:
                print(f'item_card error: {e}')

            try:
                course_name = item_card.find_element_by_tag_name('h2').text
                #print(course_name.text)

            except Exception as e:
                print(f'course_name error: {e}')

            try:
                course_partner = item_card.find_element_by_class_name('partner-name').text

            except Exception as e:
                print(f'course_partner error : {e}')

            data['courses'].append(
                {
                    'Name': course_name,
                    'Offered By': course_partner
                }
            )

            count += 1
            print(f'{count}/{num} scraped')

            seconds = time.time() - start
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print("\t%d:%02d:%02d" % (h, m, s))
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    except Exception as e:
        print(f'driver.get error:\n {e}')

    try:
        with open('data.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f'Data Dumping Error: {e}')

    driver.quit()

get_courses('../chromedriver_linux/chromedriver')