import request
from bs4 import BeautifulSoup
url='https://www.justdial.com/Hyderabad/Online-Training-Institutes-For-Data-Science/nct-11571447'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
name1=[]
page=requests.get(url,headers=headers)
soup=BeautifulSoup(page.content,'html.parser')

name = soup.findAll("span",{'class':'lng_cont_name'})
n1=[]
for i in range(len(name)):
    n={}
    n['lng_cont_name']=name[i].text
    name1.append(n)

for i in range(len(name1)):
    n1=name1[i]
    print(n1['lng_cont_name'])

sp=soup.findAll(attrs={"class" : "cntanr"})
for i in range(len(sp)):
    op=sp[i]["data-href"]
    print(op)
