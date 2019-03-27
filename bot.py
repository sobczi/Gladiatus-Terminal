from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from configparser import SafeConfigParser
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
    if isinstance(path1, str):
        element1 = driver.find_element_by_xpath(path1)
    else:
        element1 = path1
    if isinstance(path2, str):
        element2 = driver.find_element_by_xpath(path2)
    else:
        element2 = path2

    action = ActionChains(driver)
    action.click_and_hold(element1)
    action.move_to_element(element2)
    action.perform()

def move_release(path1, path2):
    action = ActionChains(driver)
    action.click_and_hold(driver.find_element_by_xpath(path1))
    action.release(driver.find_element_by_xpath(path2))
    action.perform()

def mouse_move(path):
    action = ActionChains(driver)
    element = driver.find_element_by_xpath(path)
    action.move_to_element(element).perform()

def drag_and_drop(path1, path2):
    action = ActionChains(driver)
    wait_for_element(path1)
    element1 = driver.find_element_by_xpath(path1)
    wait_for_element(path2)
    element2 = driver.find_element_by_xpath(path2)
    action.drag_and_drop(element1, element2).perform()

def release(path1):
    while True:
        try:
            action = ActionChains(driver)
            element = driver.find_element_by_xpath(path1)
            action.move_to_element(element)
            action.release(element)
            action.perform()
            return
        except:
            pass

def click_element(variable):
    check_events()
    if isinstance(variable, str):
        variable = get_element(variable)
    variable.click()

def wait_for_element(path):
    while not search_element(path):
        time.sleep(0.05)

def get_digits(path):
    string = driver.find_element_by_xpath(path).text
    tmp = ""
    for s in string:
        if s.isdigit():
            tmp += s
        if s == "\n":
            break
    return tmp
# gladiatus: system functions

def display_info():
    def _get_stats(arena):
        if arena:
            variable = "Arena"
        else:
            variable = "Turma"
        all_fights = int(config.get("stats","lose_"+variable)) + int(config.get("stats","win_"+variable))
        win = int(config.get("stats","win_"+variable))
        return int(round((win/all_fights)*100))

    def _update_time():
        global start_time
        end_time = time.time()
        config.set("stats","time",
            str(int(config.get("stats","time"))+int(round(end_time - start_time))))
        config_save()
        start_time = time.time()

    _update_time()
    hp = get_hp_value()
    hp = hp + "%"
    progress = driver.find_element_by_id('header_values_xp_percent').text

    gold = driver.find_element_by_id('sstat_gold_val').text
    rubles = driver.find_element_by_id('sstat_ruby_val').text

    level = driver.find_element_by_id('header_values_level').text
    rank = driver.find_element_by_id('highscorePlace').text
    print("Player: " + config.get("login","login") + ", World: " + config.get("login","server") + ", HP: " + hp)
    print("Level: " + level + ", Progress: " + progress + ", Rank: " + rank)
    print("Gold: " + gold + ", Rubles: " + rubles)
    print()
    print("Some stats:")

    print("Tottaly farmed " + "{:,}".format(int(config.get("stats","gold_earned"))) + " gold.")
    if config_return_bool("farm","arena"):
        print("Winning percentage of Arena: " + str(_get_stats(True))+"%" +
            " (Wins: " + str(config.get("stats","win_Arena") + " | Loses: " +
             str(config.get("stats","lose_Arena")) + ")"))

    if config_return_bool("farm","turma"):
        print("Winning percentage of Turma: " + str(_get_stats(False))+"%" +
             " (Wins: " + str(config.get("stats","win_Turma") + " | Loses: " +
              str(config.get("stats","lose_Turma")) + ")"))

    print("Spent totally " + str(config.get("stats","expedition_points")) +
     " expedition points and " + str(config.get("stats","dungeon_points")) + " dungeon points.")

    if config_return_bool("pack_gold","pack_gold"):
        print("Packed totally: " + "{:,}".format(int(config.get("stats","packed"))) + " gold.")

    if config_return_bool("sell_items","sell_items"):
        print("Sold totally: " + "{:,}".format(int(config.get("stats","sold_items"))) +
         " items for " + "{:,}".format(int(config.get("stats","sold_gold"))) + " gold.")

    print("You totally saved on this server: " + str(time.strftime('%H:%M:%S', time.gmtime(int(config.get("stats","time"))))) + " time.")
    print()

def return_false_true(variable):
    if variable == 'True':
        return True
    else:
        return False

# gladiatus: navigation functions

def guild_market_navigation():
    while search_element("//a[contains(@href,'guildMarket')][@class='map_label']") == False:
        click_element("//a[text() = 'Gildia']")
        time.sleep(1)
    click_element("//a[contains(@href,'guildMarket')][@class='map_label']")
    while search_element("//div[@id='market_sell_box']//section[@style='display: none;']"):
        click_element("//h2[@class='section-header'][text() = 'sprzedaj']")

def packages_navigation():
    driver.find_element_by_id('menue_packages').click()
    if search_element("//section[@style='display: none;']"):
        click_element("//h2[@class='section-header'][contains(text(), 'Opcje')]")

def open_backpack(variable):
    click_element("//a[@data-bag-number='"+variable+"']")
    wait_for_element("//a[@data-bag-number='"+variable +"'][@class='awesome-tabs current']")
    time.sleep(2)

def review_navigation():
    click_element("//a[@title='Podgląd']")

def main_menu_navigation(path):
    element = driver.find_element_by_xpath(path)
    if not element.is_displayed():
        arena_navigation()
    driver.find_element_by_xpath(path).click()

def arena_navigation():
    while True:
        click_element("//div[@id='cooldown_bar_arena']/a")
        element = driver.find_element_by_xpath("//*[@id='mainnav']/li/table/tbody/tr/td[1]/a")
        if element.text == "Arena":
            click_element("//*[@id='mainnav']/li/table/tbody/tr/td[1]/a")
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

def login():
    driver.get("https://pl.gladiatus.gameforge.com/game/")
    name = driver.find_element_by_xpath("//input[@id='login_username']")
    name.send_keys(config.get("login","login"))
    passwd = driver.find_element_by_xpath("//input[@id='login_password']")
    passwd.send_keys(config.get("login","password"))
    click_element("//option[@value='s"+config.get("login","server")+"-pl.gladiatus.gameforge.com/game/index.php?mod=start&submod=login']")
    driver.find_element_by_id("loginsubmit").click()

def heal_me():
    while int(get_hp_value()) < int(config.get("heal","health_level")):
        print("Eating food..")
        review_navigation()
        open_backpack(config.get("backpacks","health_backpack"))
        drag_and_drop("//div[@id='inv']//div[@data-content-type-accept='16777215']",
                      "//div[@id='avatar']//div[@class='ui-droppable']")
        time.sleep(2)

# gladiatus: main functions

def take_hades_costume():
    if search_element("//div[contains(@onmousemove,'Zbroja Disa Patera')]"):
        return
    review_navigation()
    click_element("//input[@value='zmień']")
    if search_element("//input[contains(@onclick,'Zbroja Disa Patera')]"):
        click_element("//input[contains(@onclick,'Zbroja Disa Patera')]")
        click_element(
            "//td[@id='buttonleftchangeCostume']/input[@value='Tak']")
        return True
    else:
        return False

def config_return_bool(section, variable):
    if config.get(section, variable) == "True":
        return True
    else:
        return False

def config_save():
    with open(config_name,'w') as file:
        config.write(file)

def take_gold():
    if not config_return_bool("take_gold","take_gold"):
        return

    def calculate_difference(element):
        return int(best_element.get_attribute("data-price-gold")) + get_gold_value() - int(config.get("take_gold","gold_limit_value"))

    print("Taking out gold..")
    packages_navigation()
    Pack().filter_packages("Złoto",0)
    if search_element("//a[@class='paging_button paging_right_full']"):
        click_element("//a[@class='paging_button paging_right_full']")
    while True:
        if get_gold_value() > int(config.get("take_gold","gold_limit_value")) and config_return_bool("take_gold","gold_limit"):
            print()
            return
        if search_element("//div[@class='packageItem']//div[contains(@class,'ui-draggable')]"):
            elements = driver.find_elements_by_xpath("//div[@class='packageItem']//div[contains(@class,'ui-draggable')]")
            if int(elements[len(elements)].get_attribute("data-price-gold")) + get_gold_value() < int(config.get("take_gold","gold_limit_value")):
                move_move(elements[len(elements)],"//div[@id='inv']")
            else:
                best_element = elements[len(elements)]
                best_diff = calculate_difference(best_element)
                for element in elements:
                    if calculate_difference(element) < best_diff:
                        best_element = element
                        best_diff = calculate_difference(element)
                move_move(best_element,"//div[@id='inv']")
        else:
            print()
            return    

# gladiatus: main classes

def expedition():
    if not config_return_bool("farm","expedition"):
        return False

    points = driver.find_element_by_id('expeditionpoints_value_point').text
    if points == '0':
        print('Leaving expeditions.. Points: 0')
        print()
        return False

    heal_me()
    temp2 = driver.find_element_by_id('expeditionpoints_value_pointmax').text
    print("Waiting for expedition.. Points: " + str(points) + "/" + str(temp2))

    wait_for_element("//div[@id='cooldown_bar_expedition']/div[@class='cooldown_bar_text']")
    click_element("//div[@id='cooldown_bar_expedition']//a[@class='cooldown_bar_link']")

    temp1 = driver.find_element_by_xpath("//a[@class='awesome-tabs current']").text
    temp2 = driver.find_element_by_xpath("//div[@class='expedition_box']["+config.get("farm","expedition_option")+"]//div[@class='expedition_name']").text
    print("Attacking.. " + temp1 + " -> " + temp2)
    click_element("//button[contains(@onclick,'"+config.get("farm","expedition_option")+"')]")
    wait_for_element("//table[@style='border-spacing:0;']//td[2]")
    temp1 = driver.find_element_by_xpath("//table[@style='border-spacing:0;']//td[2]").text
    print("Result of fight: " + temp1)
    print()
    config.set("stats","expedition_points", str(int(config.get("stats","expedition_points"))+1))
    if "sobczi" in temp1:
        config.set("stats","gold_earned", str(int(config.get("stats","gold_earned"))+int(get_digits("//table/tbody/tr/td/p[1]"))))
    config_save()
    if points == '1':
        return False
    else:
        return True

def dungeon(exit_dungeons):
    if not config_return_bool("farm","dungeon") or exit_dungeons:
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

    wait_for_element("//div[@id='cooldown_bar_dungeon']/div[@class='cooldown_bar_text']")
    click_element("//div[@id='cooldown_bar_dungeon']/a[@class='cooldown_bar_link']")
    # check if new dungeon needed
    if search_element("//input[@value='normalne']") or search_element("//input[@value='zaawansowane']"):
        if config_return_bool("farm","dungeon_advenced"):
            if search_element("//input[@value='zaawansowane'][@disabled='disabled']"):
                click_element("//input[@value='normalne']")
            else:
                click_element("//input[@value='zaawansowane']")
        else:
            click_element("//input[@value='normalne']")

    wait_for_element("//span[@class='dungeon_header_open']")
    temp1 = driver.find_element_by_xpath("//span[@class='dungeon_header_open']").text
    print("Attacking.. " + temp1)

    onClick = driver.find_elements_by_xpath("//*[contains(@onclick,'startFight')]")
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
    temp1 = driver.find_element_by_xpath("//table[@style='border-spacing:0;']//td[2]").text
    print("Result of fight: " + temp1)
    print()
    config.set("stats","dungeon_points", str(int(config.get("stats","dungeon_points"))+1))
    if "sobczi" in temp1:
        config.set("stats","gold_earned", str(int(config.get("stats","gold_earned"))+int(get_digits("//table/tbody/tr/td/p[1]"))))
    config_save()
    if points == '1':
        return False
    else:
        return True

class Pack():
    def pack_gold(self):
        if int(get_gold_value()) < int(config.get("pack_gold","pack_level")) or not config_return_bool("pack_gold","pack_gold"):
            return

        print("Packing gold.. ")
        # load data
        while(int(get_gold_value()) > int(config.get("pack_gold","pack_level"))):
            classes, soulbounds, prices, categories, qualities, levels, amounts, solds, lines = self.pack_read_packages()

            guild_market_navigation()
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

            first_iterator = len(driver.find_elements_by_xpath("//input[@value='Kup']"))
            second_iterator = len(driver.find_elements_by_xpath("//input[@value='Anuluj']"))
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
                by_name, by_soulbound, by_level, by_quality, by_amount = self.pack_packages_switchers(
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
                    click_element("//a[contains(text(),'Następna strona')]")
                elif not bought and not search_element("//a[contains(text(),'Następna strona')]") and found_case == len(lines)-1:
                    print("Avalibe pack not found..")
                    print()
                    return

            # prepare xpaths
            print("Bought pack for " + "{:,}".format(int(price_temp)) + "..")
            path, path2 = self._pack_prepare_xpath(classes[found_case], soulbound_temp, level_temp, quality_temp, amount_temp)
            # gib it back niggur
            success_market = False
            while not success_market:
                packages_navigation()
                Pack().filter_packages(categories[found_case], qualities[found_case])
                open_backpack(config.get("backpacks","free_backpack"))

                if not self._pack_take_from_packages(path, path2, solds[found_case]):
                    return

                guild_market_navigation()
                open_backpack(config.get("backpacks","free_backpack"))

                if not self._pack_sell_on_market(path2, price_temp):
                    expedition()
                else:
                    print("Sucessfully returned pack to guild market..")
                    config.set("stats","packed",str(int(config.get("stats","packed")) + int(price_temp)))
                    config_save()
                    success_market = True
        print()

    def pack_search(self):
        if not config_return_bool("pack_gold","pack_gold"):
            return

        print("Searching for possible lost item..")
        classes, soulbounds, prices, categories, qualities, levels, amounts, solds, _ = self.pack_read_packages()

        packages_navigation()
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
                Pack().filter_packages(categories[i], qualities[i])
                last_category = categories[i]
                last_quality = qualities[i]
                open_backpack(config.get("backpacks","free_backpack"))

            first_time = True
            both_locations = False
            while not both_locations:
                if not first_time:
                    items = driver.find_elements_by_xpath("//div[@id='inv']//div[contains(@class,'ui-draggable')]")
                    both_locations = True
                else:
                    items = driver.find_elements_by_xpath("//div[@id='packages']//div[contains(@class,'ui-draggable')]")

                packages = True
                while packages:
                    packages = False
                    if first_time:
                        items = driver.find_elements_by_xpath("//div[@id='packages']//div[contains(@class,'ui-draggable')]")

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
                        if solds[i] == self._pack_check_sold(item):
                            by_sold = True

                        if by_name and by_level and by_soulbound and by_quality and by_amount and by_sold:
                            path1, path2 = self._pack_prepare_xpath(classes[i], soulbounds[i], levels[i], qualities[i], amounts[i])
                            found_sold = solds[i]
                            found_price = prices[i]
                            if both_locations:
                                found_backpack = True
                            else:
                                found_packages = True
                            break

                    if first_time and search_element("//a[@class = 'paging_button paging_right_step']"):
                        click_element("//a[@class = 'paging_button paging_right_step']")
                        packages = True
                        continue
                    first_time = False

        if found_packages:
            print("Found lost item in packages..")
            self._pack_take_from_packages(path1, path2, found_sold)
        elif found_backpack:
            print("Found lost item in inventory..")
        else:
            print("Didnt found any lost item..")
            print()
            return

        if found_packages or found_backpack:
            success_market = False
            while not success_market:
                guild_market_navigation()
                open_backpack(config.get("backpacks","free_backpack"))
                if not self._pack_sell_on_market(path2, found_price):
                    expedition()
                else:
                    print("Successfuly returned to guild market lost item..")
                    print()
                    return

    def pack_packages_switchers(self, name, soulbound, level, quality, amount):
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

    def pack_read_packages(self):
        lines = [line.rstrip('\n')for line in open('settings_packages'+config.get("login","server"))]
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

    def download_packages(self):
        guild_market_navigation()
        first_iterator = len(driver.find_elements_by_xpath("//input[@value='Kup']"))
        second_iterator = len(driver.find_elements_by_xpath("//input[@value='Anuluj']"))
        iterator = int(first_iterator) + int(second_iterator)

        if os.path.exists('settings_packages'+config.get("login","server")):
            os.remove('settings_packages'+config.get("login","server"))

        package_file = open('settings_packages'+config.get("login","server"), 'a')
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

    def filter_packages(self, category, colour):
        def is_number(variable):
            try:
                int(variable)
                return True
            except:
                return False
        if category == "None":
            category = "Wszystko"
        if colour == "None":
            colour = "Normalny"
        if is_number(category) and is_number(colour):
            click_element("//select[@name = 'f']//option[text() = '" + str(get_category_packages(category)) + "']")
            click_element("//select[@name = 'fq']//option[text() = '" + str(quality_pack(colour)) + "']")
        elif is_number(category) and not is_number(colour):
            click_element("//select[@name = 'f']//option[text() = '" + str(get_category_packages(category)) + "']")
            click_element("//select[@name = 'fq']//option[text() = '" + str(colour) + "']")
        elif not is_number(category) and is_number(colour):
            click_element("//select[@name = 'f']//option[text() = '" + str(category) + "']")
            click_element("//select[@name = 'fq']//option[text() = '" + str(quality_pack(colour)) + "']")
        elif not is_number(category) and not is_number(colour):
            click_element("//select[@name = 'f']//option[text() = '" + str(category) + "']")
            click_element("//select[@name = 'fq']//option[text() = '" + str(colour) + "']")
        click_element("//input[@value = 'Filtr']")

    def _pack_sell_on_market(self, path, price):
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

    def _pack_take_from_packages(self, path1, path2, sold):
        if not search_element(path1) and search_element(path2):
            return True
        elif search_element(path1):
            found = True
        elif not search_element(path1) and not search_element(path2):
            while search_element("//a[@class = 'paging_button paging_right_step']"):
                if search_element(path1) and self._pack_check_sold(path1) == sold:
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

    def _pack_check_sold(self, element):
        action = ActionChains(driver)
        if isinstance(element, str):
            element = driver.find_element_by_xpath(element)
        action.move_to_element(element).perform()
        if search_element("//p[contains(text(),'Wskazówka')]"):
            return True
        else:
            return False
    def _pack_prepare_xpath(self, name, soulbound, level, quality, amount):
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

class Sell_items():

    def sell_items(self):
        if not config_return_bool("sell_items","sell_items"):
            return

        category = 0
        maximum_gold = self._pack_get_maximum_gold()

        print("Selling items..")
        gold_counter = int(get_gold_value())
        item_counter = 0

        collection_ready = []
        collection_ready_class = []
        first_time_switch = True
        shop = 1
        all_items = True
        while category < 11:
            if int(get_gold_value()) > int(maximum_gold):
                print("Reached maximum gold for selling..")
                print()
                return
            #Check if anything is in category container
            if all_items:
                category += 1
            if first_time_switch and category > 6:
                shop = 1
                first_time_switch = False
            print("Working on category " + str(category) + "..")
            collection_ready = []
            collection_ready_class = []
            packages_navigation()
            Pack().filter_packages(self._sell_items_get_category(category), 0)
            if search_element("//a[@class='paging_button paging_right_full']"):
                click_element("//a[@class='paging_button paging_right_full']")

            for _ in range(3):
                if search_element("//a[@class='paging_button paging_left_step']"):
                    click_element("//a[@class='paging_button paging_left_step']")

            clicked_times=0
            for _ in range(3):
                if search_element("//div[@id='packages']//div[contains(@class,'ui-draggable')]"):
                    elements=driver.find_elements_by_xpath("//div[@id='packages']//div[contains(@class,'ui-draggable')]")
                    collection_ready.extend(self._sell_items_find_ready_objects(elements, category, False))
                    collection_ready_class.extend(self._sell_items_find_ready_objects(elements, category, True))

                if search_element("//a[@class='paging_button paging_right_step']"):
                    click_element("//a[@class='paging_button paging_right_step']")
                    clicked_times += 1
                else:
                    break
                    
            for _ in range(0, clicked_times):
                click_element("//a[@class='paging_button paging_left_step']")

            if not collection_ready:
                continue

            #Check if can pick anything
            got_first = False
            open_backpack(config.get("backpacks","free_backpack"))
            collection_selling = []
            while collection_ready:
                temporary = "//div[@id='packages']//div[@data-hash='" + str(collection_ready[0]) + "']"
                wait_for_element(temporary)
                move_move(temporary, "//input[@name='show-item-info']")
                
                if not search_element("//body[@id='packagesPage']/div[contains(@class,'" + str(collection_ready_class[0]) + "')]"):
                    driver.refresh()
                    open_backpack(config.get("backpacks","free_backpack"))
                    continue
                
                if search_element("//div[contains(@class,'active')]"):
                    release("//div[contains(@class,'active')]")
                    if(search_element("//div[@id='inv']//div[@data-hash='" + str(collection_ready[0]) + "']")):
                        collection_selling.append(collection_ready[0])
                        got_first = True
                        del collection_ready[0]
                        continue
                else:
                    all_items = False
                    break

            if not collection_ready:
                all_items = True

            if not got_first:
                continue

            item_counter += len(collection_selling)
            #Sell items
            no_space = False
            while collection_selling:
                if no_space:
                    shop += 1
                    no_space = False
                if shop == 1:
                    self._sell_items_npc("Broń",2)
                elif shop == 2:
                    self._sell_items_npc("Pancerz",2)
                elif shop == 3:
                    self._sell_items_npc("Handlarz",0)
                elif shop == 4:
                    self._sell_items_npc("Handlarz",1)
                elif shop == 5:
                    self._sell_items_npc("Handlarz",2)
                elif shop == 6:
                    self._sell_items_npc("Alchemik",0)
                elif shop == 7:
                    self._sell_items_npc("Alchemik",1)
                elif shop == 8:
                    self._sell_items_npc("Alchemik",2)
                elif shop == 9:
                    self._sell_items_npc("Żołnierz",0)
                elif shop == 10:
                    self._sell_items_npc("Żołnierz",1)
                elif shop == 11:
                    self._sell_items_npc("Żołnierz",2)
                elif shop == 12:
                    self._sell_items_npc("Malefica",0)
                elif shop == 13:
                    self._sell_items_npc("Malefica",1)
                elif shop == 14:
                    self._sell_items_npc("Malefica",2)
                else:
                    print("Spending one ruble for new shops..")
                    if int(driver.find_element_by_xpath("//div[@id='sstat_ruby_val']").text) > 0:
                        arena_navigation()
                        main_menu_navigation("//a[contains(text(),'Broń')]")
                        click_element("//input[@value='Nowe towary']")
                        shop = 1
                        continue
                    else:
                        return

                open_backpack(config.get("backpacks","free_backpack"))
                found = True
                while found:
                    found = False
                    time.sleep(0.05)
                    while collection_selling:
                        temporary = "//div[@id='inv']//div[@data-hash='"+collection_selling[-1]+"']"
                        if search_element("//div[@id='shop']//div[@data-hash='"+collection_selling[-1]+"']") or\
                            not search_element(temporary):
                            del collection_selling[-1]
                            continue
                        move_move(temporary,"//input[@name='show-item-info']")
                        if search_element("//div[@id='shop']//div[contains(@class,'active')]"):
                            release("//div[@id='shop']//div[contains(@class,'active')]")
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
        gold_counter = int(get_gold_value()) - gold_counter
        print("Successfully ended sellings items..")
        print("Totally sold " + "{:,}".format(int(item_counter)) + " items for total " + "{:,}".format(int(gold_counter)) + " gold!")
        print()
        config.set("stats","sold_items",str(item_counter))
        config.set("stats","sold_gold",str(gold_counter))
        config_save()
        
    def _sell_items_find_ready_objects(self, elements, category, names):
            purple = config_return_bool("sell_items","purple")
            orange = config_return_bool("sell_items","orange")
            red = config_return_bool("sell_items","red")
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

    def _sell_items_npc(self, npc_name, page):
        main_menu_navigation("//div[contains(@id,'submenu')]//a[text() = '"+str(npc_name)+"']")
        if page == 1:
            click_element("//div[@class='shopTab'][text() = 'Ⅱ']")
        elif page == 2:
            click_element("//div[@class='shopTab dynamic']")

    def _sell_items_get_category(self, variable):
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

    def _pack_get_maximum_gold(self):
        classes, soulbounds, prices, _, qualities, levels, amounts, _, lines = Pack().pack_read_packages()
        total_price = 0
        guild_market_navigation()
        if not search_element("//input[@value='Kup']") and not search_element("//a[contains(text(),'Następna strona')]"):
            return 0
        while True:
            iterator = len(driver.find_elements_by_xpath("//input[@value='Kup']")) + len(driver.find_elements_by_xpath("//input[@value='Anuluj']"))
            for i in range(0, len(lines)):
                price_temp = prices[i]
                name_temp = classes[i]
                soulbound_temp = soulbounds[i]
                level_temp = levels[i]
                quality_temp = qualities[i]
                amount_temp = amounts[i]
                by_name, by_soulbound, by_level, by_quality, by_amount = Pack().pack_packages_switchers(name_temp, soulbound_temp, level_temp, quality_temp, amount_temp)
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
            if search_element("//a[contains(text(),'Następna strona')]"):
                click_element("//a[contains(text(),'Następna strona')]")
            else:
                break
        return total_price

class Auction_house():
    def auction_house(self):
        if not config_return_bool("auction_house","rings")and not config_return_bool("auction_house","amulets")\
             and not config_return_bool("auction_house", "boosters"):
            return 

        print("Buying items from auction house..")
        if config_return_bool("auction_house", "food"):
            print("Checking food..")
            packages_navigation()
            Pack().filter_packages("Jadalne","Normalny")
            food_pages = int(config.get("auction_house","food_pages"))
            need_food = True
            for i in range(food_pages, food_pages*10):
                if search_element("//div[@class='paging_numbers']//a[text() = '" + str(i) + "']"):
                    print("Got enough food..")
                    need_food = False
                    break
                if need_food:
                    print("Buying food..")
                    self._auction_house_items("Jadalne")

        if config_return_bool("auction_house","boosters"):
            print("Buying boosters..")
            self._auction_house_boosters()

        if config_return_bool("auction_house","rings"):
            print("Buying rings..")
            self._auction_house_items("Pierścienie")

        if config_return_bool("auction_house","amulets"):
            print("Buying amulets..")
            self._auction_house_items("Amulety")

        print("Successfully hided whole gold..")
        print()

    def _auction_house_items(self,filter):
        main_menu_navigation("//a[contains(text(),'Dom aukcyjny')]")
        self._auction_house_filter(filter)
        auction_forms = self._auction_house_get_forms()
        for i in range(len(auction_forms)):
            helper = "//div[@id='auction_table']//form[@id='" + auction_forms[i] + "']"
            price = self._auction_house_get_numbers(str(driver.find_element_by_xpath(helper + "//input[@name='bid_amount']").get_attribute("value")))
            mouse_move(helper + "//div[@data-price-gold]")
            value = self._auction_house_get_numbers(driver.find_element_by_xpath("//p[@style='color:#DDDDDD']").text)

            if int(price) - int(value) > int(config.get("auction_house","highest_difference"))\
                 or not "Brak ofert" in driver.find_element_by_xpath(helper + "//div[@class='auction_bid_div']/div").text:
                continue

            click_element(helper + "//input[@value='Licytuj']")
            if search_element("//div[@class='message fail']"):
                return False
        return True

    def _auction_house_get_numbers(self,string):
        result = ""
        for char in string:
            if char.isdigit():
                result += str(char)
        return result

    def _auction_house_get_forms(self):
        elements = driver.find_elements_by_xpath("//div[@id='auction_table']//form[@method='post']")
        auction_forms = [""] * len(elements)
        for i in range(len(elements)):
            auction_forms[i] = str(elements[i].get_attribute("id"))
        return auction_forms

    def _auction_house_filter(self,category):
        click_element("//select[@name='itemType']//option[text() = '"+str(category)+"']")
        click_element("//input[@value='Filtr']")

    def _auction_house_boosters(self):
        classes = []
        classes.append("item-i-11-4 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-3 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-2 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-1 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-8 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-7 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-6 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-5 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-12 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-11 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-10 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-9 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-16 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-15 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-14 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-13 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-20 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-19 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-18 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-17 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-27 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-26 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-25 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-24 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-23 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-22 ui-draggable ui-droppable ui-draggable-handle")
        classes.append("item-i-11-21 ui-draggable ui-droppable ui-draggable-handle")
        values = [0] * 27

        packages_navigation()
        Pack().filter_packages("Przyspieszacze","Normalny")
        while True:
            for i in range(len(classes)):
                values[i] += len(driver.find_elements_by_xpath("//div[@class='" + classes[i] + "']"))
            if search_element("//a[@class='paging_button paging_right_step']"):
                click_element("//a[@class='paging_button paging_right_step']")
            else:
                break

        need_boosters = False
        for i in range(len(values)):
            changed = False
            if values[i] >= int(config.get("auction_house","boosters_per_type")):
                values[i] = 0
            else:
                changed = True
            if changed:
                values[i] -= int(config.get("auction_house","boosters_per_type"))
                values[i] *= -1
                need_boosters = True

        if not need_boosters:
            return
        del need_boosters

        changed = True
        while changed:
            changed = False
            for i in range(len(values)-1):
                if values[i] < values[i+1]:
                    temporary_str = classes[i+1]
                    temporary_int = values[i+1]
                    values[i+1] = values[i]
                    classes[i+1] = classes[i]
                    values[i] = temporary_int
                    classes[i] = temporary_str
                    changed = True
        del temporary_str
        del temporary_int
        del changed

        positive_values = -1
        for i in range(len(values)):
            if values[i] > 0:
                positive_values += 1
            else:
                break

        main_menu_navigation("//a[contains(text(),'Dom aukcyjny')]")
        self._auction_house_filter("Przyspieszacze")
        auction_forms = self._auction_house_get_forms()
        for k in range(len(classes)):
            for i in range(len(auction_forms)):
                if k > positive_values:
                    return
                if not values[k]:
                    break
                helper = "//div[@id='auction_table']//form[@id='" + auction_forms[i] + "']"
                no_offers = False
                if "Brak ofert" in driver.find_element_by_xpath(helper + "//div[@class='auction_bid_div']/div").text:
                    no_offers = True
                if search_element(helper + "//div[contains(@class,'" + classes[k] + "')]") and no_offers:
                    click_element(helper + "//input[@value='Licytuj']")
                    values[k] -= 1
                if search_element("//div[@class='message fail']"):
                    return
        return

class Extract():
    def extract(self):
        if not config_return_bool("extract","extract"):
            return

        print("Extracting items..")
        self._extract_get()
        print("Melting items..")
        main_menu_navigation("//a[contains(text(),'Roztapiarka')]")
        open_backpack(config.get("backpacks","extract_backpack"))
        inv_draggable = "//div[@id='inv']//div[contains(@class,'ui-draggable')]"
        if not search_element(inv_draggable):
            print("Didnt found any items..")
            return
        for i in range(2):
            first_path = "//div[contains(@class,'forge_closed " + str(i) + "')]"
            second_path = "//div[contains(@class,'forge_finished-succeeded " + str(i) + "')]"
            if search_element(first_path):
                click_element(first_path)
            elif search_element(second_path):
                click_element(second_path)
                click_element("//div[contains(text(),'Wyślij jako pakiet')]")
            else:
                continue
            move_release(inv_draggable,"//fieldset[@id='crafting_input']//div[@class='ui-droppable']")
            click_element("//div[@class='icon_gold']")
            print("Successfully used " + str(i) + ". melting box..")
        print("Storing components..")
        self._extract_store()
        print()
        
    def _extract_get_move(self,element):
            move_move(element,"//input[@name='show-item-info']")
            if search_element("//div[contains(@class,'active')]"):
                release("//div[contains(@class,'active')]")
                return True
            else:
                return False
    
    def _extract_store(self):
            main_menu_navigation("//a[contains(text(),'Magazyn surowców')]")
            if search_element("//button[@id='store'][@disabled='']"):
                click_element("//input[@id='from-packages']")
            click_element("//button[contains(text(),'Jazda!')]")

    def _extract_get(self):
            print("Getting items for extract..")
            colours = ["Mars (purpurowy)", "Jupiter (pomarańczowy)", "Olimp (czerwony)"]
            colours_bools = [config_return_bool("extract","purple"), config_return_bool("extract","orange"), config_return_bool("extract","red")]
            invalid_types = ["64","4096","8192","32768"]

            packages_navigation()
            for i in range(3):
                if colours_bools[i]:
                    Pack().filter_packages(0,colours[i])
                    break

            if search_element("//a[@class='paging_button paging_right_full']"):
                click_element("//a[@class='paging_button paging_right_full']")

            while True:
                open_backpack(config.get("backpacks","extract_backpack"))
                all_items = driver.find_elements_by_xpath("//div[@id='packages']//div[contains(@class,'ui-draggable')]")
                good_items = []
                for i in range(len(all_items)-1,-1):
                    good = True
                    for j in range(len(invalid_types)):
                        if all_items[i].get_attribute("data-content-type") == invalid_types[j]:
                            good = False
                            break
                    if good:
                        good_items.append(all_items[i])

                if not good_items:
                    return

                for i in range(len(good_items)-1,-1):
                    if good_items[i].get_attribute("data-quality") == "4" and config.get("extract","red") or\
                        good_items[i].get_attribute("data-quality") == "3" and config.get("extract","orange") or\
                            good_items[i].get_attribute("data-quality") == "3" and config.get("extract","orange"):
                        if not _extract_get_move(good_items[i]):
                            return

                if search_element("//a[@class='paging_button paging_left_step']"):
                    click_element("//a[@class='paging_button paging_left_step']")
                else:
                    break

class Farm():
    def Arena(self, arena):
        if arena:
            if not config_return_bool("farm","arena"):
                return
            variable1 = "Arena"
            variable2 = "areny"
            variable3 = "Arena"
            variable4 = "arena"
        else:
            if not config_return_bool("farm","turma"):
                return
            variable1 = "Turma"
            variable2 = "Circus Turma"
            variable3 = "Circus"
            variable4 = "ct"

        heal_me()
        print("Waiting for "+variable1+"..")
        wait_for_element("//div[@id='cooldown_bar_text_"+variable4+"'][text() = 'Do "+variable2+"']")
        arena_navigation()
        click_element("//a[contains(@class,'awesome-tabs')][text() = '"+variable3+" Provinciarum']")

        best_choice, best_choice_level = self._find_best_choice_arena()
        print("Found weakest level: " + str(best_choice_level) + "..")
        print("Attacking " + driver.find_element_by_xpath("//section[contains(@id,'own')]//tbody/tr["+str(best_choice)+"]/td[1]").text + "..")
        click_element("//section[contains(@id,'own')]//tbody/tr["+str(best_choice)+"]//div[@class='attack']")

        wait_for_element("//table[@style='border-spacing:0;']//td[2]")
        temp1 = driver.find_element_by_xpath("//table[@style='border-spacing:0;']//td[2]").text
        print("Result of fight: " + temp1)
        print()
        if "sobczi" in temp1:
            config.set("stats","win_"+variable1+"", str(int(config.get("stats","win_"+variable1))+1))
        else:
            config.set("stats","lose_"+variable1+"", str(int(config.get("stats","lose_"+variable1))+1))
        if "sobczi" in temp1:
            config.set("stats","gold_earned", str(int(config.get("stats","gold_earned"))+int(get_digits("//table/tbody/tr/td/p[1]"))))
        config_save()
                

    def _find_best_choice_arena(self):
        best_choice = 0
        best_choice_level = 0
        first_time = True
        for i in range(2,6):
            level = int(driver.find_element_by_xpath("//section[contains(@id,'own')]//tbody/tr["+str(i)+"]/td[2]").text)
            if first_time:
                best_choice = i
                best_choice_level = level
                first_time = False
            elif level < best_choice_level:
                best_choice = i
                best_choice_level = level
        return best_choice, best_choice_level

# main-settings
clear()
start_time = time.time()
debug = True
try:
    if sys.argv[1]:
        config_name = "config"+str(sys.argv[1])+".ini" 
except:
    if not debug:
        print("Send argument while running this file to set server!")
        print("Example -> python3 file.py 35")
        sys.exit()
    else:
        config_name = "config35.ini"
    
config = SafeConfigParser()
config.read(config_name)

chrome_options = Options()
if config_return_bool("top","headless"):
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--windows-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
driver.maximize_window()

print("Logging in as " + config.get("login","login") + " at server " + config.get("login","server") + "..")
print()

# main-botting
login()
display_info()

exit_dungeons = False
exp = True
dung = True
iterator = 0
Pack().pack_gold()
while exp or dung:
    iterator += 1
    exp = expedition()
    dung = dungeon(exit_dungeons)
    Farm().Arena(True)
    Farm().Arena(False)
    display_info()
    if not exp and not dung:
        take_hades_costume()
        exp = expedition()
        dung = dungeon(exit_dungeons)
    Pack().pack_gold()
Sell_items().sell_items()
Pack().pack_gold()
Pack().pack_search()
Extract().extract()
Auction_house().auction_house()
display_info()
print("Bot done work.. Closing webdriver..")
driver.close()