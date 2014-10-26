import requests, bs4, sys, time

USERNAME = "username" 
PASSWORD = "password"

login_url = 'https://myvue.hsd.k12.or.us/Login_Student_PXP.aspx'
protected_url = 'https://myvue.hsd.k12.or.us/Home_PXP.aspx'

#To get this information, go to the myvue login page, press F12 > network,
#clear the entries, log on using your account, click on Login_Student_PXP.aspx
#under the network tab, and look for form data. Copy and paste all of the informations
#here
payload = {
    '__VIEWSTATE': "/wEPDwUKMTk4OTU4MDc2NWRkhaPCMTDo5uAcvztIUMPybq7F5qC35cmNiYoPt6oozZ4=",
    '__VIEWSTATEGENERATOR' : "C520BE40",
    '__EVENTVALIDATION': "/wEdAASvkKDJtIoL9ykvu7VExcu1KhoCyVdJtLIis5AgYZ/RYe4sciJO3Hoc68xTFtZGQEgSYOQVAPr9tiF9q7nSHjzonsQAUrP+el20mfFA1sZ2BeRkaGvIH+AdMJ1N3u/j8ew=",
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
