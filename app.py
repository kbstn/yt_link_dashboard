from scraper import create_yt_df
import streamlit as st
import pandas as pd

st.title('My yt Links')
st.markdown('This is a simple Streamlit app with a multiselect widget and a function that returns a dataframe containing yt links.')

# Set the default values for the multiselect widget
default_options = st.multiselect(
    'Select your search terms',
     ['TheViper', 'T90Official', 'SpiritOfTheLaw','Veritasium','Gamestar','PBS Eons','Kurzgesagt - in a Nutshell','Hashoshi','Be Smart']  ,
    ['TheViper', 'T90Official'])

# Add the text input widget to the app
# Split the input string into a list of strings

num_videos = st.number_input('How many searches to perform for every search?',value= 40)
# # Call the create_yt_df function and pass the results from the multiselect widget as a list
df = create_yt_df(default_options,num_videos=num_videos)

st.write(df.to_html(render_links=True,escape=False, index=False), unsafe_allow_html=True)
