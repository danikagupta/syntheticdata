import pandas as pd
import numpy as np
import os
import datetime

import streamlit as st

HOME_DIR=os.environ['CODESPACE_VSCODE_FOLDER']

def load_csv(file):
    df = pd.read_csv(file)
    return df

def clean_df(df):
    df = df[df["Label1"] == "Data"]
    df = df.loc[:, ["labid", "pid", "reqid", "delFlag", "fasting", "labsDate","bloodSugar"]]

    return df

def updateDistribution(df,num_participants = 250, start_date = datetime.date(2010, 1, 1), end_date = datetime.date(2020, 12, 31)):
    participant_ids = np.arange(1, num_participants+1)
    df["pid"] = np.random.choice(participant_ids, size=df.shape[0], replace=True)
    df["labsDate"] = [np.random.choice(pd.date_range(start_date, end_date)) for _ in range(df.shape[0])]
    
    # Add BvsF column
    df = df.sort_values(by=['pid', 'labsDate'])
    df['sequence'] = df.groupby('pid').cumcount() + 1
    df['total_labs'] = df.groupby('pid')['labsDate'].transform('size')
    df['BvsFvsL'] = df.apply(lambda row: 'B' if row['sequence'] == 1 else ('F' if row['sequence'] == 2 and row['total_labs'] > 2 else ('L' if row['sequence'] == row['total_labs'] else 'Other')), axis=1)
    df = df.drop(columns=['sequence', 'total_labs'])
    return df
    
# Populate bloodSugar column with random values
def populate_bloodSugar(df, mean=125, std=20, min=70, max=200):
    df["bloodSugar"] = np.random.normal(mean, std, df.shape[0])
    df["bloodSugar"] = df["bloodSugar"].clip(min, max)
    df["bloodSugar"] = df["bloodSugar"].round().astype(int)
    return df


def pivot_table(df):
    pivot_df = pd.pivot_table(df, values='bloodSugar', index=['pid'], columns=['BvsFvsL'], aggfunc=np.mean)
    pivot_df.columns = ['sugar_' + col for col in ['B', 'F', 'L','Other']]
    return pivot_df
 
def analyze_bloodSugar(df):
    baseline = df[df['BvsFvsL'] == 'B']
    first_followup = df[df['BvsFvsL'] == 'F']
    last_followup = df[df['BvsFvsL'] == 'L']
    #st.markdown("Baseline")
    #st.dataframe(baseline,hide_index=True)
    #st.markdown("First Follow-up")
    #st.dataframe(first_followup,hide_index=True)
    #st.markdown("Last Follow-up")
    #st.dataframe(last_followup,hide_index=True)

    baseline_mean = round(baseline['bloodSugar'].mean(), 1)
    baseline_std = round(baseline['bloodSugar'].std(), 1)

    first_followup_mean = round(first_followup['bloodSugar'].mean(), 1)
    first_followup_std = round(first_followup['bloodSugar'].std(), 1)

    last_followup_mean = round(last_followup['bloodSugar'].mean(), 1)
    last_followup_std = round(last_followup['bloodSugar'].std(), 1)

    st.markdown(f"Glucose levels at Baseline Mean: {baseline_mean} Standard Deviation: {baseline_std}")
    st.markdown(f"Glucose levels at First Follow-up Mean: {first_followup_mean} Standard Deviation: {first_followup_std}")
    st.markdown(f"Glucose levels at Last Follow-up Mean: {last_followup_mean} Standard Deviation: {last_followup_std}")

def analyze_pivot(df):
    for col in df.columns:
        if col != "pid":
            col_mean = df[col].mean()
            col_std = df[col].std()
            st.write(f"{col} Mean: {round(col_mean,1)} Standard Deviation: {round(col_std,1)}")

st.set_page_config(page_title="Data clean-up", page_icon="📹")
st.markdown("# Data clean-up")
df=load_csv(f"{HOME_DIR}/syntheticData/synthDataTblLab.csv")
st.markdown("## Original data")
st.dataframe(df)
df=clean_df(df)
df=updateDistribution(df)

df=populate_bloodSugar(df)
st.markdown("## Updated data")
st.dataframe(df)
analyze_bloodSugar(df)
pf=pivot_table(df)
st.markdown("## Pivot table")
st.dataframe(pf)
analyze_pivot(pf)



