# FUNCTIONS RELATING TO THE DISPLAY OF DATA

# import packages
from random import randrange
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# function to highlight a column
def highlight_col(x):
    df = pd.DataFrame('', index=x.index, columns=x.columns)
    df['rollingrate'] = 'background-color: purple'
    return df

# create the data to display the areas with the greatest rolling rate, highlighting the rolling rate
def show_latest_cases(df, n):
    n = int(n)
    df = df[['areaname', 'rollingsum', 'rollingrate']]
    return df.head(n).style.apply(highlight_col, axis=None)

# Changes the format of a date string from yyyy-mm-dd to dd-mm-yyyy 
def format_date( date ):
    date = date.split("-")
    date.reverse()
    return "-".join(date)    

# display bubble chart
def bubble_chart(df, col_name, title_text, y_label, num_rows):
    # sort the data frame in descending order of the specified column
    sorted_cases_df = df.sort_values(col_name, ascending=False)

    # construct the title
    title_text = "Areas with highest rolling " + title_text + " on " + format_date(sorted_cases_df.date.max())

    # display the bubble chart
    fig = px.scatter(sorted_cases_df.head(num_rows), x='areaname', y=col_name, size=col_name, color='areaname', hover_name='areaname', size_max=60)
    fig.update_layout(title=title_text, xaxis_title="Areas", yaxis_title=y_label, width = 1000)
    fig.show()    

 # restrict a specified dataframe by the specified areaname
def get_df_area(df, areaname):
    return df[df['areaname']==areaname]
    
# select a randomly generated areaname from those available in the dataframe
def get_random_areaname(df):
    area_id = randrange(df.shape[0])
    return df["areaname"].iloc[area_id]

# plot line on graph
def plot_line(fig, df, data_field, label):
    x_data = np.asarray(df['date'])
    y_data = np.asarray(df[data_field])                 
    if len(x_data) > 0:
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode="lines", name=label, connectgaps=True))   

# display graph with a separate plot line for each column of data
def plot_cases(df, col_names, labels, graph_title, y_label):
    fig = go.Figure()
    for i, data_field in enumerate(col_names):
        plot_line(fig, df, data_field, labels[i])     
    fig.update_layout(title=graph_title, xaxis_title="Date", yaxis_title=y_label, width = 800)
    fig.show()

# display graph with a separate plot line for each area
def plot_area(df, area_names, labels):
    fig = go.Figure()
    for i, area in enumerate(area_names):
        df_area = get_df_area(df, area).sort_values('date')
        plot_line(fig, df_area, 'rollingsum', labels[i])     
    fig.update_layout(title="Cases by Specimen Date", xaxis_title="Date", yaxis_title="Rolling Sum", width = 1000)
    fig.show()