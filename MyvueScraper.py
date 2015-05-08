import requests, bs4, sys, time

USERNAME = raw_input('Name pls: ') 
PASSWORD = raw_input('Password pls: ')

login_url = 'https://myvue.hsd.k12.or.us/Login_Student_PXP.aspx'
destination_url = 'https://myvue.hsd.k12.or.us/Home_PXP.aspx'
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

#Print just the texts on the webpage
print "Text:"
#print soup_get.get_text().split()

#for stuffs in soup_get.find_all('td'):
#    print(stuffs.get('a'))

#Get all the texts from the page and turn it into a single string
#all_texts = []
#for s in soup_get.find_all('td'):
#    print(s);

weightTr = soup_get.find('td', text="Weight")
weightTable = weightTr.parent.parent
i = 0
print(weightTable)
weightTabEntries = None
for x in weightTable.contents:
    print(x.name)
    if x.name == 'td':
        weightTabEntries.put(x)
print(weightTabEntries)
        
#for i in range(1, len(weightTable.contents) - 1):
#    print(weightTable.contents[i])

#Print all the links
#print "Links:"
#for link in soup_get.find_all('a'):
#    print(link.get('href'))

print post #server response (ex. code 200, 500, etc...)
