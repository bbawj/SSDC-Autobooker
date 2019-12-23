import os
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
msg = EmailMessage()
msg['Subject'] = 'Car lesson booked'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS




chromedriver = os.path.abspath("chromedriver.exe")
driver = webdriver.Chrome(chromedriver)
driver.implicitly_wait(10)
driver.maximize_window()
driver.get("https://www.ssdcl.com.sg/User/Login")


#login navigation to booking screen
while True:
    username = input("Enter your NRIC: ")
    password = input("Enter your password: ")
    user_elem = driver.find_element_by_id("UserName")
    pass_elem = driver.find_element_by_id("Password")
    user_elem.send_keys(username)
    pass_elem.send_keys(password)

    driver.find_element_by_xpath("//button[@type='submit']").click()
    try:
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='modal-footer']/button[1]")))
        element.click()
        print("Password or username incorrect")
        continue
    except TimeoutException:
        break
driver.find_element_by_xpath("//a[@href='/User/Booking/BookingList']").click()
driver.find_element_by_link_text('New Booking').click()
driver.find_element_by_id("chkProceed").click()
driver.find_element_by_link_text('Proceed').click()

#booking conditions
while True:
    type = input("Enter lesson type (PL/PT/SL/TT):")
    if type not in {'PL','PT','SL','TT'}:
        print("Please enter either PL/PT/SL/TT")
        continue
    else:
        break

while True:
    input_date = input("Enter date (eg. 01 Jan 2020): ")
    date_pref = input("Do you want to enable 7 day range (y/n): ")
    present = datetime.now()
    date_list_actual = []
    if date_pref =="y":
        try:
            test_date = datetime.strptime(input_date, '%d %b %Y')
            date_list = [test_date + timedelta(days = x) for x in range(7)]
            for d in date_list:
                if d.date() < present.date():
                    print("Invalid date please try again")
                    continue
                else:
                    base_date = d.strftime('%#d/%#m/%Y')
                    date_list_actual.append(base_date)
            break

        except ValueError:
            print("Wrong date format")
            continue


    elif date_pref=="n":
        try:
            test_date = datetime.strptime(input_date, '%d %b %Y')
            if test_date < present:
                print("Invalid date please try again")
                continue

        except ValueError:
            print("Wrong date format")
            continue

        else:
            id_date = test_date.strftime('%#d/%#m/%Y')

            break
    else:
        print("Invalid input please enter y/n")
        continue


while True:
    location = input("Enter location (Woodlands/Ang Mo Kio): ")
    if location not in {'Woodlands','Ang Mo Kio'}:
        print("Please enter either Woodlands/Ang Mo Kio")
        continue
    else:
        break

id_list = []


while True:

    try:
        x = [int(x) for x in input("Enter your session number (1-6 separated by whitespace): ").split()]
        for a in x:
            if a < 1 or a > 6:
                print("Enter valid numbers")
                continue
            elif date_pref=="n":
                id = str(a) + "_" + id_date
                id_list.append(id)
            elif date_pref=="y":
                for id_date in date_list_actual:
                    id = str(a) + "_" + id_date
                    id_list.append(id)
            else:
                pass
        break

    except ValueError:
        print("Enter valid numbers")
        continue



type_select = Select(driver.find_element_by_id('BookingType'))
type_select.select_by_value(type)
date_elem = driver.find_element_by_id("SelectedDate")
date_elem.send_keys(Keys.CONTROL + "a")
date_elem.send_keys(Keys.DELETE)
date_elem.send_keys(input_date)
loc_select = Select(driver.find_element_by_id('SelectedLocation'))
loc_select.select_by_value(location)

driver.find_element_by_id("btn_checkforava").click()


#refreshes the page while there are remaining slot IDs to be booked
while len(id_list) != 0:

    try:
        driver.execute_script("window.scrollTo(0, window.scrollY + 800)")
        booking_conditions = " or ".join(["contains(@id, '%s')" % keyword for keyword in id_list])
        expression = "//*[%s]" % booking_conditions
        #print(id_list)
        booking_slot = driver.find_element_by_xpath(expression)
        slot_id = booking_slot.get_attribute("id")
        for id in id_list:
            if id in slot_id:
                id_list.remove(id)
            else:
                pass
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, expression)))
        booking_slot.click()
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='modal-footer']/button[1]")))
        close_button.click()
        msg.set_content(f'A class of id {slot_id} has been booked, please login to confirm your booking within 40 mins')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        if len(id_list) != 0:
            driver.find_element_by_id("btn_checkforava").click()
            driver.execute_script("window.scrollTo(0, window.scrollY + 800)")
        continue

    except (NoSuchElementException, TimeoutException) as e:
        driver.execute_script("location.reload()")
        continue

print("All sessions booked")
