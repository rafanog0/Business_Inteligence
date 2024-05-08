import pandas as pd
import streamlit as st
from datetime import datetime
import yfinance as yf #Yahoo finance library
import os
import matplotlib.pyplot as plt

def plot_chart_stock(df):
    fig = plt.figure(figsize=(16,9))
    plt.style.use("ggplot")
    plt.barh(y = df["Categoria"], width = df["Quantidade"], height=0.3)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # plt.savefig("barh.png")
    return fig

def plot_chart_revenue(df):
    fig = plt.figure(figsize=(16,9))
    plt.style.use("ggplot")
    plt.bar(x = df["Categoria"], height = df["Revenue"], width=0.3)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # plt.savefig("bar.png")
    return fig

def plot_candles_chart(df):
    df = df.reset_index() # Default from yfinance is using date as index. Resetting makes it a column
    fig = plt.figure(figsize=(16,9))
    green_df = df[df.Close >= df.Open].copy()
    red_df = df[df.Close < df.Open].copy()
    green_df['Height'] = green_df['Close'] - green_df['Open']
    red_df['Height'] = red_df['Open'] - red_df['Close']
    plt.vlines(x = df["Date"], ymin = df['Low'], ymax = df['High'], color = 'grey')
    plt.bar(x = green_df["Date"], height = green_df['Height'], bottom = green_df['Open'], color = 'green')
    plt.bar(x = red_df["Date"], height = red_df['Height'], bottom = red_df['Close'], color = 'orangered')
    plt.xlabel("Date")
    plt.ylabel("Price")
    return fig




def main_page():
    st.markdown("# Business Inteligence")
    st.sidebar.markdown("# Business Inteligence")
    st.markdown('---')
    st.write("""
    ### Business Inteligence
    #### The goal is to create an interactive dashboard using Streamlit
    #### Pick a page in the sidebar
    """)

def page2():
    st.markdown("# Atividade 📊")
    st.sidebar.markdown("# Atividade 📊")
    df = pd.read_csv("./dados/estoque.csv")
    df_revenue = df.filter(items = ['Categoria', 'Quantidade', 'Valor'])
    df_revenue['Revenue'] = df_revenue['Quantidade'] * df_revenue['Valor']
    df_revenue = df_revenue.loc[:, df_revenue.columns != 'Valor']
    df_mostsold = df.filter(items = ['Produto', 'Quantidade'])
    df_mostsold = df_mostsold.groupby("Produto")['Quantidade'].sum()
    most_sold_item = df_mostsold.idxmax()
    st.write("""
    ### Most sold item:      
    """)
    st.write(most_sold_item)
    st.write("""
    ### Stock by Category      
    """)
    st.pyplot(plot_chart_stock(df))
    st.write("""
    ### Revenue by Category      
    """)
    st.pyplot(plot_chart_revenue(df_revenue))

def page3():
    st.markdown("# Bonus 📈")
    st.sidebar.markdown("# Bonus 📈")
    st.write("""
            
    ##### Get a candle chart by putting NYSE stock name
        ex: GOOGL, MMM, AAPL, META, JPM

    """)
    st.markdown('---')


    user_input = st.text_input("Stock Name (NYSE)", "GOOGL")
    brazil = st.checkbox(label = "Brazilian Stock?")
    if brazil:
        user_input = user_input + ".SA"
    st.metric("input", user_input, delta=None, delta_color="normal", help=None, label_visibility="hidden")
    start_date = st.date_input('Enter start date', value = datetime(2024,3,1))
    end_date = st.date_input('Enter end date')


    tickerData = yf.Ticker(user_input)
    df = tickerData.history(period = "1d", start = start_date, end = end_date)
    if(df.empty):
        st.write("### :exclamation: INVALID STOCK NAME:exclamation:")


    fig = plot_candles_chart(df)

    st.pyplot(fig)


page_names_to_funcs = {
    "Business Inteligence": main_page,
    "Atividade": page2,
    "Bonus": page3,
}
logo_path = './static/idp_logo.png'


st.sidebar.image(image = logo_path, width = 64)
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()