from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from datetime import datetime, timezone

from pytz import timezone
import pytz

date_format='%m/%d/%Y %H:%M:%S %Z'
date = datetime.now(tz=pytz.utc)

date = date.astimezone(timezone('US/Pacific'))

update_time = date.strftime(date_format)


#Headers to parse url
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gec...: ko) Chrome/83.0.4103.97 Safari/537.36"}
url = 'https://fcfs-intl.fwc22.tickets.fifa.com/secure/selection/event/date/product/101397570845/lang/en'

#Url Vs
url_match = 'https://www.roadtrips.com/world-cup/2022-world-cup-packages/schedule/'




#Send page and headers
page = requests.get(url,headers=headers)
page_with_display_none = requests.get(url,headers=headers)
page_team_1 = requests.get(url_match,headers=headers)
page_team_2 = requests.get(url_match,headers=headers)


#Parse html
soup = BeautifulSoup(page.content, 'html.parser')
soup_find_display_none = BeautifulSoup(page_with_display_none.content, 'html.parser')
soup_matche_team_1 = BeautifulSoup(page_team_1.content, 'html.parser')
soup_matche_team_2 = BeautifulSoup(page_team_2.content, 'html.parser')

#Set the class that contains all the match information and its parent tag
all_data = soup.find_all('div', class_='performance_container') 
all_data_display_none = soup_find_display_none.find_all('ul', class_='performances_sub_group_container') 
data_team1_from_page = soup_matche_team_1.find_all('td', class_='column-2')
data_team2_from_page = soup_matche_team_2.find_all('td', class_='column-4')

stateStr=""
count=0
data_into_alist  = list()
data_display_none_into_alist = list()
data_category = list() 
data_list = []
data_list_none = []
data_list_display_none = []
team1_data_list = []
team2_data_list = []
list_index = []
final_list= []

#For to add team 1 to list
for i in data_team1_from_page:
    team1_data_list.append(i.text)


#For to add display none to alist
for i in all_data_display_none:
    data_list_display_none.append(i.text)


#For to add team 2 to list
for i in data_team2_from_page:
    team2_data_list.append(i.text)

#For to add items to a list
for i in all_data:
    data_into_alist.append(i.text)


#print(data_list_display_none)   

#Remove all garbage
special_char = '@_!#$%^&*()<>?/\|}{~:;.[]\n\r\t'
#General
out_list = [''.join(filter(lambda i: i not in special_char, string)) for string in data_into_alist]
#Display none
out_list_none = [''.join(filter(lambda i: i not in special_char, string)) for string in data_into_alist]

#general
string_clean = ''.join(map(str, out_list))
new_list_clean = string_clean.split()
data_list = ','.join(map(str, new_list_clean))


#none
string_clean_none = ''.join(map(str, out_list_none))
new_list_clean_none = string_clean_none.split()
data_list_none = ','.join(map(str, new_list_clean_none))
#print(data_list_none)

#Final clean list
lista = data_list.split(',')


#Final clean list none
lista_none = data_list_none.split(',')

#print(lista_none)



cc =[]
counturl=0
for j in range(0,64):
    counturl += 1
    id_tikect = 101437163854+counturl  
    url_tikect = 'https://fcfs-intl.fwc22.tickets.fifa.com/secure/selection/event/seat/performance/'+str(id_tikect)+'/lang/en'

#    url_tikect = 'https://fcfs-intl.fwc22.tickets.fifa.com/secure/selection/event/seat/performance/101437163855/lang/en'
#Send page and headers
    page = requests.get(url_tikect,headers=headers)
    #Parse html
    soup = BeautifulSoup(page.content, 'html.parser')

    #Set the class that contains all the match information and its parent tag
    all_data1 = soup.find_all('div', class_='category_unavailable_overlay') 
    #all_data = soup.find_all('class', class_='color') 
    countEl =0;
    for k in all_data1:
        data_category.append(k.text)
        #Remove all garbage
        special_char = '@_!#$%^&*()<>?/\|}{~:;.[]\n\r\t'
        #General
        out_list = [''.join(filter(lambda k: k not in special_char, string)) for string in data_category]
    
        #general
        string_clean = ''.join(map(str, out_list))
        new_list_clean = string_clean.split()
        data_list_c = ','.join(map(str, new_list_clean))
    
        #Final clean list
            
        lista_c = data_list_c.split(',')
        #lista_ca= lista_c.strip()
        #print(lista_c)
    
    cc.append(lista_c[0])
    cc.append(lista_c[1])
    cc.append(lista_c[2])

print(len(cc))
print(cc)


#Find a string that is repeated in all matches
#To take it as a reference and work
#The list starting from that element
#And generate the index of the list to iterate
for i in range(0,len(lista_none)):
    if('Stadium' in lista_none[i] ):
        list_index.append(i)
        count += 1
        id_tikect = 101437163854+count  
        url_tikect = 'https://fcfs-intl.fwc22.tickets.fifa.com/secure/selection/event/seat/performance/'+str(id_tikect)+'/lang/en'
        #Send page and headers
        page = requests.get(url_tikect,headers=headers)
        #Parse html
        soup = BeautifulSoup(page.content, 'html.parser')

        #Set the class that contains all the match information and its parent tag
        all_data = soup.find_all('span', class_='text') 


cuenta = 0
#Iterating the indexes to find available tickets
for i in range(len(list_index)):      
    for j in range(list_index[i],list_index[i]+1):
         if lista_none[j+3] == 'Limited' or lista_none[j+3] == 'availability' or  lista_none[j+3] == 'Low' or lista_none[j+3] == 'Currently' or lista_none[j+3]== 'unavailable' or lista_none[j+3]=='This':
            state = 'Not available'
         else:
            state = 'Available'
         cuenta += 1
         id_tikect = 101437163854+count
         
         if(lista_none[j+3]== 'Limited'):
             stateStr = 'Limited Availability'


         if(lista_none[j+3]== 'Low'):
             stateStr = 'Low Availability'



         if(cc[0]=='Currently'):
             cat1 = 'Not available'
         else:
             cat1 = 'Available'

         if(cc[1]=='unavailableCurrently'):
             cat2 = 'Not available'

         else:
             cat2 = 'Available'

         if(cc[2]=='unavailableCurrently'):
             cat3 = 'Not available'
        
         else:
             cat3 = 'Available'
         matchesV = {'Match': 'M'+str(cuenta) ,'HomeTeam': team1_data_list[i] ,'AwayTeam': team2_data_list[i] , 'Status': state, 'StateDesc': 'Low Availability', 'Category1': cat1, 'Category2': cat2, 'Category3': cat3, 'Buy': 'https://fcfs-intl.fwc22.tickets.fifa.com/secure/selection/event/seat/performance/'+str(id_tikect)+'/lang/en', 'UpdateAt': update_time}
         final_list.append(matchesV)
         del cc[0:2]   
#Conver into json

json_dump = json.dumps(final_list)
with open('fifa.json', 'w') as f:
    f.write(json_dump)
    print("The json file is created")
print(json_dump)
