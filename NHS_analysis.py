import os # https://www.kaggle.com/datasets/treich/ae-attendances-england
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
with open ("AE_attendances_england_monthly.csv") as f:
    df = pd.read_csv(f)
    print(df.head())
print(df.info())
new_df = df.drop_duplicates()
new_df2 = new_df.drop(columns=["Unnamed: 0", "Other Emergency admissions (i.e not via A&E)","Total attendances", "Emergency Admissions via Type 1 A&E in 4 hours", "Emergency Admissions via Type 2 A&E in 4 hours", "Emergency Admissions via Type 3 and 4 A&E in 4 hours","Number of patients spending >12 hours from decision to admit to admission", "lat", "lon"] )
new_df2.dropna()
print(new_df2.info())
new_df2["date"] = pd.to_datetime(new_df2["date"])
Filtered_date = (new_df2["date"] >= "2015-07-01") & (new_df2["date"] <= "2020-6-30")
new_df2_clean = new_df2[Filtered_date].copy()
new_df2_clean = new_df2_clean[new_df2_clean["Percentage in 4 hours or less (all)"] <= 1].copy()
monthly = new_df2_clean.groupby(pd.PeriodIndex(new_df2_clean["date"], freq= "M"))["Percentage in 4 hours or less (all)"].mean().reset_index()
print(monthly.dtypes)
monthly["month_num"] = range(len(monthly))
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(
    monthly["month_num"],
    monthly["Percentage in 4 hours or less (all)"]
)
print(f"Slope: {slope:.5f}")
print(f"R-value: {r_value:.3f}")
print(f"P-value: {p_value:.5f}")
# next do a line chart and what percentage of ach deperatment left in the time span