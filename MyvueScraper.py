import requests, bs4, sys, time

USERNAME = raw_input('Name pls: ') 
PASSWORD = raw_input('Password pls: ')

login_url = 'https://myvue.hsd.k12.or.us/Login_Student_PXP.aspx'
protected_url = 'https://myvue.hsd.k12.or.us/Home_PXP.aspx'



with requests.session() as s:
    get_payload = s.get(login_url)

soup = bs4.BeautifulSoup(get_payload.text)
viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

payload = {
    '__VIEWSTATE': viewstate,
    '__EVENTVALIDATION': eventvalidation,
    'username':USERNAME,
    'password':PASSWORD
}

#Do this loop until you get 200
while True:
    with requests.session() as s:
        post = s.post(login_url, data=payload) #Logging in
        get = s.get(protected_url) #Get the page you want
    if post.__bool__():
        break
    print post
    sys.stdout.flush()
    time.sleep(5)

soup_get = bs4.BeautifulSoup(get.text) #Use soup to make this pretty
soup_post = bs4.BeautifulSoup(post.content) #get the content of the post request in case of error

#print "Post content:"
#print soup_post.prettify()

print soup_get.prettify()
print "Text:"
print soup_get.get_text().split()

#print "Links:"
#for link in soup_get.find_all('a'):
#    print(link.get('href'))

print post #server response (ex. 200, 500, etc...)
print post.__bool__()
