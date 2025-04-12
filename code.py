import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk #python version of deck.gl by uber
import plotly.express as px #used to create intractive plots

DATA_URL= (
"/home/rhyme/Desktop/Project/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This Application is a Streamlit Application that can be used to analyse motor vehical collision ")

@st.cache(persist=True)  #so we have to run below code only if input is changed & not everytime
def load_data(nrows):
    data=pd.read_csv(DATA_URL,nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True) #so to drop na value as streamlit cant take them
    lowercase=lambda x: str(x).lower()  #to change in lower case
    data.rename(lowercase,axis='columns',inplace=True) #change coloum name to lowercase
    data.rename(columns={'crash_date_crash_time':'date/time'},inplace=True)
    return data

data=load_data(100000)
original_data=data

st.header("Where are the most people injured in NYC")
injured_people=st.slider("Number of person injured in vehical collision",0,19) #to add a slider
st.map(data.query("injured_persons>= @injured_people")[["latitude","longitude"]].dropna(how="any")) #to add map that take particular value from table and inserted a query

st.header("How many collision occur during a given time a day")
hour=st.slider("Hour to look at",0,23) #draw slider on s
data=data[data['date/time'].dt.hour==hour] #using panada date time lib(dt.hour) to equate to time date

st.markdown("Vehicle Collision between %i:00 and %i:00" %(hour,(hour+1) %24)) #to write a subtext and using special charecter to apop on text as you move the slider by assigning the special operator the value as given

midpoint=(np.average(data['latitude']),np.average(data['longitude'])) #calculating the midpoint for intialising the map later

st.write(pdk.Deck(    #using pydeck port
   map_style="mapbox://styles/mapbox/light-v9",  #using v9 mapstyle and specifying the path
   initial_view_state={
     "latitude":midpoint[0],      #initialising the map with intial parameters by forming a initial value dictionery
     "longitude":midpoint[1],
     "zoom":11,
     "pitch":50,
  },
  layers=[
    pdk.Layer(      #pdk layer tool to add content in our map and make 3d representation
    "HexagonLayer", #to make point hexagon as by default it is circle
    data=data[['date/time','latitude','longitude']],
    get_position=['longitude','latitude'],
    radius=100,       #for the radius of dots
    extruded=True,    #it makes the map 3d
    pickable=True,
    elevation_scale=4,                         #scale and range parameter are used to set the height of bars
    elevation_range=[0,1000],
    ),
  ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" %(hour,(hour+1)%24))
filtered=data[
 (data['date/time'].dt.hour>=hour)&(data['date/time'].dt.hour<(hour+1)) #take value between hour and hour +1
]
hist=np.histogram(filtered['date/time'].dt.minute,bins=60,range=(0,60))[0] #histogram to take parameter as min(60)
chart_data=pd.DataFrame({'minute':range(60), 'crashes':hist}) #to set a new data frame with 2 coloums
fig=px.bar(chart_data,x='minute',y='crashes',hover_data=['minute','crashes'],height=400) #to draw bar chart
st.write(fig) #to display

st.header("Top 5 Dangerous Streets")
select=st.selectbox('Affected type of people',['Pedestrians','Cyclists','Motorists']) #for drop down box

if select=='Pedestrians':
    st.write(original_data.query("injured_pedestrians >=1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'],ascending=False).dropna(how='any')[:5])
    #this above line sort the values from original data file and return the street name and injusred pedestrian of top 5
    #to show top 5 Dangerous street
elif select=='Cyclists':
    st.write(original_data.query("injured_cyclists >=1")[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'],ascending=False).dropna(how='any')[:5])
 
else:
    st.write(original_data.query("injured_motorists >=1")[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'],ascending=False).dropna(how='any')[:5])

if st.checkbox("Show Raw Data ",False): #checkbox initially false(unchecked) when click show Data
    st.subheader('Raw Data') #giving subheading
    st.write(data)  #To display raw tabular Data
app.py
Displaying app.py.
