import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil.relativedelta import relativedelta
import urllib.request
import json
import config

def get_search(body):
    url = "https://openapi.naver.com/v1/datalab/search";
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",config.CLIENT_ID)
    request.add_header("X-Naver-Client-Secret",config.CLIENT_SECRET)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        return json.loads(response.read())
    else:
        st.error("Error Code:" + rescode)
  

def get_group(selected_keyword):
    group = []
    for word in selected_keyword:
        word = {
        "groupName": word,
        "keywords": [word]
        }
        group.append(word)
    return group
    
def age_number(selected_age):
    for index, value in enumerate(selected_age):
        if value == "0∼12세":
            selected_age[index] = "1"
        elif value == "13∼18세":
            selected_age[index] = "2"
        elif value == "19∼24세":
            selected_age[index] = "3"
        elif value == "25∼29세":
            selected_age[index] = "4"
        elif value == "30∼34세":
            selected_age[index] = "5"
        elif value == "35∼39세":
            selected_age[index] = "6"
        elif value == "40∼44세":
            selected_age[index] = "7"
        elif value == "45∼49세":
            selected_age[index] = "8"
        elif value == "50∼54세":
            selected_age[index] = "9"
        elif value == "55∼59세":
            selected_age[index] = "10"
        elif value == "60세 이상":
            selected_age[index] = "11"
    return selected_age

def get_chart(data):
    df = pd.DataFrame(data["results"][0]["data"])
    df = df["period"]
    for i in range(len(group)):
        tmp = pd.DataFrame(data["results"][i]["data"])
        tmp = tmp.rename(columns={"ratio" : data["results"][i]["title"]})
        df = pd.merge(df, tmp)
    df['period'] = pd.to_datetime(df['period'])

    search_word = df.columns[1:]

    fig = plt.figure(figsize=(18.5,10))
    plt.ylabel("volume")
    for i in range(len(search_word)):
        sns.lineplot(x=df["period"], y=df[search_word[i]], label=search_word[i])
    matplotlib.rcParams["font.family"] = "Malgun Gothic" 
    return fig
    
st.title("NAVER Keyword Search Volume")

    
input = st.sidebar.text_input("Keywords","네이버",  key="keyword")

if 'keywords' not in st.session_state:
    st.session_state.keywords = []
    
list = st.session_state.keywords
if st.session_state.keyword != "":
    if len(list) < 5:
        list.append(st.session_state.keyword)
    else:
        pass
    
  
keyword = []
for word in list:
    if word not in keyword:
        keyword.append(word)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}', unsafe_allow_html=True)
selected_keyword = st.sidebar.multiselect("Selected keyword", keyword, keyword)
selected_device = st.sidebar.radio("Devicd", ("All", "Pc", "Mobile"))
selected_age = st.sidebar.multiselect("Age", ("0∼12세","13∼18세","19∼24세","25∼29세","30∼34세","35∼39세","40∼44세","45∼49세","50∼54세","55∼59세","60세 이상" ),
                                      ("0∼12세","13∼18세","19∼24세","25∼29세","30∼34세","35∼39세","40∼44세","45∼49세","50∼54세","55∼59세","60세 이상" ))
selected_gender = st.sidebar.radio("Gender", ("All", "Male", "Female"))

today = datetime.today()
startDate = (today-relativedelta(years=1)).strftime("%Y-%m-%d")
endDate = today.strftime("%Y-%m-%d") 

group = get_group(selected_keyword)

if selected_device == "All":
    selected_device = ""
elif selected_device == "Pc":
    selected_device = "pc"
else:
    selected_device = "mo"
    
selected_number = age_number(selected_age)
    
if selected_gender == "All":
    selected_gender = ""
elif selected_gender == "Male":
    selected_gender = "m"
else:
    selected_gender = "f"
    
daily = json.dumps({
  "startDate": startDate,
  "endDate": endDate,
  "timeUnit": "date",
  "keywordGroups": group,
  "device": selected_device,
  "ages": selected_number,
  "gender": selected_gender
},ensure_ascii=False)

monthly = json.dumps({
  "startDate": startDate,
  "endDate": endDate,
  "timeUnit": "month",
  "keywordGroups": group,
  "device": selected_device,
  "ages": selected_number,
  "gender": selected_gender
},ensure_ascii=False)

daily_data = get_search(daily)
daily_fig = get_chart(daily_data)
monthly_data = get_search(monthly)
monthly_fig = get_chart(monthly_data)

st.header("Daily sarch volume")
st.pyplot(daily_fig)
st.header("Monthly search volume")
st.pyplot(monthly_fig)