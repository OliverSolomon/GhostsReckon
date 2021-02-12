"""This script populates fields with user data generated """

from main import db, Ghosts
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from time import sleep
from requests import get


#pyairmore
from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.device import DeviceService
from pyairmore.services.messaging import MessagingService
from re import findall as findnum


# def getText():



url = r"https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F%3Fpc%3Dtopnav-about-n-en&flowName=GlifWebSignIn&flowEntry=SignUp"

#initiated driver
driver = webdriver.Chrome(executable_path="/home/gamin3/Desktop/Ghosts-main/Ghosts-beta/chromedriver/chromedriverV88.0.4324.150")


#============================================ [X-PATHS] ===============
#page1
fname_xpath = '//*[@id="firstName"]'
lname_xpath = '//*[@id="lastName"]' 
email_xpath = '//*[@id="username"]'
pword_xpath = '//*[@id="passwd"]/div[1]/div/div[1]/input'
cPword_xpath = '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input'
nextBtn_xpath = '//*[@id="accountDetailsNext"]/div/button/div[2]'

#page2(phone verification)
inputPhoneNo_xpath = '//*[@id="phoneNumberId"]'
# inputPhoneNo_xpath = '/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div/div[2]/div[1]/div/div[1]/input'
otpInput_xpath = '//*[@id="code"]'
phoneNext_xpath  = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'

OTPverify_xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button/div[2]'

#page3 (Bio INformation)
birthDate_xpath = '//*[@id="day"]'
birthMonthDrop_xpath = '//*[@id="month"]'
birthYear_xpath = '//*[@id="year"]'
genderDrop_xpath = '//*[@id="gender"]'
nextPage_xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]'

# page4 (Additional verification info)
skip_xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/button/div[2]'

#page5 (accept terms)
yesImIn_xpath = '//*[@id="termsofserviceNext"]/div[2]'

#====================== [form filling functionality] ====================

#account
# accounts = [['mwangi', 'kipchoge', 'mwangikipchoge88', 'Mwangikipchoge88#'],['mwangi', 'kipchoge', 'mwangikipchoge89', 'Mwangikipchoge89#']]
accounts = Ghosts.query.all()




phoneNumber = ""

for i in accounts:
    #start session
    driver.get(url)

    #page1 functionality
    driver.find_element_by_xpath(fname_xpath).send_keys(i.fName)
    driver.find_element_by_xpath(lname_xpath).send_keys(i.sName)
    driver.find_element_by_xpath(email_xpath).send_keys(i.email)
    driver.find_element_by_xpath(pword_xpath).send_keys(i.password)
    driver.find_element_by_xpath(cPword_xpath).send_keys(i.password)
    driver.find_element_by_xpath(nextBtn_xpath).click()

    sleep(15)

    #page2 phone verification functionality
    driver.find_element_by_xpath(inputPhoneNo_xpath).send_keys(phoneNumber)
    driver.find_element_by_xpath(phoneNext_xpath).click()

    sleep(25)
    print("here")
        
    #getting text from phone using pyairmore
    ip = IPv4Address("192.168.0.27")  # whatever server's address is(press the three dots at top right corner of airmore apk to get this)
    session = AirmoreSession(ip)  # port is default to 2333
    txt_service = MessagingService(session)

    messages = txt_service.fetch_message_history()
    OTP_message = messages[0].content  # "latest Message"
    OTP_code = findnum(r'\d+', OTP_message)

    driver.find_element_by_xpath(otpInput_xpath).send_keys(OTP_code)
    driver.find_element_by_xpath(OTPverify_xpath).click()

    sleep(15)
    #page3 Bio info functionality
    driver.find_element_by_xpath(birthDate_xpath).send_keys(1)
    dropMonth = Select(driver.find_element_by_xpath(birthMonthDrop_xpath))
    dropMonth.select_by_value('2')
    driver.find_element_by_xpath(birthYear_xpath).send_keys(i.dob)

    dropGender = Select(driver.find_element_by_xpath(genderDrop_xpath))
    dropGender.select_by_value('3') #Rather not say for gender

    driver.find_element_by_xpath(nextPage_xpath).click()

    sleep(15)

    #page4 (additional Verification)
    driver.find_element_by_xpath(skip_xpath).click()

    sleep(20)
    #page5 (accept terms and conditions)
    driver.find_element_by_xpath(yesImIn_xpath).click()

    #end session
    driver.quit()
    print("201!  account " + i.email + " created.")

    sleep(2)