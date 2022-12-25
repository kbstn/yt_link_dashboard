from scraper import create_yt_df
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")



st.title('My yt Links')
st.markdown('This is a simple Streamlit app with a multiselect widget and a function that returns a dataframe containing yt links.')

# serach terms
search_terms=['TheViper', 'T90Official - Age Of Empires 2', 'Spirit Of The Law','Veritasium','Gamestar','PBS Eons','Kurzgesagt – In a Nutshell',
     'Hashoshi','Be Smart','Real Science','Two Minute Papers','Vsauce','Daniel Madison','BeHaind','Chris Ramsay',
     'Doug Conn','Heath Cards','Mike Boyd','Siegismund'] 

# channel names as listed in channel_name, filtering for them will drop videos from other channels wich might occur in the search results
channel_names = ['TheViper', 'T90Official - Age Of Empires 2', 'Spirit Of The Law','Veritasium','Gamestar','PBS Eons','Kurzgesagt – In a Nutshell',
     'Hashoshi','Be Smart','Real Science','Two Minute Papers','Vsauce','Daniel Madison','BeHaind','Chris Ramsay',
     'Doug Conn','Heath Cards','Mike Boyd','Siegismund']
# Set the default values for the multiselect widget
default_options = st.multiselect(
    'Select your search terms',search_terms
      ,search_terms)
    # ['Kurzgesagt - in a Nutshell'] )


# Add the text input widget to the app
# Split the input string into a list of stringszz

num_videos = st.number_input('How many searches to perform for every search?',value= 40)
# # Call the create_yt_df function and pass the results from the multiselect widget as a list
df = create_yt_df(default_options,num_videos=num_videos)
df2= df[df['channel_name'].isin(channel_names)]
st.write(df2.to_html(render_links=True,escape=False, index=False), unsafe_allow_html=True)
