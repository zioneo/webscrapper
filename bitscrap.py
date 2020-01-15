from bs4 import BeautifulSoup
import requests
import csv
import smtplib
import pandas as pd

# Create a dictionary
d = {'key':'value'}
print(d)


# Update the dictionary
d['new key'] = 'new value'
print(d)

npo_craws = {}
row_no = 0
page_no = 0

while True:

    url = "https://bitkeys.work/?page=" + str(page_no)

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    craws = soup.find_all('div',{'class':'display-keys'})
    for craw in craws:
        address = craw.find("span", {"class":"display-keys-w-balance"}).text
        balance = craw.find("span", {"class":"balance"}).text
        rand_priv = craw.find("span", {"class":"random-generated-private-keys"}).text
        rand_balance = craw.find("span", {"class":"random-keys-balance"}).text
        row_no+=1
        npo_craws[row_no] = [address, balance, rand_priv, rand_balance]
        if rand_balance > str(0):
            msg = "found"+ " " +rand_priv+ ' ' + rand_balance
            text = msg
            server =smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login("johndoe@gmail.com", "your-password")
            fromaddr = "johndoe@gmail.com"
            toaddr = "anybBody@gmail.com"
            server.sendmail(fromaddr, toaddr, text)
            data = open("dat.txt","a")
            data.write(rand_priv+ ' ' + rand_balance + ' ' +"\n")
            data.close()
        else:
            print(rand_priv + ' ' + rand_balance)
    
    print(row_no)
    page_no+=1
    npo_craws_df = pd.DataFrame.from_dict(npo_craws, orient = 'index', columns = ['Address','Balance','Random Key', 'Random Balance'])
    npo_craws_df.head()
    npo_craws_df.to_csv('npo_craws.csv')
