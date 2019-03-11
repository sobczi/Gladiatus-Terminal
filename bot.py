from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os
import sys
import os.path

def clear(): return os.system('clear')

# selenium help functions


def search_element(path):
    list_elements = driver.find_elements_by_xpath(str(path))
    if len(list_elements) != 0:
        return True
    else:
        return False


def get_element(path):
    while not search_element(path):
        time.sleep(1)

    return driver.find_element_by_xpath(path)


def move_move(path1, path2):
    time.sleep(0.250)
    action = ActionChains(driver)
    wait_for_element(path1)
    element = driver.find_element_by_xpath(path1)
    action.click_and_hold(element)
    wait_for_element(path2)
    element2 = driver.find_element_by_xpath(path2)
    action.move_to_element(element2)
    action.perform()
    return


def drag_and_drop(path1, path2):
    action = ActionChains(driver)
    wait_for_element(path1)
    element1 = driver.find_element_by_xpath(path1)
    wait_for_element(path2)
    element2 = driver.find_element_by_xpath(path2)
    action.drag_and_drop(element1, element2).perform()


def release(path1):
    time.sleep(0.250)
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(path1)
    action.move_to_element(element)
    action.release(element)
    action.perform()
    return


def click_element(variable):
    check_events()
    if isinstance(variable, str):
        variable = get_element(variable)

    variable.click()
    return


def wait_for_element(path):
    while not search_element(path):
        time.sleep(0.05)
    return

# gladiatus: system functions


def display_info():
    hp = get_hp_value()
    hp = hp + "%"
    progress = driver.find_element_by_id('header_values_xp_percent').text

    gold = driver.find_element_by_id('sstat_gold_val').text
    rubles = driver.find_element_by_id('sstat_ruby_val').text

    level = driver.find_element_by_id('header_values_level').text
    rank = driver.find_element_by_id('highscorePlace').text
    print("Player: " + username + ", World: " + server + ", HP: " + hp)
    print("Level: " + level + ", Progress: " + progress + ", Rank: " + rank)
    print("Gold: " + gold + ", Rubles: " + rubles)
    print()
    return


def return_false_true(variable):
    if variable == 'True':
        return True
    else:
        return False


def read_settings(variable):
    lines = [line.rstrip('\n') for line in open('settings_bot'+str(variable))]
    for line in lines:
        if 'login' in line:
            login = re.findall("\'(.*?)\'", line)
        elif 'password' in line:
            password = re.findall("\'(.*?)\'", line)
        elif 'server' in line:
            server = re.findall("\'(.*?)\'", line)
        elif 'expedition_option' in line:
            expedition_option = re.findall("\'(.*?)\'", line)
        elif 'expedition' in line:
            expedition_enabled = re.findall("\'(.*?)\'", line)
        elif 'minimum_value_for_packing_gold' in line:
            val_pack_gold = re.findall("\'(.*?)\'", line)
            val_pack_gold[0] = val_pack_gold[0].replace(" ", "")
        elif 'pack_gold' in line:
            pack_gold_enabled = re.findall("\'(.*?)\'", line)
        elif 'dungeon_advenced' in line:
            dungeon_option = re.findall("\'(.*?)\'", line)
        elif 'dungeon' in line:
            dungeon_enabled = re.findall("\'(.*?)\'", line)
        elif 'health_level' in line:
            health = re.findall("\'(.*?)\'", line)
        elif 'pack_backpack' in line:
            backpack = re.findall("\'(.*?)\'", line)
            backpack[0] = type_backpack(backpack[0])
        elif 'food_backpack' in line:
            backpack_food = re.findall("\'(.*?)\'", line)
            backpack_food[0] = type_backpack(backpack_food[0])
        elif 'headless' in line:
            headless = re.findall("\'(.*?)\'", line)
        elif 'sell_items' in line:
            sell_items = re.findall("\'(.*?)\'", line)

    expedition_enabled[0] = return_false_true(expedition_enabled[0])
    dungeon_enabled[0] = return_false_true(dungeon_enabled[0])
    dungeon_option[0] = return_false_true(dungeon_option[0])
    pack_gold_enabled[0] = return_false_true(pack_gold_enabled[0])
    headless[0] = return_false_true(headless[0])
    sell_items[0] = return_false_true(sell_items[0])

    return login[0], password[0], server[0], expedition_enabled[0],\
        expedition_option[0], pack_gold_enabled[0], val_pack_gold[0],\
        dungeon_enabled[0], dungeon_option[0], health[0],\
        backpack[0], backpack_food[0], headless[0], sell_items[0]

# gladiatus: navigation functions


def guild_market():
    while search_element("//a[contains(@href,'guildMarket')][@class='map_label']") == False:
        click_element("//a[text() = 'Gildia']")
        time.sleep(1)
    click_element("//a[contains(@href,'guildMarket')][@class='map_label']")

    while search_element("//div[@id='market_sell_box']//section[@style='display: none;']"):
        click_element("//h2[@class='section-header'][text() = 'sprzedaj']")

    return


def packages():
    driver.find_element_by_id('menue_packages').click()
    if search_element("//section[@style='display: none;']"):
        click_element(
            "//h2[@class='section-header'][contains(text(), 'Opcje')]")
    return


def filter_packages(first, second):
    if isinstance(first,int) and isinstance(second, int):
        click_element("//select[@name = 'f']//option[text() = '" + str(get_category_packages(first)) + "']")
        click_element("//select[@name = 'fq']//option[text() = '" + str(quality_pack(second)) + "']")
    elif isinstance(first, int) and not isinstance(second, int):
        click_element("//select[@name = 'f']//option[text() = '" + str(get_category_packages(first)) + "']")
        click_element("//select[@name = 'fq']//option[text() = '" + str(second) + "']")
    elif not isinstance(first, int) and isinstance(second, int):
        click_element("//select[@name = 'f']//option[text() = '" + str(first) + "']")
        click_element("//select[@name = 'fq']//option[text() = '" + str(quality_pack(second)) + "']")
    click_element("//input[@value = 'Filtr']")
    return


def open_backpack(variable):
    click_element("//a[@data-bag-number='"+variable+"']")
    wait_for_element("//a[@data-bag-number='"+variable +
                     "'][@class='awesome-tabs current']")
    time.sleep(2)
    return


def review():
    click_element("//a[@title='Podgląd']")
    return

# gladiatus: functions returing values


def get_category_packages(variable):
    switcher = {
        '2': 'Bronie',
        '4': 'Tarcze',
        '8': 'Napierśniki',
        '1': 'Hełmy',
        '256': 'Rękawice',
        '512': 'Buty',
        '48': 'Pierścienie',
        '1024': 'Amulety',
        '4096': 'Bonusy',
        '8192': 'Błogosławieństwa',
        '16384': 'Najemnik',
        '32768': 'Składniki kuźnicze',
        '65536': 'Dodatki'
    }
    return switcher.get(variable, 'Wszystko')


def type_backpack(variable):
    switcher = {
        '1': '512',
        '2': '513',
        '3': '514',
        '4': '515',
        '5': '516',
        '6': '517'
    }
    return switcher.get(variable, '512')


def get_category_selling(variable):
    switcher = {
        1: "Bronie",
        2: "Tarcze",
        3: "Napierśniki",
        4: "Hełmy",
        5: "Rękawice",
        6: "Buty",
        7: "Pierścienie",
        8: "Amulety",
        #9: "Przyspieszacze",
        9: "Bonusy",
        10: "Błogosławieństwa",
        11: "Zwój"
    }
    return switcher.get(variable, "Wszystko")


def quality_pack(variable):
    switcher = {
        '0': 'Ceres (zielony)',
        '1': 'Neptun (niebieski)',
        '2': 'Mars (purpurowy)',
        '3': 'Jupiter (pomarańczowy)',
        '4': 'Olimp (czerwony)',
    }
    return switcher.get(variable, 'Normalny')


def get_gold_value():
    gold = driver.find_element_by_id('sstat_gold_val').text
    gold = gold.replace(".", "")
    return gold


def get_hp_value():
    hp = driver.find_element_by_id('header_values_hp_percent').text
    hp = hp[:-1]
    return hp


def get_packages_switchers(name, soulbound, level, quality, amount):
    by_name = False
    by_soulbound = False
    by_level = False
    by_quality = False
    by_amount = False

    if name != 'None':
        by_name = True
    if soulbound != 'None':
        by_soulbound = True
    if level != 'None':
        by_level = True
    if quality != 'None':
        by_quality = True
    if amount != 'None':
        by_amount = True
    return by_name, by_soulbound, by_level, by_quality, by_amount


def read_and_return_packages():
    lines = [line.rstrip('\n')
             for line in open('settings_packages'+str(server))]
    classes = []
    soulbounds = []
    prices = []
    categories = []
    qualities = []
    levels = []
    amounts = []
    solds = []
    for line in lines:
        split_line = line.split(" ")
        classes.append(re.findall("\'(.*?)\'", split_line[0])[0])
        soulbounds.append(re.findall("\'(.*?)\'", split_line[1])[0])
        prices.append(re.findall("\'(.*?)\'", split_line[2])[0])
        categories.append(re.findall("\'(.*?)\'", split_line[3])[0])
        qualities.append(re.findall("\'(.*?)\'", split_line[4])[0])
        levels.append(re.findall("\'(.*?)\'", split_line[5])[0])
        amounts.append(re.findall("\'(.*?)\'", split_line[6])[0])
        temp_sold = re.findall("\'(.*?)\'", split_line[7])[0]
        temp_sold = return_false_true(temp_sold)
        solds.append(temp_sold)

    # sorting from most expensive
    changed = True
    while changed:
        changed = False
        for i in range(0, len(lines)-1):
            if int(prices[i]) < int(prices[i+1]):
                changed = True

                temp = classes[i]
                classes[i] = classes[i+1]
                classes[i+1] = temp

                temp = soulbounds[i]
                soulbounds[i] = soulbounds[i+1]
                soulbounds[i+1] = temp

                temp = prices[i]
                prices[i] = prices[i+1]
                prices[i+1] = temp

                temp = categories[i]
                categories[i] = categories[i+1]
                categories[i+1] = temp

                temp = qualities[i]
                qualities[i] = qualities[i+1]
                qualities[i+1] = temp

                temp = levels[i]
                levels[i] = levels[i+1]
                levels[i+1] = temp

                temp = amounts[i]
                amounts[i] = amounts[i+1]
                amounts[i+1] = temp

                temp = solds[i]
                solds[i] = solds[i+1]
                solds[i+1] = temp

    return classes, soulbounds, prices, categories, qualities, levels, amounts, solds, lines


def read_colours_settings_selling():
    lines = [line.rstrip('\n')
             for line in open('settings_packages'+str(server))]
    purple = False
    orange = False
    red = False
    for line in lines:
        if 'purple' in line:
            purple = return_false_true(re.findall("\'(.*?)\'", line)[0])
        elif 'orange' in line:
            orange = return_false_true(re.findall("\'(.*?)\'", line)[0])
        elif 'red' in line:
            red = return_false_true(re.findall("\'(.*?)\'", line)[0])
    return purple, orange, red


def find_ready_objects_selling(elements, category, names):
    purple, orange, red = read_colours_settings_selling()
    filtr = []
    collection_ready = []
    for element in elements:
        data_quality = element.get_attribute("data-quality")
        filtr.append(str(element.get_attribute("data-hash")))
        if data_quality == "2" and purple or data_quality == "3" and orange or data_quality == "4" and red\
                or category == 11 or category == 12:
            if not names:
                collection_ready.append(filtr[-1])
            else:
                collection_ready.append(
                    (element.get_attribute("class").rstrip(' '))[0])
        elif data_quality != "2" and data_quality != "3" and data_quality != "4":
            if not names:
                collection_ready.append(filtr[-1])
            else:
                collection_ready.append(
                    (element.get_attribute("class").rstrip(' '))[0])

    return collection_ready

# gladiatus: basic functions


def check_events():
    paths = []
    paths.append("//input[@id='linkLoginBonus']")
    paths.append("//a[contains(@onclick,'MAX_simplepop')]")
    paths.append("//*[@id='linkcancelnotification']")
    paths.append("//*[@id='linknotification']")

    for path in paths:
        try:
            driver.find_element_by_xpath(path).click()
        except:
            continue

    return


def login():
    driver.get("https://pl.gladiatus.gameforge.com/game/")
    name = driver.find_element_by_xpath("//input[@id='login_username']")
    name.send_keys(username)
    passwd = driver.find_element_by_xpath("//input[@id='login_password']")
    passwd.send_keys(password)
    click_element("//option[@value='s"+str(server) +
                  "-pl.gladiatus.gameforge.com/game/index.php?mod=start&submod=login']")
    driver.find_element_by_id("loginsubmit").click()
    return


def heal_me():
    while int(get_hp_value()) < int(health):
        print("Eating food..")
        review()
        open_backpack(backpack_food)
        drag_and_drop("//div[@id='inv']//div[@data-content-type-accept='16777215']",
                      "//div[@id='avatar']//div[@class='ui-droppable']")
        time.sleep(2)
    return


def take_from_packages(path1, path2, sold):
    if not search_element(path1) and search_element(path2):
        return True
    elif search_element(path1):
        found = True
    elif not search_element(path1) and not search_element(path2):
        while search_element("//a[@class = 'paging_button paging_right_step']"):
            if search_element(path1) and check_if_item_is_sold(path1) == sold:
                found = True

    if found:
        move_move(path1, "//div[@id = 'inv']")
        if search_element("//div[@class = 'ui-droppable grid-droparea image-grayed active']"):
            release(
                "//div[@class = 'ui-droppable grid-droparea image-grayed active']")
            return True
        else:
            return False
    else:
        return False


def sell_on_market(path, price):
    drag_and_drop(path, "//div[@id='market_sell']/div[@class='ui-droppable']")
    click_element("//select[@id='dauer']//option[@value='3']")
    price_input = driver.find_element_by_xpath("//input[@name='preis']")
    price_input.clear()
    price_input.send_keys(price)
    click_element("//input[@value='Oferta']")

    if search_element("//div[@class='message fail']"):
        return False
    else:
        return True


def prepare_xpath(name, soulbound, level, quality, amount):
    path = "//div[@class='packageItem']//div"
    path2 = "//div[@id='inv']//div"

    if name != 'None':
        path = path + \
            "[contains(concat(' ', normalize-space(@class), ' '), ' " + name + " ')]"
        path2 = path2 + \
            "[contains(concat(' ', normalize-space(@class), ' '), ' " + name + " ')]"

    if soulbound != 'None':
        path += "[@data-soulbound-to='" + soulbound + "']"
        path2 += "[@data-soulbound-to='" + soulbound + "']"

    if level != 'None':
        path += "[@data-level='" + level + "']"
        path2 += "[@data-level='" + level + "']"

    if quality != 'None':
        path += "[@data-quality='" + quality + "']"
        path2 += "[@data-quality='" + quality + "']"

    if amount != 'None':
        path += "[@data-amount='" + amount + "']"
        path2 += "[@data-amount='" + amount + "']"

    return path, path2


def check_if_item_is_sold(element):
    action = ActionChains(driver)

    if isinstance(element, str):
        element = driver.find_element_by_xpath(element)

    action.move_to_element(element).perform()
    if search_element("//p[contains(text(),'Wskazówka')]"):
        return True
    else:
        return False


def get_maximum_gold_packages():
    classes, soulbounds, prices, categories, qualities, levels, amounts, solds, lines = read_and_return_packages()
    total_price = 0

    guild_market()
    if not search_element("//input[@value='Kup']"):
        return 0
    iterator = len(driver.find_elements_by_xpath(
        "//input[@value='Kup']")) + len(driver.find_elements_by_xpath("//input[@value='Anuluj']"))
    
    for i in range(0, len(lines)):
        price_temp = prices[i]
        name_temp = classes[i]
        soulbound_temp = soulbounds[i]
        level_temp = levels[i]
        quality_temp = qualities[i]
        amount_temp = amounts[i]
        by_name, by_soulbound, by_level, by_quality, by_amount = get_packages_switchers(name_temp, soulbound_temp, level_temp, quality_temp, amount_temp)
        for j in range(2,iterator):
            if search_element("//section[@id='market_table']//tr[position()='"+str(j)+"']/td[@align='center']/input[@value='Kup']"):
                element = driver.find_element_by_xpath("//section[@id='market_table']//tr[position()='"+str(j)+"']/td[@style]/div[@style]")
                price = (driver.find_element_by_xpath("//section[@id='market_table']//tr[position()='"+str(j)+"']/td[position()='3']").text).replace(".","")
                name = element.get_attribute("class")
                soulbound = element.get_attribute("data-soulbound-to")
                level = element.get_attribute("data-level")
                quality = element.get_attribute("data-quality")
                amount = element.get_attribute("data-amount")
                if price == price_temp:
                    if by_name and name_temp != name or by_soulbound and soulbound_temp != soulbound or\
                        by_level and level_temp != level or by_quality and quality_temp != quality or\
                            by_amount and amount_temp != amount:
                            continue

                    total_price += int(price)
        
    return total_price
                    
# gladiatus: main functions


def download_packages():
    guild_market()
    first_iterator = len(
        driver.find_elements_by_xpath("//input[@value='Kup']"))
    second_iterator = len(
        driver.find_elements_by_xpath("//input[@value='Anuluj']"))
    iterator = int(first_iterator) + int(second_iterator)

    file_path = 'settings_packages'+str(server)
    if os.path.exists(file_path):
        os.remove(file_path)

    package_file = open(file_path, 'a')
    action = ActionChains(driver)
    for i in range(2, int(iterator)):
        element = driver.find_element_by_xpath(
            "//section[@id='market_table']//tr[position()='" + str(i) + "']/td[@style]/div[@style]")
        soulbound = element.get_attribute('data-soulbound-to')
        price = driver.find_element_by_xpath(
            "//section[@id='market_table']//tr[position()='" + str(i) + "']/td[position()='3']").text
        price = price.replace(".", "")
        level = element.get_attribute('data-level')
        quality = element.get_attribute('data-quality')
        amount = element.get_attribute('data-amount')
        category = element.get_attribute('data-content-type')
        class_name = element.get_attribute('class')
        already_sold = 'False'
        temp = driver.find_element_by_xpath(
            "//section[@id='market_table']//tr[position()='" + str(i) + "']/td[@style]/div[@style]")
        action.move_to_element(temp).perform()
        if search_element("//p[contains(text(),'Wskazówka')]"):
            already_sold = 'True'

        ready_line = "class_name='" + str(class_name) + "' soulbound='" + str(soulbound) + "' price='" + str(price) + "' category='" + str(
            category) + "' quality='" + str(quality) + "' level='" + str(level) + "' amount='" + str(amount) + "' sold='" + str(already_sold) + "'\n"
        package_file.write(str(ready_line))


def expedition():
    if not expedition_enabled:
        return False

    points = driver.find_element_by_id('expeditionpoints_value_point').text
    if points == '0':
        print('Leaving expeditions.. Points: 0')
        print()
        return False

    heal_me()
    temp2 = driver.find_element_by_id('expeditionpoints_value_pointmax').text
    print("Waiting for expedition.. Points: " + str(points) + "/" + str(temp2))

    wait_for_element(
        "//div[@id='cooldown_bar_expedition']/div[@class='cooldown_bar_text']")
    click_element(
        "//div[@id='cooldown_bar_expedition']//a[@class='cooldown_bar_link']")

    temp1 = driver.find_element_by_xpath(
        "//a[@class='awesome-tabs current']").text
    temp2 = driver.find_element_by_xpath(
        "//div[@class='expedition_box']["+expedition_option+"]//div[@class='expedition_name']").text
    print("Attacking.. " + temp1 + " -> " + temp2)
    click_element("//button[contains(@onclick,'"+expedition_option+"')]")
    wait_for_element("//table[@style='border-spacing:0;']//td[2]")
    temp1 = driver.find_element_by_xpath(
        "//table[@style='border-spacing:0;']//td[2]").text
    print("Result of fight: " + temp1)
    print()

    if points == '1':
        return False
    else:
        return True

    return False


def dungeon():
    global exit_dungeons
    if not dungeon_enabled or exit_dungeons:
        return False

    if search_element("//div[@id='cooldown_bar_dungeon']/a[@class='cooldown_bar_link']"):
        element = driver.find_element_by_xpath(
            "//div[@id='cooldown_bar_dungeon']/a[@class='cooldown_bar_link']")
        if not element.is_displayed():
            exit_dungeons = True
            return False

    points = driver.find_element_by_id('dungeonpoints_value_point').text
    if points == '0':
        print("Leaving dungeons.. Points: 0")
        print()
        return False

    temp2 = driver.find_element_by_id('dungeonpoints_value_pointmax').text
    print("Waiting for dungeon.. Points: " + str(points) + "/" + str(temp2))

    wait_for_element(
        "//div[@id='cooldown_bar_dungeon']/div[@class='cooldown_bar_text']")
    click_element(
        "//div[@id='cooldown_bar_dungeon']/a[@class='cooldown_bar_link']")
    # check if new dungeon needed
    if search_element("//input[@value='normalne']") or search_element("//input[@value='zaawansowane']"):
        if dungeon_advenced:
            if search_element("//input[@value='zaawansowane'][@disabled='disabled']"):
                click_element("//input[@value='normalne']")
            else:
                click_element("//input[@value='zaawansowane']")
        else:
            click_element("//input[@value='normalne']")

    wait_for_element("//span[@class='dungeon_header_open']")
    temp1 = driver.find_element_by_xpath(
        "//span[@class='dungeon_header_open']").text
    print("Attacking.. " + temp1)

    onClick = driver.find_elements_by_xpath(
        "//*[contains(@onclick,'startFight')]")
    for button in onClick:
        try:
            click_element("//img[contains(@src,'combatloc.gif')]")
            break
        except:
            pass

        try:
            click_element(button)
            break
        except:
            pass

    wait_for_element("//table[@style='border-spacing:0;']//td[2]")
    temp1 = driver.find_element_by_xpath(
        "//table[@style='border-spacing:0;']//td[2]").text
    print("Result of fight: " + temp1)
    print()

    if points == '1':
        return False
    else:
        return True

    return False


def pack_gold():
    if int(get_gold_value()) < int(pack_gold_minimum) or not pack_gold_enabled:
        return

    print("Packing gold.. ")
    # load data
    classes, soulbounds, prices, categories, qualities, levels, amounts, solds, lines = read_and_return_packages()

    guild_market()
    if not search_element("//input[@value='Kup']"):
        return

    found_case = 0
    orginal_case = 0

    # find the best packing option
    gold_level = get_gold_value()
    for i in range(0, len(lines)):
        if (int(gold_level) - int(prices[i])) > 0:
            found_case = i
            orginal_case = i
            break

    first_iterator = len(
        driver.find_elements_by_xpath("//input[@value='Kup']"))
    second_iterator = len(
        driver.find_elements_by_xpath("//input[@value='Anuluj']"))
    iterator = first_iterator + second_iterator

    # search one of saved pack at guild market
    print("Searching pack at guild market..")
    bought = False
    while not bought:
        price_temp = prices[found_case]
        name_temp = classes[found_case]
        soulbound_temp = soulbounds[found_case]
        level_temp = levels[found_case]
        quality_temp = qualities[found_case]
        amount_temp = amounts[found_case]
        by_name, by_soulbound, by_level, by_quality, by_amount = get_packages_switchers(
            name_temp, soulbound_temp, level_temp, quality_temp, amount_temp)

        bought = False
        for i in range(2, int(iterator)+1):
            if search_element("//section[@id='market_table']//tr[position()='" + str(i) + "']/td[@align='center']/input[@value='Kup']"):
                element = driver.find_element_by_xpath(
                    "//section[@id='market_table']//tr[position()='" + str(i) + "']/td[@style]/div[@style]")
                soulbound = element.get_attribute('data-soulbound-to')
                class_item = element.get_attribute('class')
                price = driver.find_element_by_xpath(
                    "//section[@id='market_table']//tr[position()='" + str(i) + "']/td[position()='3']").text
                price = price.replace(".", "")
                level = element.get_attribute('data-level')
                quality = element.get_attribute('data-quality')
                amount = element.get_attribute('data-amount')

                if price_temp == price:

                    if by_name and name_temp != class_item or\
                            by_soulbound and soulbound_temp != soulbound or\
                            by_level and level_temp != level or\
                            by_quality and quality_temp != quality or\
                            by_amount and amount_temp != amount:
                        continue

                    gold_before = get_gold_value()
                    driver.find_element_by_xpath("//section[@id='market_table']//tr[position()='" + str(
                        i) + "']/td[@align='center']/input[@value='Kup']").click()
                    if (int(gold_before) - int(get_gold_value())) == int(price_temp):
                        bought = True
                        break

        if not bought and found_case != len(lines)-1:
            found_case += 1
        elif not bought and search_element("//a[contains(text(),'Następna strona')]") and found_case == len(lines)-1:
            found_case = orginal_case
        elif not bought and search_element("//a[contains(text(),'Następna strona')]") == False and found_case == len(lines)-1:
            print("Avalibe pack not found..")
            print()
            return

    # prepare xpaths
    print("Bought pack for " + str(price_temp) + "..")
    path, path2 = prepare_xpath(
        classes[found_case], soulbound_temp, level_temp, quality_temp, amount_temp)
    # gib it back niggur
    success_market = False
    while not success_market:
        packages()
        filter_packages(categories[found_case], qualities[found_case])
        open_backpack(backpack_free)

        if not take_from_packages(path, path2, solds[found_case]):
            return

        guild_market()
        open_backpack(backpack_free)

        if not sell_on_market(path2, price_temp):
            expedition()
        else:
            print("Sucessfully returned pack to guild market..")
            print()
            return

    return


def search_pack():
    if not pack_gold_enabled:
        return

    print("Searching for possible lost item..")
    classes, soulbounds, prices, categories, qualities, levels, amounts, solds, lines = read_and_return_packages()

    packages()
    path1 = ''
    path2 = ''
    found_packages = False
    found_backpack = False
    found_sold = ''
    found_price = ''
    items = []
    last_category = ''
    last_quality = ''
    for i in range(0, len(classes)):
        if last_category != categories[i] or last_quality != qualities[i]:
            filter_packages(categories[i], qualities[i])
            last_category = categories[i]
            last_quality = qualities[i]
            open_backpack(backpack_free)

        first_time = True
        both_locations = False
        while not both_locations:
            if not first_time:
                items = driver.find_elements_by_xpath(
                    "//div[@id='inv']//div[contains(@class,'ui-draggable')]")
                both_locations = True
            else:
                items = driver.find_elements_by_xpath(
                    "//div[@id='packages']//div[contains(@class,'ui-draggable')]")

            for item in items:
                name = item.get_attribute("class")
                level = item.get_attribute("data-level")
                soulbound = item.get_attribute("data-soulbound-to")
                quality = item.get_attribute("data-quality")
                amount = item.get_attribute("data-amount")

                by_name = False
                by_level = False
                by_soulbound = False
                by_quality = False
                by_amount = False
                by_sold = False

                if re.search(r"\s*\b"+classes[i]+r"\s*\b", name):
                    by_name = True
                if levels[i] == level or levels[i] == 'None':
                    by_level = True
                if soulbounds[i] == soulbound or soulbounds[i] == 'None':
                    by_soulbound = True
                if qualities[i] == quality or qualities[i] == 'None':
                    by_quality = True
                if amounts[i] == amount or amounts[i] == 'None':
                    by_amount = True
                if solds[i] == check_if_item_is_sold(item):
                    by_sold = True

                if by_name and by_level and by_soulbound and by_quality and by_amount and by_sold:
                    path1, path2 = prepare_xpath(
                        classes[i], soulbounds[i], levels[i], qualities[i], amounts[i])
                    found_sold = solds[i]
                    found_price = prices[i]
                    if both_locations:
                        found_backpack = True
                    else:
                        found_packages = True

                    break
            first_time = False

    if found_packages:
        print("Found lost item in packages..")
        take_from_packages(path1, path2, found_sold)
    elif found_backpack:
        print("Found lost item in inventory..")
    else:
        print("Didnt found any lost item..")
        print()
        return

    if found_packages or found_backpack:
        success_market = False
        while not success_market:
            guild_market()
            open_backpack(backpack_free)
            if not sell_on_market(path2, found_price):
                expedition()
            else:
                print("Successfuly returned to guild market lost item..")
                print()
                return
    return


def take_hades_costume():
    if search_element("//div[contains(@onmousemove,'Zbroja Disa Patera')]"):
        return

    review()
    click_element("//input[@value='zmień']")
    if search_element("//input[contains(@onclick,'Zbroja Disa Patera')]"):
        click_element("//input[contains(@onclick,'Zbroja Disa Patera')]")
        click_element(
            "//td[@id='buttonleftchangeCostume']/input[@value='Tak']")
        return True
    else:
        return False
    return False

def sell_items():

    if not sell_items_bool:
        return

    file_name = 'selling_items'+str(server)
    category = 0
    maximum_gold = get_maximum_gold_packages()

    collection_ready = []
    collection_ready_class = []
    lines = []
    if os.path.isfile(file_name):
        for line in lines:
            if search_element("//div[@id='inv']//div[@data-hash='" + line + "']"):
                collection_ready.append(line)
        os.remove(file_name)
    packages()
    open_backpack(backpack_free)
    while category < 11:
        if int(get_gold_value()) > int(maximum_gold):
            return
        #Check if anything is in category container
        category += 1
        filter_packages(get_category_selling(category), 0)
        if search_element("//a[@class='paging_button paging_right_full']"):
            click_element("//a[@class='paging_button paging_right_full']")

        for i in range(3):
            if search_element("//a[@class='paging_button paging_left_step']"):
                click_element("//a[@class='paging_button paging_left_step']")

        clicked_times=0
        for i in range(3):
            if search_element("//div[@id='packages']//div[contains(@class,'ui-draggable')]"):
                elements=driver.find_elements_by_xpath("//div[@id='packages']//div[contains(@class,'ui-draggable')]")
                collection_ready.extend(find_ready_objects_selling(elements, category, False))
                collection_ready_class.extend(find_ready_objects_selling(elements, category, True))

            if search_element("//a[@class='paging_button paging_right_step']"):
                click_element("//a[@class='paging_button paging_right_step']")
                clicked_times += 1
            else:
                break
                
        for i in range(0, clicked_times):
            click_element("//a[@class='paging_button paging_left_step']")

        if not collection_ready:
            continue

        #Check if can pick anything
        got_first = False
        open_backpack(backpack_free)
        collection_selling = []
        for i in range (0, len(collection_ready)):
            done = False
            time.sleep(0.05)
            while not done:
                temporary = "//div[@id='packages']//div[@data-hash='" + str(collection_ready[i]) + "']"
                if search_element(temporary):
                    move_move(temporary, "//input[@name='show-item-info']")
                else:
                    done = True
                    continue
                
                if not search_element("//body[@id='packagesPage']/div[contains(@class,'" + str(collection_ready_class[i]) + "')]"):
                    driver.refresh()
                    open_backpack(backpack_free)
                
                if search_element("//div[@class='ui-droppable grid-droparea image-grayed active']"):
                    release("//div[@class='ui-droppable grid-droparea image-grayed active']")
                    if(search_element("//div[@id='inv']//div[@data-hash='" + str(collection_ready[i]) + "']")):
                        collection_selling.append(collection_ready[i])
                        got_first = True
                        done = True
                        continue
                else:
                    break

        if not got_first:
            continue

        #Sell items
        with open(file_name, 'w+') as f:
            for string in collection_selling:
                string+="\n"
                f.write(string)
        
        shop = 0
        while collection_selling:
            shop += 1
            if shop == 1:
                click_element("//a[text() = 'Broń']")
                click_element("//div[@class='shopTab dynamic']")
            elif shop == 2:
                click_element("//a[text() = 'Pancerz']")
                click_element("//div[@class='shopTab dynamic']")
            elif shop == 3:
                click_element("//a[text() = 'Handlarz']")
                click_element("//div[@class='shopTab dynamic']")
            elif shop == 4:
                click_element("//a[text() = 'Alchemik']")
                click_element("//div[@class='shopTab dynamic']")
            elif shop == 5:
                click_element("//a[text() = 'Żołnierz']")
                click_element("//div[@class='shopTab'][text() = 'Ⅱ']")
            elif shop == 6:
                click_element("//a[text() = 'Żołnierz']")
                click_element("//div[@class='shopTab dynamic']")
            elif shop == 7:
                click_element("//a[text() = 'Malefica']")
            else:
                return

            open_backpack(backpack_free)
            found = True
            no_space = False
            while found:
                found = False
                time.sleep(0.05)
                while collection_selling:
                    temporary = "//div[@id='inv']//div[@data-hash='"+collection_selling[-1]+"']"
                    if search_element("//div[@id='shop']//div[@data-hash='"+collection_selling[-1]+"']") or\
                        not search_element(temporary):
                        del collection_selling[-1]
                        print("Element XPath:")
                        print(temporary)
                    move_move(temporary,"//input[@name='show-item-info']")
                    if search_element("//div[@id='shop']//div[@class='ui-droppable grid-droparea image-grayed active']"):
                        release("//div[@id='shop']//div[@class='ui-droppable grid-droparea image-grayed active']")
                        del collection_selling[-1]
                    else:
                        no_space = True
                        break

                if no_space:
                    break

                collection_selling.clear()
                for string in collection_ready:
                    if search_element("//div[@id='inv']//div[@data-hash='"+string+"']"):
                        collection_selling.append(string)
                        found = True
    return
# main
clear()

try:
    username, password, server, expedition_enabled, expedition_option,\
        pack_gold_enabled, pack_gold_minimum, dungeon_enabled,\
        dungeon_advenced, health, backpack_free,\
        backpack_food, headless, sell_items_bool = read_settings(sys.argv[1])
except:
    print("Send argument while running this file to set server!")
    print("Example -> python3 file.py 35")
    sys.exit()

chrome_options = Options()
#chrome_options.add_extension("./Gladiatus_addon.crx")
if headless:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--windows-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
driver.maximize_window()
login()
sell_items()
display_info()

exit_dungeons = False
exp = True
dung = True
while exp or dung:
    exp = expedition()
    dung = dungeon()
    pack_gold()
    search_pack()
    display_info()
    if not exp and not dung:
        take_hades_costume()
        exp = expedition()
        dung = dungeon()

print("Bot done work.. Closing webdriver..")
driver.close()
