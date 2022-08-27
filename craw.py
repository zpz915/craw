import pandas as pd
from lxml import etree
import json
import requests
data_list = []
for i in range(0,6660,10):
    url = 'https://api.finder.partners.aws.a2z.com/search?locale=en&highlight=on&sourceFilter=searchPage&size=10'+'&from='+str(i)

    response = requests.get(url=url)
    response.encoding = 'utf-8'
    data = response.text
    data_dict = json.loads(data)

    for j in data_dict['message']['results']:
        id = j['_id']
        txt = j['_source']
        name = txt['name']
        url = 'https://api.finder.partners.aws.a2z.com/search?id='+str(id)+'&locale=en&sourceFilter=detailPage'
        response = requests.get(url=url)
        response.encoding = 'utf-8'
        data1 = response.text
        data_dict1 = json.loads(data1)
        #if data_dict1['message']['_source'].get()
        address_list = data_dict1['message']['_source'].get('office_address','none')
        if isinstance(address_list,str):
            data = dict()
            data['id'] = id
            data['name'] = name
            data['address'] = address_list
        else:
            data = dict()
            data['id'] = id
            data['name'] = name
            data['address'] = address_list[0]['country'] + address_list[0]['street']
        #address_list = data_dict1['message']['_source']['office_address']
        # address_los = []
        # for j in address_list:
        #     country = j['country']
        #     street = j['street']
        #     address_los.append(country+street)
        #n = len(address_list)

        # for i in range(n):
        #     data['address'+str(i)] = address_list[i]['country'] + address_list[i]['street']
        data_list.append(data)

df = pd.DataFrame(data_list)
df.to_excel('{}.xlsx'.format('infro'))
print(data_dict)
print(type(data_dict))
