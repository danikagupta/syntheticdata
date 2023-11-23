import streamlit as st
from streamlit_pills import pills
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import calendar
#
#

def classify_visit(days):
    if days is None or pd.isna(days):
        return 'New'
    elif days < 730:
        return 'Current'
    else:
        return 'ReEngaged'

def load_csv():
    FILENAME=os.getcwd()+"/data/"+"patient_visits.csv"
    df=pd.read_csv(FILENAME,parse_dates=["visit_date"])
    df['visit_number'] = df.groupby('patient_id')['visit_date'].cumcount()
    df['days_since_last_visit'] = df.groupby('patient_id')['visit_date'].diff().dt.days
    #df['days_since_last_visit'].fillna(0, inplace=True)
    df['category'] = df['days_since_last_visit'].apply(classify_visit)
    df.to_csv(os.getcwd()+"/data/"+"patient_visits_MOD2.csv",index=False)
    return df

def new_patients_monthly():
    df=load_csv()
    
    df = df.sort_values(by=['patient_id', 'visit_date'])
    first_visits = df.drop_duplicates(subset='patient_id', keep='first')
    current_date = datetime.now()
    current_year = current_date.year
    start_year = current_year - 3
    first_visits = first_visits[(first_visits['visit_date'].dt.year >= start_year) & (first_visits['visit_date'] <= current_date)]
    #monthly_new_patients = first_visits.groupby([first_visits['visit_date'].dt.year, first_visits['visit_date'].dt.month]).size().unstack(fill_value=0)
    
    first_visits['month'] = first_visits['visit_date'].dt.month
    first_visits['year'] = first_visits['visit_date'].dt.year

    # Group Data by Year and Month
    monthly_new_patients = first_visits.groupby(['year', 'month']).size().reset_index(name='new_patients')

    # Convert Month Numbers to Names and Sort
    monthly_new_patients['month_name'] = monthly_new_patients['month'].apply(lambda x: calendar.month_name[x])
    monthly_new_patients.sort_values(by=['year', 'month'], inplace=True)

    # Plot the Data with Plotly
    fig = px.line(monthly_new_patients, x='month_name', y='new_patients', color='year', markers=True,
                  labels={'month_name': 'Month', 'new_patients': 'Number of New Patients', 'year': 'Year'},
                  title='New Patients per Month')
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)


    # Also show the raw data
    if st.expander("Show raw data"):
        st.dataframe(monthly_new_patients)

def patients_to_date():
    df = load_csv()
    df=df[df['visit_number'] == 0]

    # Data Preparation
    #df['visit_date'] = pd.to_datetime(df['visit_date'])
    df['month_year'] = df['visit_date'].dt.to_period('M')

    # Identify Distinct Patients Up to Each Month
    # Creating a cumulative distinct count
    cumulative_patients = df.groupby('month_year')['patient_id'].nunique().cumsum().reset_index()

    # Convert Month-Year to a readable format
    cumulative_patients['month_year'] = cumulative_patients['month_year'].dt.strftime('%Y-%m')

    # Plot the Data with Plotly
    fig = px.line(cumulative_patients, x='month_year', y='patient_id', markers=True,
                  labels={'month_year': 'Month-Year', 'patient_id': 'Cumulative Distinct Patients'},
                  title='Cumulative Number of Distinct Patients Served by Month')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    # Also show the raw data
    if st.expander("Show raw data"):
        st.dataframe(cumulative_patients)

def visits_monthly():
    df=load_csv()
    
    visits=df
    current_date = datetime.now()
    current_year = current_date.year
    start_year = current_year - 3
    visits = visits[(visits['visit_date'].dt.year >= start_year) & (visits['visit_date'] <= current_date)]
    
    visits['month'] = visits['visit_date'].dt.month
    visits['year'] = visits['visit_date'].dt.year

    # Group Data by Year and Month
    monthly_visits = visits.groupby(['year', 'month']).agg(number_of_visits=('patient_id', 'size')).reset_index()

    # Convert Month Numbers to Names and Sort
    monthly_visits['month_name'] = monthly_visits['month'].apply(lambda x: calendar.month_name[x])
    monthly_visits.sort_values(by=['year', 'month'], inplace=True)

    # Plot the Data with Plotly
    fig = px.line(monthly_visits, x='month_name', y='number_of_visits', color='year', markers=True,
                  labels={'month_name': 'Month', 'number_of_visits': 'Number of Visits', 'year': 'Year'},
                  title='Visits per Month')
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)


    # Also show the raw data
    if st.expander("Show raw data"):
        st.dataframe(monthly_visits)

def patients_new_current_reengaged():
    df=load_csv()
    
    visits=df
    current_date = datetime.now()
    current_year = current_date.year
    start_year = current_year - 3
    visits = visits[(visits['visit_date'].dt.year >= start_year) & (visits['visit_date'] <= current_date)]
    
    visits['month'] = visits['visit_date'].dt.month
    visits['year'] = visits['visit_date'].dt.year

    # Group Data by Year and Month
    monthly_visits = visits.groupby(['year', 'month','category']).agg(number_of_visits=('patient_id', 'size')).reset_index()

    # Convert Month Numbers to Names and Sort
    monthly_visits['month_name'] = monthly_visits['month'].apply(lambda x: calendar.month_name[x])
    monthly_visits.sort_values(by=['year', 'month','category'], inplace=True)

    monthly_visits['year-month'] = pd.to_datetime(monthly_visits['year'].astype(str) + '-' + monthly_visits['month'].astype(str))

    # Reshape the DataFrame
    mv_long = monthly_visits.pivot_table(index='year-month', columns='category', values='number_of_visits', fill_value=0).reset_index()

    # Melt the DataFrame for Plotly
    mv_melted = mv_long.melt(id_vars=['year-month'], var_name='category', value_name='number_of_visits')

    # Create a Plotly figure
    fig = px.line(mv_melted, x='year-month', y='number_of_visits', color='category',
              title='Number of Visits by Category Over Time')
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)


    # Also show the raw data
    if st.expander("Show raw data"):
        st.dataframe(monthly_visits)

#
# Template for new dashboards
#
def XXX():
    df=load_csv()
    
    visits=df
    current_date = datetime.now()
    current_year = current_date.year
    start_year = current_year - 3
    visits = visits[(visits['visit_date'].dt.year >= start_year) & (visits['visit_date'] <= current_date)]
    
    visits['month'] = visits['visit_date'].dt.month
    visits['year'] = visits['visit_date'].dt.year

    # Group Data by Year and Month
    monthly_visits = visits.groupby(['year', 'month']).agg(number_of_visits=('patient_id', 'size')).reset_index()

    # Convert Month Numbers to Names and Sort
    monthly_visits['month_name'] = monthly_visits['month'].apply(lambda x: calendar.month_name[x])
    monthly_visits.sort_values(by=['year', 'month'], inplace=True)

    # Plot the Data with Plotly
    fig = px.line(monthly_visits, x='month_name', y='number_of_visits', color='year', markers=True,
                  labels={'month_name': 'Month', 'number_of_visits': 'Number of Visits', 'year': 'Year'},
                  title='Visits per Month')
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)


    # Also show the raw data
    if st.expander("Show raw data"):
        st.dataframe(monthly_visits)
#
#
# MAIN
#
options = ["New patients monthly","Patients-to-date", "Monthly visits",
           "Patients new vs current vs reengaged", "Visits per patient",
           "Active patients", "New patients weekly", "Patients per month" ]
made_dashboards=4
#icons=["✅","✅","✅","✅","🚧","🚧","🚧","🚧","🚧"]
icons=["✅"]*made_dashboards+["🚧"]*(len(options)-made_dashboards)
st.markdown("# Select a dashboard")
selected = pills(" ", options,icons)
#st.write("You selected:", selected)
if(selected=="New patients monthly"):
    new_patients_monthly()
elif(selected=="Patients-to-date"):
    patients_to_date()
elif(selected=="Monthly visits"):
    visits_monthly()
elif(selected=="Patients new vs current vs reengaged"):
    patients_new_current_reengaged()
else:
    st.markdown("## TBD")