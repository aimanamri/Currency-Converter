import streamlit as st
from bs4 import BeautifulSoup
import requests as r
import pandas as pd
import re

st.set_page_config(layout="wide")

URL = [
['機械工学課程' , 'https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=05&sc=040&page='],
['情報工学課程' , 'https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=05&sc=037&page='],
['電子システム工学課程' , 'https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=05&sc=036&page='],
['デザイン経営工学課程' , 'https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=05&sc=039&page='],
['デザイン・建築学課程','https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=06&sc=041&page='],
['応用化学課程 ','https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=08&sc=032&page='],
['応用生物学課程','https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=04&sc=032&page='],
['高分子機能工学課程','https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=04&sc=034&page='],
['物質工学課程','https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=04&sc=035&page='],
['留学生科目','https://www.syllabus.kit.ac.jp/?c=search_list&sk=00&dc=01&ac=11&page='] 
]

# # Create the pandas DataFrame for url links
df = pd.DataFrame(URL, columns=['URL', 'link'])
values = df['URL'].tolist()
options = df['link'].tolist()
dic = dict(zip(options, values))

# Side Panel
url = st.sidebar.selectbox('課程 / Program', options, format_func=lambda x: dic[x])
st.sidebar.multiselect('年次 / Year', [1,2,3,4])
st.sidebar.multiselect('学期 / Semester', ['前期','後期','第1ｸｫｰﾀ','第2ｸｫｰﾀ','通年'])

# About
st.write('''# Web Syllabus App
### Kyoto Institute of Technology (KIT)
''')

@st.cache
def main(URL):  # sourcery no-metrics
    where = URL
    courseName =[]
    classID= []
    cred_list=[]
    year_list=[]
    sem_list=[]

    pages_to_find = 20
    pages =[]
    for i in range(1,pages_to_find+1):
        urls = f'{where}{i}' 
        pages.append(urls)

    for url in pages:
        try:
            response = r.get(url).text
            soup = BeautifulSoup(response,'lxml')
            print(r.get(url)) # check if the response is OK [200]
        except:
            print("Page cannot be found. Try again.")

        # COURSE TITLE
        try:
            for x in soup.find_all('tr'):
                if x.a != None:
                    title = x.find('form').a.text
                    course_title = re.split(r'([a-zA-Z]+)', title)[0]
                    courseName.append(course_title)
        except:
                pass

        ## TIMETABLE NUMBER
        try:
            for x in soup.find_all('tr'):
                if x.a != None:
                    class_id = x.find('td').text
                    classID.append(class_id)
        except:
            pass

        ## CREDITS
        try:
            for y in soup.find('table',class_='gen_tbl2 data_list_tbl').find_all('tr'):
                if y != None:
                    credits = y.find_all('td')
                    for x in credits[4:5]:
                        data = {}
                        # print(x.text)
                        data['Credit'] = x.text
                        cred_list.append(int(x.text)) #change string to integer for credits.
        except:
            pass

        ## Year
        try:
            for y in soup.find('table',class_='gen_tbl2 data_list_tbl').find_all('tr'):
                if y != None:
                    year = y.find_all('td')
                    for x in year[6:7]:
                        # print(x.text[0])
                        data['Year'] = x.text[0]
                        year_list.append(x.text[0])
        except:
            pass

        ## SEMESTER
        try:
            for y in soup.find('table',class_='gen_tbl2 data_list_tbl').find_all('tr'):
                if y != None:
                    sm = y.find_all('td')
                    for x in sm[7:8]:
                        y = x.text
                        sem =  re.split(r'([a-zA-Z]+)', y)[0]
                        data['Semester'] = sem
                        sem_list.append(sem)
        except:
            pass

    ## Change multiple lists into a dictionary
    data = {'Timetable number' : classID,
        'Course name': courseName,
            'Credits' : cred_list,
            'Year' : year_list,
            'Semester' : sem_list
        }
    print('Retrieving data was successful !')

    ## Create dataframe from the dictionary
    df = pd.DataFrame(data=data)
    df.index+=1
    return df

df  = main(url)
st.write(df)

head = st.expander('About')
head.markdown('''
An app that will show all the results for each faculty you selected. (in-progress)
- **Python libraries: ** streamlit, pandas
- **Data source: ** [syllabus.kit.ac.jp](https://www.syllabus.kit.ac.jp/?c=menu&sk=00)
''')