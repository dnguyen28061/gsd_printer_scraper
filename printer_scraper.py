
from bs4 import BeautifulSoup
import requests
import urllib3
from selenium import webdriver
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time 
from selenium import webdriver

names_806_printers = [
    "Help Desk",
    "2S Laser",
    "2N Laser",
    "2C Laser",
    "3S Laser",
    "3C Laser",
    "3N Laser",
    "4S Laser",
    "4C Laser",
    "4N Laser",
    "Sackler 2nd Floor"
] 
addresses_806_printers = [
    "http://10.103.170.246",
    "http://10.103.170.250/",
    "http://10.103.170.249/",
    "http://10.103.170.84/",
    "http://10.103.170.252/",
    "http://10.103.170.203/",
    "http://10.103.170.251/",
    "http://10.103.170.254/",
    "http://10.103.170.226",
    "http://10.103.170.253/",
    "https://10.245.225.15/"
]
names_xerox_printers = [
    "2C Color", "3C Color", "4C Color", "Help Desk Color", "40K Color", "42K Color"
    ]
addresses_xerox_printers = [
    "http://10.103.170.82/", "http://10.103.170.81/", "http://10.103.170.212/", 
    "http://10.103.170.210/", "http://10.103.170.211/", "http://10.103.170.80/"
]

def make_soup(url):
    r = requests.get(url, verify = False)
    return BeautifulSoup(r.text,'html.parser')

def get_info_HP_m806(address): 
    soup = make_soup(address)
    ids = ["SupplyPLR0", "SupplyPLR1", "TrayBinStatus_2", "TrayBinStatus_3", "TrayBinStatus_4",
    "TrayBinStatus_5"]
    info = ["Black", "Maint", "T2", "T3", "T4", "T5"]
    for idx, tag in enumerate(ids): 
        percentage = soup.find(id = tag).contents[0]
        print(info[idx] + ": " + percentage)
    
def get_info_xerox(address): 
    xerox_elts = ["Black", "Cyan", "Magenta", "Yellow", "Black Image", 
                  "Cyan Image", "Magenta Image", "Yellow Image", 
                   "Fuser", "Belt Cleaner", "Transfer Roller", "Suction Roller"]
    # get the page source of a xerox page 
    def html_xerox(address): 
        browser = webdriver.Chrome() 
        browser.get(address)
        browser.switch_to.frame("theTree")
        browser.find_element_by_xpath("//*[@id='n5']/a").click()
        time.sleep(3)
        browser.switch_to.default_content()
        browser.switch_to.frame("theContent")
        source = browser.page_source
        browser.quit()
        return source
    html = html_xerox(address)
    soup = BeautifulSoup(html, "html.parser")
    elts = soup.find_all(class_ = "horizTherm")
    
    for i in range(len(xerox_elts)): 
        percentage = int((elts[i].contents[1]['title']).split("%")[0])
        # if percentage < 2: 
        print(xerox_elts[i] + ": " + str(percentage) + "%")

if __name__ == '__main__':
    for idx, address in enumerate(addresses_806_printers): 
        print(names_806_printers[idx])
        get_info_HP_m806(address)
        print("\n")
    for i, address in enumerate(addresses_xerox_printers): 
        print(names_xerox_printers[i])
        get_info_xerox(address)
        print("\n")

