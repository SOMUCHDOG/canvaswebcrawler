from os import link, name
import time
from selenium import webdriver



driver = webdriver.Chrome('chromedriver')  # Optional argument, if not specified will search path.

driver.get('#loginpageURL') #removed for github

time.sleep(2) # Let the user actually see something!

#Sign in
def signIn():
    email_box = driver.find_element_by_id('emailAddress')

    email_box.send_keys('validemail@email.com') #removed for github

    password_box = driver.find_element_by_id('password')

    password_box.send_keys('validpassword') #removed for github

    signIn_button = driver.find_element_by_class_name('btn-submit')

    signIn_button.click()

    time.sleep(5)
signIn()
#Go to modules page
driver.get('#moduleURL') #removed for github

#add all the elements with @href within the container of the models to a list
linkObj = driver.find_elements_by_xpath('//*[@id="context_modules"]//div/a[@href]')

#Add the links to an array
links = []
for lo in linkObj:
    links.append(lo.get_attribute('href'))

#Global counting variable for naming files with the same name
i=0

#Given a URL (Assuming. Could verify it is a valid URL first, but I am the only one using it so I wasn't worried.)
#Navigates the driver to the url and writes the source html to an html file.

#IN ADDITION, this script checks to see if the page has an element with class "page-number". (All of the module content was unique like this and made it easy to tell the modules apart.)
# example: 
#       Module 1, part 1, activity 3: 1.1.3
# If it does not contain the page-number it writes it with the name "Needs_name_" + the global i variable for counting and giving them unique names.
def writeFile(url):
    
    driver.get(url)
    pageSource = driver.page_source
    try:
        title = driver.find_element_by_class_name("page-number").text
    except: 
        global i 
        i+=1
        title = "Needs_name_" + str(i)
        
    title += ".html"
    fileToWrite = open("html/" + title, "w")
    fileToWrite.write(pageSource)
    print("Writing: " + url)
    fileToWrite.close()

#Saving failed links to an array to print after to identify why they failed and improve conditionals.
failedLinks = []
def savePageSource():
    

    for l in links:

        #ignore the default links because we don't need that page 25x
        if l != "modulepageURL":
            try:
                writeFile(l)
            except:
                #Some of the links failed and I couldn't pinpoint which ones. So I sent failing ones to a list to fix at a later date if needed.
                print("LINK FAILED: " + l)
                failedLinks.append(l)

#Writes the failures to a file for later reference
def failedLinksLog(list):
    #because Sometimes you need a link list and not a linked list:)
    with open("logs/log.txt", "w") as fileToWrite:
        fileToWrite.write("//MARK -- FAILED LINKS")
        fileToWrite.writelines(list)
        fileToWrite.close()
#failedLinksLog(failedLinks)


#func to append to a log
def appendToVideoLinks(url):
    fileToWrite = open("logs/videolinks.txt", "a")
    fileToWrite.write(url)
    
#Navigate the list again to find and download videos.
def getVideos(list):
    for l in list:
        driver.get(l)

        #Get the iFrames from the page (There are multiple, so we will need to find the one with a src)
        
        try:
            iFrames = driver.find_elements_by_xpath('//iframe')
            for el in iFrames:
                try:
                    iFrameSource = el.get_attribute('src')
                except:
                    return
            
            #go to the new page
            driver.get(iFrameSource)
            
            #Find the video source link
            time.sleep(3)
            source = driver.find_element_by_xpath('//video/source[@src]')

            #append that src link to a log
            appendToVideoLinks(source.get_attribute('src') + "\n")
            time.sleep(3)
        except:

            #if the above fails, skip to the next link in the list
            continue
        

getVideos(links)


time.sleep(3) # Let the user actually see something!
driver.quit()