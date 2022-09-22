import os
from time import sleep
from login import login
import requests
from selenium.webdriver.common.keys import Keys


def spell_check(name):
    symbs = ('/', '\\', '<', '>', ':', '*', '"', '|', '?')
    for symb in symbs:
        if symb in name:
            name = name.replace(symb, '')
    return name

def parse(driver, lesson, lib, number, error = False):
    driver.get(lesson[1])
    name = spell_check(lesson[0][0])
    lib_name = spell_check(lesson[0][1])
    lib_number = lesson[0][2]
    sleep(2)
    try:
        url = driver.find_element_by_css_selector('.vjs-tech').get_attribute('src')
    except:
        if error:
            print('aborted due to stale video element')
            raise ValueError
        else:
            parse(driver, lesson, lib, number, True)
    r = requests.get(url)
    try:
        os.mkdir(os.getcwd() + f'/{lib[:-1]}/{lib_number}.{lib_name}')
    except FileExistsError:
        pass
    with open(f'{lib[:-1]}/{lib_number}.{lib_name}/{number}.{name}.mp4','wb') as f:  
        f.write(r.content)
    return number + 1

with open('C:\Python\Projects\pl_sight\parsed_links.txt', 'r', encoding = 'utf-8') as f:
    start = f.readlines()
if start[0] == 'None':
    got_start = True
else:
    got_start = False
    
driver = login()
find = driver.find_element_by_css_selector
find_many = driver.find_elements_by_css_selector
            
with open('selected_links.txt', 'r', encoding = 'utf-8') as file:
    os.chdir(os.path.dirname(__file__) + '/courses')
    for link in file:
        if start[0] != link and not got_start:
            continue
        driver.get(link)
        sleep(1)
        sections = find_many('.drawer---2bAtz')
        titles = [x.text for x in find_many('.table-of-contents__title')]
        count = 0
        lessons_titles = []
        lessons_links = []
        btn = find('.buttonLink---KymJM')
        for section in sections:
            section.click()
            lessons_titles += [(x.text, titles[count], count + 1) for x in find_many('.clipListTitle---hbKca') if x.text != '']
            lessons_links += [x.get_attribute('href') for x in find_many('.clipListTitle---hbKca') if x.text != '']
            count += 1
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            for _ in range(2):
                sleep(0.5)
                btn.click()
            sleep(1)
        lessons = [(lessons_titles[x],lessons_links[x]) for x in range(len(lessons_titles))]
        number = int(start[2]) if not got_start else 1
        for lesson in lessons:
            if lesson[1] != start[1][:-1] and not got_start:
                continue
#defines will acc be banned or not
            sleep(5)
            number = parse(driver, lesson, link.split('/')[-1], number)
            print('got element #', number - 1)
            with open('C:\Python\pl_sight\parsed_links.txt', 'w', encoding = 'utf-8') as f:
                f.write(link + lesson[1] + '\n' + str(number))
            got_start = True
            
