#bring in modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from collections import defaultdict
import requests,os,csv


print "Welcome to the Twitter Scraper."
#ask the user for the search term
searchTerm = str(raw_input("What is the search term you would like to scrape? \n"))


#ask the user for the search term
try:
    numberOfTweets = int(raw_input("How many tweets do you want? \n"))
except ValueError:
    print("This is not a whole number")

theIntervals = int(numberOfTweets / 25)

driver = webdriver.Firefox()
driver.get("https://twitter.com/search?f=tweets&vertical=news&q="+searchTerm+"&src=typd")

tweets=[]
timeStampsEpoc=[]
timeStamps=[]
usernames = []
tweetLinks =[]
count = 0

def _tweetCounter():
    global count
    count = 0
    counter = driver.find_elements(By.XPATH,'//*[@class="js-tweet-text-container"]')
    for thecount in counter:
        count +=1
        #print "on tweet #" +str(count)
    print "currently on this tweet "+str(count)

def _autoScroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    _tweetCounter()
    time.sleep(3)
    
def _getData():
    rawTweets = driver.find_elements(By.XPATH,'//*[@class="js-tweet-text-container"]')
    for tweet in rawTweets:
        text = tweet.text
        tweets.append(text.encode('unicode_escape'))
        #print(text)
        
    #to get time stamps    
    rawTimestamps = driver.find_elements(By.XPATH,'//small/a')
    for timestamp in rawTimestamps:
        theTimestamp = timestamp.get_attribute("title")
        timeStamps.append(str(theTimestamp))
        
    #to get username    
    userNamesList = driver.find_elements(By.XPATH,'//*[@class="stream-item-header"]')
    for user in userNamesList:
        if len(user.text) > 0:
            name = user.text
            namewithtime = name.split('@', 1)[1]
            theUserName = "@"+namewithtime.split(' ',1)[0]
            usernames.append(theUserName.encode('utf-8'))
            #print theUserName
    #print usernames
    rawLinks = driver.find_elements(By.XPATH,'//li/div')
    #print rawLinks
    for link in rawLinks:
        tweetLink = link.get_attribute("data-permalink-path")
        #print link
        if link.get_attribute("data-permalink-path"):
            thePermalink = "https://twitter.com/"+ tweetLink
            tweetLinks.append(thePermalink.encode('unicode_escape'))
            
#convert the time data into human readble format 
def _epocTimeConverter():
    for timeStamp in timeStampsEpoc:
        dt = datetime.fromtimestamp(timeStamp)
        s = dt.strftime('%Y-%m-%d %H:%M:%S')
        timeStamps.append(s)
        
startTime = 0
endTime = 0

while count < numberOfTweets:
    _autoScroll()
    startTime+=1
    #print startTime
_getData()
#_epocTimeConverter()
    
driver.quit()

#write the new csv file
targetFile = open("./"+searchTerm+".csv", "wb")
writer = csv.writer(targetFile)
writer.writerow(["User Name", "Tweet","Time","Link"])

#summarize the data for the user
#print timeStamps
print 'number of contents found:',len(tweets)
print 'number of users:',len(usernames)
print 'number of timestamp:',len(timeStamps)
print 'number of tweetLinks:',len(tweetLinks)

#zip the data up
theData=(zip(usernames,tweets,timeStamps,tweetLinks))

#write the data into the csv file
for row in theData:
    writer.writerow(row)
    #print row

#finish the script by closing the csv file and letting the user know
print "Please find your file here: "+str(targetFile)
targetFile.close()
