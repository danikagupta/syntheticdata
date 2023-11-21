import streamlit as st
from streamlit_pills import pills
import pandas as pd
import os
#
#

def load_csv():
    FILENAME=os.getcwd()+"/data/"+"patient_visits.csv"
    df=pd.read_csv(FILENAME,parse_dates=["visit_date"])
    return df


options = ["Patients-to-date", "Active patients", "New patients monthly", 
           "Visits per month", "Visits per patient", "New vs returning patients" ]
st.markdown("# Select a dashboard")
selected = pills(" ", options,None)
st.write("You selected:", selected)
if(selected=="Patients-to-date"):
    st.write("Patients-to-date")
    st.write("This is the number of patients who have visited the clinic since the beginning of the year.")
    df=load_csv()
    df2=df.groupby("patient_id").count()
    st.write(df2.shape[0])
elif(selected=="Active patients"):
    st.write("Active patients")
    st.write("This is the number of patients who have visited the clinic in the last 6 months.")
    df=load_csv()
    df2=df.groupby("patient_id").count()
    df3=df2[df2["visit_date"]>1]
    st.write(df3.shape[0])
elif(selected=="New patients monthly"):
    st.write("New patients monthly")
    st.write("This is the number of new patients who have visited the clinic each month.")
    df=load_csv()
    df2=df.groupby(["year","month"]).count()
    st.line_chart(df2["patient_id"])
elif(selected=="Visits per month"):
    st.write("Visits per month")
    st.write("This is the number of visits per month.")
    df=load_csv()
    df2=df.groupby(["year","month"]).count()
    st.line_chart(df2["visit_date"])
elif(selected=="Visits per patient"):
    st.write("Visits per patient")
    st.write("This is the number of visits per patient.")
    df=load_csv()
    df2=df.groupby("patient_id").count()
    st.line_chart(df2["visit_date"])
elif(selected=="New vs returning patients"):
    st.write("New vs returning patients")
    st.write("This is the number of new patients vs returning patients each month.")
    df=load_csv()
    df2=df.groupby(["year","month"]).count()
    df3=df2[df2["patient_id"]==1]
    df4=df2[df2["patient_id"]>1]
    st.line_chart(df3["patient_id"],df4["patient_id"])
else:
    st.write("Unknown selection")