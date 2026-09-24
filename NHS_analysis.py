import os # https://www.kaggle.com/datasets/treich/ae-attendances-england # "Has NHS A&E performance against the 4-hour waiting time target significantly declined between 2010 and 2020?"
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
new_df2 = new_df2.dropna()
print(new_df2.info())
new_df2["date"] = pd.to_datetime(new_df2["date"])
Filtered_date = (new_df2["date"] >= "2015-07-01") & (new_df2["date"] <= "2020-6-30")
new_df2_clean = new_df2[Filtered_date].copy()
new_df2_clean = new_df2_clean[
    ~((new_df2_clean["date"].dt.year == 2019) & (new_df2_clean["date"].dt.month == 4))
].copy()
new_df2_clean = new_df2_clean[new_df2_clean["Percentage in 4 hours or less (all)"] <= 1].copy()
monthly = new_df2_clean.groupby(
    pd.PeriodIndex(new_df2_clean["date"], freq="M")
)["Percentage in 4 hours or less (all)"].mean().reset_index()
print(monthly[monthly["Percentage in 4 hours or less (all)"] < 0.1])
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
plt.figure(figsize=(10, 6))
plt.plot(monthly["month_num"], monthly["Percentage in 4 hours or less (all)"], marker="o")
plt.title("NHS A&E performance within 4 hours (July 2015 - June 2020)")
plt.xlabel("Months since July 2015")
plt.ylabel("Percnatges within 4 hours")
plt.tight_layout()
plt.savefig("Genereal_NHS_Trend.png", dpi=300, bbox_inches="tight")
plt.close()
type1_pct = (new_df2_clean["Type 1 Departments - 4 hours to decision"]).sum() / (new_df2_clean["Type 1 Departments - Major A&E"]).sum() * 100 
type2_pct = (new_df2_clean["Type 2 Departments - 4 hours to decision"]).sum() / (new_df2_clean["Type 2 Departments - Single Specialty"]).sum() * 100
type3_pct = (new_df2_clean["Type 3 Departments - 4 hours to decision"]).sum() / (new_df2_clean["Type 3 Departments - Other A&E/Minor Injury Unit"]).sum() * 100
labels = ["Type 1 (Major)", "Type 2 (Single Specialty)", "Type 3 (Minor/Other)"]
values = [type1_pct, type2_pct, type3_pct]
plt.figure(figsize=(8, 5))
plt.bar(labels, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
plt.title("Percentages Of People Leaving Within 4 Hours by Department Type")
plt.ylabel("Percentage(%)")
plt.ylim(0, 100)# Keeps the scale consistent and readable
for i, v in enumerate(values):
    plt.text(i, v + 1, f"{v:.1f}%", ha= "center")
plt.tight_layout()
plt.savefig("Department_4h_percentage_change.png", dpi= 300, bbox_inches="tight")
plt.close()
#Now i must make my final analysis takeaway
print("\n" + "="*50)
print("            Final Analysis Takeaways")
print("=" * 50)
print(f". Regression R-value: r ={r_value:.3f}")
print(f". Regression P-value: p = {p_value:.10f}")
print(f". P-Value (Scientific): {p_value:.3e} ")
print(f". Percentage Within 4 Hours Type 1: %{type1_pct: .2f}")
print(f". Percentage Within 4 Hours Type 2: %{type2_pct: .2f}")
print(f". Percentage Within 4 Hours Type 3: %{type3_pct: .2f}")
