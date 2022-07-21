from unicodedata import decimal
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime


st.set_page_config(
    page_title='RCN Sales External Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
)

df3 = pd.read_csv('exp.csv')
df3['tonnes'] = df3.apply(lambda row: row['Number_of_KG']/1000, axis=1)
df3['end_year'] = pd.DatetimeIndex(df3['End_Date']).year
df3['end_month'] = pd.DatetimeIndex(df3['End_Date']).month
df3['month_year'] = df3['end_month'].map(str) + '-' + df3['end_year'].map(str)

st.sidebar.header('Please Filter Here')
country = st.sidebar.multiselect(
    "Select the Country:",
    options=df3["Country"].unique(),
    default=df3["Country"].unique(),
)

month = st.sidebar.multiselect(
    "Select the Month:",
    options=df3["End_Month"].unique(),
    default=df3["End_Month"].unique(),
)

#cooperative = st.sidebar.multiselect(
    #"Select the Cooperative:",
    #options=df3["Opportunity_Organization_Name"].unique(),
    #default=df3["Opportunity_Organization_Name"].unique(),
#)

df_selection = df3.query(
    #"Country == @country & Opportunity_Organization_Name == @cooperative" 
    "Country == @country & End_Month == @month" 
)


st.title(":bar_chart: RCN Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_kg = int(df_selection["Number_of_KG"].sum())
total_sales = round(df_selection['Total_Sales_(converted)'].mean(),1)
average_price_per_kg = round(df_selection['Price_per_KG_(converted)'].mean(),0)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Metric Tonnes:")
    st.subheader(f"{int(total_kg/1000):,} MTs")

with middle_column:
    st.subheader("Total Sales:")
    st.subheader(f"USD $ {int(total_sales):,}")

with right_column:
    st.subheader("Average Price Per KG:")
    st.subheader(f"USD $ {average_price_per_kg:,}")

st.markdown("---")

volume_by_country = (
    #df_selection.groupby(by=['Country']).sum()[['Number_of_KG']].sort_values(by='Number_of_KG').round(-3)
    df_selection.groupby(by=['Country']).sum()[['tonnes']].sort_values(by='tonnes').round(-3)
)

volume_by_month = (
    #df_selection.groupby(by=['Country']).sum()[['Number_of_KG']].sort_values(by='Number_of_KG').round(-3)
    df_selection.groupby(by=['End_Month']).sum()[['tonnes']].sort_values(by='End_Month').round(-3)
)

fig_country_volume = px.bar(
    volume_by_country,
    x="tonnes",
    y=volume_by_country.index,
    orientation="h",
    title="<b> Volume of Sales</b>",
    template="plotly_white",

)

fig_month_volume = px.bar(
    volume_by_month,
    y="tonnes",
    x=volume_by_month.index,
    orientation="v",
    title="<b> Volume of Sales</b>",
    
    barmode='group',

)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_country_volume, use_container_width=True)
right_column.plotly_chart(fig_month_volume,use_container_width=True)

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """

st.markdown(hide_st_style,unsafe_allow_html=True)