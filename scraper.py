import pandas as pd
import datetime
from youtubesearchpython import *
import numpy as np


def string_to_delta(string_delta):
    """Convert a string representing a time duration, such as '5 days ago', into a datetime.timedelta object.
    
    Args:
    - string_delta: str. A string representation of a time duration, such as '5 days ago'.
    
    Returns:
    - datetime.timedelta: A datetime.timedelta object representing the time duration.
    - np.nan: If the input string is empty or None, or if the unit of time is 'month'.
    
    """
    # If the input string is empty or None, return np.nan
    if not string_delta:
        return np.nan
    
    # Remove the word 'Streamed' from the beginning of the string if present
    if string_delta.startswith('Streamed'):
        string_delta=string_delta[8:]
    
    # Split the string into the value, unit, and any additional text
    value, unit, _ = string_delta.split()
    
    # Convert 'day' and 'hour' to the plural form 'days' and 'hours'
    if unit == 'day':
        unit = 'days'
    if unit == 'hour':
        unit = 'hours'
    
    # If the unit of time is 'month', return np.nan
    if unit == 'month':
        return np.nan
    
    # Convert the value and unit into a datetime.timedelta object
    return datetime.timedelta(**{unit: float(value)})


def create_yt_df(channel_names, num_videos=40):
    """Create a dataframe containing YouTube video data for the given channel names.
    
    Args:
    - channel_names: list of str. A list of YouTube channel names.
    - num_videos: int. The number of videos to retrieve for each channel. Default is 40.
    
    Returns:
    - pd.DataFrame: A dataframe containing the following columns:
        - 'title': str. The title of the video.
        - 'duration': str. The duration of the video.
        - 'published_time': str. The date and time when the video was published, in the format 'N days/hours/minutes ago'.
        - 'link': str. The URL of the video.
        - 'channel_name': str. The name of the channel that published the video.
        - 'publish_delta': datetime.timedelta. The time since the video was published, as a `datetime.timedelta` object.
    """
    # Create a list to collect all the dataframes for later concatenation
    channel_dfs = []
    
    # Iterate over the channel names
    for channel in channel_names:
        # Retrieve the specified number of videos from the last month containing the channel name
        custom_search = CustomSearch(channel, VideoUploadDateFilter.thisMonth, limit=num_videos)
        
        # Extract the results into a dictionary
        result_dict = custom_search.result()
        
        # Create a dataframe from the dictionary
        channel_df = pd.concat({k: pd.DataFrame(v).T for k, v in result_dict.items()}, axis=0).T
        
        # Remove the multi-level columns
        channel_df.columns = channel_df.columns.droplevel()
        
        # Keep only the relevant columns
        channel_df = channel_df[['title', 'duration', 'publishedTime', 'link', 'channel']]
        
        # Extract the name of the channel from the 'channel' column
        channel_df['channel_name'] = channel_df.channel.apply(pd.Series)['name']
        
        # Convert the 'publishedTime' column from a string to a datetime.timedelta object
        channel_df['publish_delta'] = channel_df.publishedTime.map(string_to_delta)
        
        # Add the dataframe for this channel to the list
        channel_dfs.append(channel_df)
    
    # Concatenate all the dataframes and sort by 'publish_delta'
    result_df = pd.concat(channel_dfs, axis=0)
    result_df = result_df.drop(columns=['channel'])
    result_df['Url'] = '<a href=' + result_df['link'] + '><div>' + result_df['title'] + '</div></a>'
    result_df = result_df[['Url','duration','publishedTime','channel_name','publish_delta']]
    result_df = result_df.sort_values(by='publish_delta')
    
    return result_df

if __name__ == "__main__":
    # This is an example list of channel names that you want to scrape
    channel_names = ['TheViper', 'T90Official', 'SpiritOfTheLaw','Veritasium','Gamestar','PBS Eons','Kurzgesagt - in a Nutshell','Hashoshi','Be Smart']  
    result=create_yt_df(channel_names,num_videos=100)
    # Convert the DataFrame to HTML
    html = result.to_html(render_links=True,
        escape=False)

    # Write the HTML to a file
    with open('index.html', 'w') as f:
        f.write(html)