import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import requests

#thelinks = []
title = []
movielength = []
moviethumbnail =[]
url = []

dataDictionary = {"title":"video-title","movielength":"style-scope ytd-thumbnail-overlay-time-status-renderer","moviethumbnail":"style-scope ytd-thumbnail no-transition"}

#searchTerm = raw_input("What do you want to search?\n")
searchTerm = "Detective Conan"
#ask the user for the search term
try:
    #numberVidsRequested = int(raw_input("How many vids do you want? \n"))
    numberVidsRequested = 50
except ValueError:
    print("This is not a whole number")

#timeFlag = int(raw_input("What time frame?\n 1- last hour \n 2- today \n 3- this week \n 4- this month \n 5- this year \n"))
timeFlag = 3
time_array = ["sp=EgIIAQ%253D%253D", "sp=EgIIAg%253D%253D", "sp=EgQIAxABQgQIABIA", "sp=EgQIBBABQgQIARIA", "sp=EgIIBQ%253D%253D"]
timeFlagIndex = timeFlag - 1
chosen_time = time_array[timeFlagIndex]

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/results?search_query="+searchTerm+"&"+chosen_time)

count=0


numAutoScroll = int(numberVidsRequested / 20)

def _specificData(dataType, allData):
    someCounter = 0
#    rawClassData = driver.find_elements(By.XPATH,'//*[@class="'+dataDictionary[dataType]+'"]')
#    rawIdData = driver.find_elements(By.XPATH,'//*[@id="'+dataDictionary[dataType]+'"]').text
    while len(title) < numberVidsRequested:
        if dataType == 'title':
            print "here"
            rawData = allData[someCounter].find_element(By.XPATH,'//*[@id="'+dataDictionary[dataType]+'"]').text
            print rawData
        elif dataType == 'movielength':
            print "there"
            try:
                rawData = allData[someCounter].text
            except:
                print "e"
        else:
            print "meh"
            try:
                rawData = allData[someCounter].text
            except:
                print "i"
            # try:
            #     print theTitle
            # except:
            #     print "issue with {}".format(titles)
        exec dataType + ".append(rawData)"
    someCounter +=1
    print someCounter

def _autoScroll():
    element = driver.find_element_by_tag_name('body')
    element.send_keys(Keys.CONTROL, Keys.END)
    time.sleep(3)

# [(k, v)] = dataDictionary.items()

def _getData():
    rawTitle = driver.find_elements(By.XPATH,'//*[@id="video-title"]')
    for the_title in rawTitle:
        try:
            text = the_title.text
            title.append(text.encode('unicode_escape'))
        except:
            print "here"
    rawMovieLength = driver.find_elements(By.XPATH,'//*[@class="style-scope ytd-thumbnail-overlay-time-status-renderer"]')
    for movieLength in rawMovieLength:
        try:
            text = movieLength.text
            movielength.append(text.encode('unicode_escape'))
        except:
            print "there"

    # rawThumbnailLink = driver.find_elements(By.XPATH,'//*[@class="style-scope ytd-thumbnail no-transition"]')
    # for thumbnail in rawThumbnailLink:
    #     try:
    #         thumbnailURL = thumbnail.get_attribute("src").text
    #         moviethumbnail.append(thumbnailURL.encode('unicode_escape'))
    #     except:
    #         print "meh"

    rawLink = driver.find_elements(By.XPATH,'//*[@id="video-title"]')
    for the_title in rawLink:
        try:
            link = the_title.get_attribute("href")
            url.append(link.encode('unicode_escape'))
        except:
            print "marh"

if numberVidsRequested > 20:
    print numAutoScroll
    for _ in range(numAutoScroll):
        _autoScroll()

_getData()

#zip the data up


#write the new csv file
targetFile = open("./"+searchTerm+".csv", "wb")
writer = csv.writer(targetFile)
writer.writerow(["Video Name","Length","Link"])

theData=(zip(title,movielength,url))

#write the data into the csv file
for row in theData:
    writer.writerow(row)
    #print row
targetFile.close()
driver.quit()
