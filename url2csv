import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

thelinks = []
driver = webdriver.Firefox()

counter=1


def getLink():
    continue_link = driver.find_element_by_tag_name('a')
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        theLink = elem.get_attribute("href")
        if "image/" in theLink:
            print theLink
            if theLink not in thelinks:
                first = theLink.replace("image","images")
                thePic = first +".jpg"
                thelinks.append(thePic)
    global counter
    counter+=1

while (counter < 10):
    driver.get("="+str(counter))
    getLink()
            
print thelinks

with open('pics.csv', "wb") as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        for line in thelinks:
            writer.writerow([line])
            
driver.quit()
