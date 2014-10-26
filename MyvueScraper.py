import requests, bs4, sys, time

USERNAME = raw_input('Name pls: ') 
PASSWORD = raw_input('Password pls: ')

login_url = 'https://myvue.hsd.k12.or.us/Login_Student_PXP.aspx'
destination_url = 'https://myvue.hsd.k12.or.us/Home_PXP.aspx'


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
    
get = s.get(destination_url) #Get the page you want
soup_get = bs4.BeautifulSoup(get.text) #Use soup to make the page pretty
print soup_get.prettify() #Print HTMl

#Print just the texts on the webpage
print "Text:"
print soup_get.get_text().split()

#Print all the links
#print "Links:"
#for link in soup_get.find_all('a'):
#    print(link.get('href'))

print post #server response (ex. code 200, 500, etc...)
