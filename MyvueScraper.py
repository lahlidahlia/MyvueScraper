from __future__ import division
import requests, bs4, sys, time, re

username = None
password = None
try:
    login = open('credentials', 'r')
    username = login.readline().rstrip()
    password = login.readline().rstrip()
except IOError:
    login = open('credentials', 'w+')
    username = raw_input('username pls: ') + "\n"
    password = raw_input('password pls: ') + "\n"
    login.write(username)
    login.write(password)
USERNAME = username
PASSWORD = password

login_url = 'https://myvue.hsd.k12.or.us/Login_Student_PXP.aspx' #URL of the login page
destination_url = 'https://myvue.hsd.k12.or.us/PXP_Gradebook.aspx?AGU=0' #URL of where you want to go
math_url = "https://myvue.hsd.k12.or.us/PXP_Gradebook.aspx?AGU=0&DGU=0&VDT=0&CID=086C17FB-25F2-4A96-87F3-6599BE0DEB4B&MK=0EE7156A-7B5C-4F97-877A-2174168A6D15&OY=C26A5BDE-0387-4388-8855-1B81AE4C65F1&GP=1354F096-E17D-4809-91FB-C3460B815A23"

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

getGradebook = s.get(destination_url)
soup_getGradebook = bs4.BeautifulSoup(getGradebook.text)
##print soup_getGradebook.prettify()    

classesList = soup_getGradebook.find_all('a', href=re.compile("Gradebook"))
del classesList[0:8]
del classesList[-2:]
classNames = [x.get_text() for x in classesList[1::5]]

for c, i in zip(classNames, range(1, len(classNames))):
    print(str(i) + ": " + classNames[i-1])
classChoice = raw_input("Which class would you like to check your grade in? ")
chosenClass = classNames[int(classChoice) - 1]

urlChoice = soup_getGradebook.find("a", text=chosenClass)
url = "https://myvue.hsd.k12.or.us/" + urlChoice['href']
##print url

get = s.get(url)
soup_get = bs4.BeautifulSoup(get.text)

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
        weightTableDict[tdList[1].get_text()] = float(tdList[2].get_text().strip('%')) / 100
##print weightTableDict

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

percentListOfAssignments = []
for i, j in zip(listOfAssignments, range(1, len(listOfAssignments)+1)):
    # i numbering key:
    # 0: Name
    # 1: Type
    # 2: Score
    # 3: Score Type
##    print "{}: {}".format(j, i)
    if i[2] != "Not Graded" and i[2] != "Not Due": #Skip everything that's not graded because that doesn't affect grade
        if i[3] == 'Raw Score':
            scoreNumbers = i[2].split(" out of ")
    ##        score = float(scoreNumbers[0]) / float(scoreNumbers[1])
    ##        print(score)
            percentListOfAssignments.append([float(scoreNumbers[0]), float(scoreNumbers[1]), i[1]]) #Store earned points, possible points and type (for weighting)
        elif i[3] == 'Percentage':
            score = float(i[2]) / 100
            percentListOfAssignments.append([score, 1, i[1]]) #Store earned grade out of 1 (e.g. 90% -> 0.9/1) and type
        elif i[3] == 'MYP Rubric 0-8 (copy)':
            score = i[2] / 8
            percentListOfAssignments.append([score, 8, i[1]])
        elif i[3] == 'Rubric 0-4':
            score = i[2] / 4
            percentListOfAssignments.append([score, 4, i[1]])

##print percentListOfAssignments
percentWeightCategory = {}
for name, weight in weightTableDict.items():
    sumEarnedScores = 0
    sumPossibleScores = 0
    numScores = 0
    for assignment in percentListOfAssignments:
        if assignment[2] == name:
            sumEarnedScores += assignment[0]
            sumPossibleScores += assignment[1]
            numScores += 1
    percentWeightCategory[name] = sumEarnedScores / sumPossibleScores
    print("{}: {}/{}".format(name, sumEarnedScores, sumPossibleScores))

listOfWeightedPercents = []
for name, percent in percentWeightCategory.items():
    listOfWeightedPercents.append(percent * weightTableDict[name])

gradeDecimal = 0
for p in listOfWeightedPercents:
    gradeDecimal += p
gradePercent = gradeDecimal * 100
print(str(gradePercent) + "%")

print post #server response (ex. code 200, 500, etc...)
