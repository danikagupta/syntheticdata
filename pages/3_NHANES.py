import streamlit as st
import pandas as pd

import os
# Demographics file
dir=os.getcwd()
f_demo='nhanes_2020_demo_output_file.csv'
df_demo=pd.read_csv(dir+'/data/nhanes/'+f_demo)
print(f"DF shape demographics: {df_demo.shape}")
with st.expander("# Raw Data : Demographics"):
    st.dataframe(df_demo,hide_index=True)
df_demo_pro=df_demo
# Select Asians
df_demo_pro=df_demo_pro[df_demo_pro['RIDRETH3']==6]
with st.expander("# Asians Only : Demographics"):
    st.dataframe(df_demo_pro,hide_index=True)

#Questionnaire file
f_diq='nhanes_2020_P_DIQ_output_file.csv' 
df_diq=pd.read_csv(dir+'/data/nhanes/'+f_diq)
print(f"DF shape questionairre: {df_diq.shape}")
with st.expander("# Raw Data : Questionnaire"):
    st.dataframe(df_diq,hide_index=True)
df_diq_pro=df_diq
# Select Asians
#df_diq_pro=df_diq_pro[df_diq_pro['RIDRETH3']==6]
with st.expander("# Asians Only : Diabetes"):
    st.dataframe(df_diq_pro,hide_index=True)

