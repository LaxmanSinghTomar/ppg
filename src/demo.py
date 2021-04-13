# Importing Libraries & Packages
import json
import pandas as pd

import neurokit2 as nk

from collections import Counter

import streamlit as st

def create_dataframe(filename):
    data = json.load(filename)
    df1 = pd.DataFrame(data['IRLED']).T
    df1.columns = ['IRLED']
    df1['index'] = pd.DataFrame(range(len(df1)))

    df2 = pd.DataFrame(data['REDLED']).T
    df2.columns = ['REDLED']
    df2['index'] = pd.DataFrame(range(len(df2)))

    merged_df = df1.merge(df2, on = 'index')
    merged_df.drop('index', axis = 1, inplace = True)
    merged_df = merged_df.apply(pd.to_numeric)
    return merged_df


def predict(file_path):
    dataframe = create_dataframe(file_path)
    signals, info = nk.ppg_process(dataframe['IRLED'][10:-1], sampling_rate=100)
    st.pyplot(nk.ppg_plot(signals))
    label_dict = Counter(signals["PPG_Peaks"])
    if label_dict[1.0] > 1:
        pred = f'Sample is a non-resting sample!'
        return pred
    else:
        pred = (f'Sample is a resting sample!')
        return pred

st.write("""
# Rest vs. Non-Rest Classifier""")
st.write("This is a simple sample classification web app to predict whether subject's sample is Resting or not!")

file = st.file_uploader("Please upload a scan sample file", type=["json"])
if file is not None:
    with st.spinner("Prediction in Progress..."):
        prediction = predict(file)
        st.success(prediction)