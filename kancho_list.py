import streamlit as st
import pandas as pd
import numpy as np
import pymongo


#client = pymongo.MongoClient(**st.secrets['koxia'])

level_option = st.multiselect(
    '选定所需大航海档位：',
    ['舰长', '提督', '总督'],
)

date_option = st.multiselect(
    '选定所需的上舰月份：',
    ['2021.11', '2021.12']
)

kancho_list = pd.DataFrame({
    'uid': [],
    '昵称': [],
    '大航海档位': [],
    '排名': []
})

st.dataframe(kancho_list.style.highlight_max(axis=0))
