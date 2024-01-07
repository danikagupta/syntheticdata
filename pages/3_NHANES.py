import streamlit as st
import pandas as pd

import os
# Demographics file
dir=os.getcwd()
f_demo='nhanes_2020_demo_output_file.csv'
df_demo=pd.read_csv(dir+'/data/nhanes/'+f_demo)
print(f"DF shape demographics: {df_demo.shape}")
with st.expander(f"# Raw Data : Demographics {df_demo.shape}"):
    st.dataframe(df_demo,hide_index=True)
df_demo_pro=df_demo
# Select Asians
df_demo_pro=df_demo_pro[df_demo_pro['RIDRETH3']==6]
df_demo_pro.to_csv(dir+'/data/nhanes/'+f_demo[:-4]+'_pro.csv',index=False)
with st.expander(f"# Aon-sians Only : Demographics {df_demo_pro.shape}"):
    st.dataframe(df_demo_pro,hide_index=True)
    st.download_button(label="Download CSV",data=df_demo_pro.to_csv(index=False),file_name='demo_pro.csv',mime='text/csv')

#Questionnaire file
f_diq='nhanes_2020_P_DIQ_output_file.csv' 
df_diq=pd.read_csv(dir+'/data/nhanes/'+f_diq)
print(f"DF shape questionairre: {df_diq.shape}")
with st.expander(f"# Raw Data : Questionnaire {df_diq.shape}"):
    st.dataframe(df_diq,hide_index=True)
df_diq_pro=df_diq
# Select Asians
df_diq_pro = df_diq_pro[df_diq_pro['SEQN'].isin(df_demo_pro['SEQN'])]
df_diq_pro.to_csv(dir+'/data/nhanes/'+f_diq[:-4]+'_pro.csv',index=False)
with st.expander(f"# Asians Only : Questionairre {df_diq_pro.shape}"):
    st.dataframe(df_diq_pro,hide_index=True)
    st.download_button(label="Download CSV",data=df_diq_pro.to_csv(index=False),file_name='diq_pro.csv',mime='text/csv')


