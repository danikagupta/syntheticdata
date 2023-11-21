import csv
from datetime import datetime, timedelta
import random
import time
import numpy as np
import streamlit as st
import os

MIN_PATIENT_ID=10001
FILENAME=os.getcwd()+"/data/"+"patient_visits.csv"

def init_session_state():
    if "current_patient_id" not in st.session_state:
        st.session_state.current_patient_id=MIN_PATIENT_ID
    if "patient_visit_data" not in st.session_state:
        st.session_state.patient_visit_data=[]

def reset_info():
    if "current_patient_id" in st.session_state:
        del st.session_state.current_patient_id
    if "patient_visit_data" in st.session_state:
        del st.session_state.patient_visit_data

def random_date_in_month(year,month):
    return datetime(year,month,random.randint(1,28))

def increment_month(month,year):
    month+=1
    if month>12:
        month=1
        year+=1
    return month,year

def in_the_past(month,year):
    current_month=datetime.now().month
    current_year=datetime.now().year
    if year<current_year:
        return True
    elif year==current_year and month<current_month:
        return True
    else:
        return False

def generate_patient_data_month(year,month,new_patients,visits_per_month):
    l=st.session_state.current_patient_id+1
    m=l+new_patients
    print(f"Generating patient data for {year}-{month:02d} ({new_patients} patients) with visits per month {visits_per_month}")
    for i in range(l,m):
        st.session_state.current_patient_id=i
        patient_id = f"PAT-{i:06d}"
        visit_date=random_date_in_month(year,month)
        st.session_state.patient_visit_data.append([patient_id,visit_date.strftime("%Y-%m-%d"),random.randint(15,120)])
        new_month,new_year=increment_month(month,year)
        while(in_the_past(new_month,new_year)):
            if(random.random()<visits_per_month):
                visit_date=random_date_in_month(new_year,new_month)
                st.session_state.patient_visit_data.append([patient_id,visit_date.strftime("%Y-%m-%d"),random.randint(15,120)])
            new_month,new_year=increment_month(new_month,new_year)
    return

        

def generate_patient_data(initial_patients, growth_rate, start_year, start_month, visits_per_month):
    year=start_year
    month=start_month
    patients=initial_patients
    init_session_state()
    generate_patient_data_month(year,month,patients,visits_per_month)
    while(in_the_past(month,year)):
        new_patients=int(patients*growth_rate/12)
        if(random.random()<patients*growth_rate/12-new_patients):
            new_patients+=1
        month,year=increment_month(month,year)
        generate_patient_data_month(year,month,new_patients,visits_per_month)
        patients+=new_patients
    return

def save_to_file():
    with open(FILENAME,"w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["patient_id","visit_date","visit_duration"])
        for row in st.session_state.patient_visit_data:
            writer.writerow(row)
    return

def generate_patient_visit_data():
    st.markdown("## Generate patient visit data")
    st.markdown("### Patient data")
    initial_patients=st.slider("Initial number of patients",min_value=1,max_value=1000,value=100)
    growth_rate=st.slider("Growth rate of patients (per year)",min_value=0.0,max_value=1.0,value=0.1)
    start_year=st.slider("Start year",min_value=2010,max_value=2023,value=2020)
    start_month=st.slider("Start month",min_value=1,max_value=12,value=1)
    visits_per_month=st.slider("Visits per month",min_value=0.0,max_value=1.0,value=0.1)
    st.markdown("### Generate data")
    if st.button("Generate patient visit data"):
        reset_info()
        generate_patient_data(initial_patients, growth_rate, start_year, start_month, visits_per_month)
        st.success("Patient visit data generated")

        st.markdown("### Patient visit data")
        st.markdown(f"## Number of patients: {st.session_state.current_patient_id-MIN_PATIENT_ID}. "+
                f"Number of records: {len(st.session_state.patient_visit_data)}")
        save_to_file()
        st.dataframe(st.session_state.patient_visit_data)
    return


st.set_page_config(page_title="Generate patient visit data", page_icon="📈")
st.markdown("# Generate patient visit data")
generate_patient_visit_data()

