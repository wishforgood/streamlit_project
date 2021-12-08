import streamlit as st
import pandas as pd
import numpy as np
import pymongo


client = pymongo.MongoClient('mongodb://koxia:koxia@localhost:27017/kancho_info')
db = client['kancho_info']
collection = db['kancho_list']
kancho_level_names = ['舰长', '提督', '总督']


date_option = st.multiselect(
    '选定所需的上舰月份：',
    ['2021,12', '2022,1']
)

level_option = []
for ind in range(len(date_option)):
    current_level_option = st.multiselect(
        '选定'+ date_option[ind] +'所需大航海档位：',
        kancho_level_names,
        key=ind
    )
    level_option.append(current_level_option)

@st.cache(ttl=600)
def get_data():
    items = collection.find()
    items = list(items)
    return items

kancho_info = get_data()
kancho_list = pd.DataFrame({
    'uid': [],
    '昵称': [],
    '大航海档位': [],
})
for kancho_ in kancho_info:
    if kancho_['register_date'] not in date_option:
        continue
    for ind in range(len(level_option)):
        current_level_option = level_option[ind]
        kancho_level = kancho_level_names[len(kancho_level_names) - int(kancho_['kancho_level'])]
        if kancho_level in current_level_option and kancho_['register_date'] == date_option[ind]:
            kancho_list = kancho_list.append(pd.DataFrame({
                                      'uid': int(kancho_['kancho_uid']), 
                                      '昵称': kancho_['kancho_nickname'],
                                      '大航海档位': kancho_level,
                                      }, index=[int(kancho_['kancho_rank'])]) 
                                     )   
st.dataframe(data=kancho_list.style.format({'uid': '{:10.0f}', '大航海档位': '{:10}'}),
             width=2048, height=768)
@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(kancho_list)

st.download_button(
     label="下载",
     data=csv,
     file_name='大航海信息.csv',
     mime='text/csv',
 )
