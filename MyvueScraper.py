import requests, bs4, sys, time

USERNAME = raw_input('User Name pls: ')
PASSWORD = raw_input('Password pls: ')




login_url = 'https://myvue.hsd.k12.or.us/Login_Student_PXP.aspx' #URL of the login page
destination_url = 'https://myvue.hsd.k12.or.us/Home_PXP.aspx' #URL of where you want to go
math_url = "https://myvue.hsd.k12.or.us/PXP_Gradebook.aspx?AGU=0&DGU=0&VDT=0&CID=866043FD-4A76-4AE3-A97E-EA655AF8117B&MK=3DCC8162-7F92-4317-AFBF-E5F464772BA0&OY=C26A5BDE-0387-4388-8855-1B81AE4C65F1&GP=B1C73921-DEB6-41E8-AA79-514267833B0A"

#Poll the login page and get the appropriate form data
get_payload = requests.get(login_url)

soup = bs4.BeautifulSoup(get_payload.text)
viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

#Form data that accompanies the POST request
payload = {
    '__VIEWSTATE': viewstate,
    '__EVENTVALIDATION': eventvalidation,
    'username':USERNAME,
    'password':PASSWORD
}

#Do this loop until you succeed (code 200)
while True:
    with requests.session() as s:
        post = s.post(login_url, data=payload) #Logging in
        
    if post.__bool__(): #If post succeeds (code 200)
        break
    
    #print out the error code and repoll every 5 seconds
    print post
    sys.stdout.flush()
    time.sleep(5)
    
get = s.get(math_url) #Get the page you want
soup_get = bs4.BeautifulSoup(get.text) #Use soup to make the page pretty
print soup_get.prettify() #Print HTMl


weightTr = soup_get.find('td', text="Weight")
weightTable = weightTr.parent.parent

weightTabEntries = [] #weightTabEntries will contain the tr which contains the td
for x in weightTable.contents:
    if x.name == 'tr':
        weightTabEntries.append(x)


weightTableDict = {} #Key: Assignment Type, Value: Weight percent
for tr in weightTabEntries:
    tdList = tr.contents
    if tdList[1].get_text() != 'Assignment Type' and tdList[1].get_text() != 'Totals':
        weightTableDict[tdList[1].get_text()] = tdList[2].get_text()
print weightTableDict

gradeTable = soup_get.find("td", text = "Score").parent.parent

gradeTableEntries = []
for i in gradeTable.contents:
    if i.name == "tr":
        gradeTableEntries.append(i)

listOfAssignments = []
for tr in gradeTableEntries:
    #tdList numbering key:
    # 0: \n
    # 1: Dates
    # 2: Assignment Name
    # 3: Assignment Type
    # 4: Resources (probably irrelevant)
    # 5: Score
    # 6: Score Type
    # 7: Notes (irrelevant)

    if tr["class"] == ["altrow1"] or tr["class"] == ["altrow2"]:
        tdList = tr.contents
        assignmentDetails = []
        assignmentDetails.extend([tdList[2].get_text(), tdList[3].get_text(), tdList[5].get_text(), tdList[6].get_text()])
        listOfAssignments.append(assignmentDetails)
        #print "1 : {}".format(tdList[2].get_text())



for i, j in zip(listOfAssignments, range(1, len(listOfAssignments))):
    print "{}: {}".format(j, i)


print post #server response (ex. code 200, 500, etc...)
