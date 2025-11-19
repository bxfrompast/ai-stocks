import streamlit as st
import yfinance as yf
import pandas as pd
import time

# გვერდის სათაური და პარამეტრები
st.set_page_config(page_title="AI Stocks Tracker", layout="wide")

st.title("🤖 AI კომპანიების აქციების ტრეკერი")
st.markdown("**მონაცემები ახლდება ავტომატურად რეალურ დროში.**")

# აქციების სია (შეგიძლია ჩაამატო სხვა სიმბოლოებიც)
tickers = ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMD', 'PLTR', 'IBM', 'TSLA', 'AVGO']

def get_data():
    """მონაცემების წამოღება Yahoo Finance-დან"""
    data_list = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            
            current_price = info.last_price
            previous_close = info.previous_close
            change_percent = ((current_price - previous_close) / previous_close) * 100
            
            data_list.append({
                "კომპანია": ticker,
                "ფასი ($)": round(current_price, 2),
                "ცვლილება (%)": round(change_percent, 2),
                "სტატუსი": "🟢 ზრდა" if change_percent > 0 else "🔴 კლება"
            })
        except:
            pass # თუ რომელიმე ვერ წამოიღო, არ გაჩერდეს
        
    return pd.DataFrame(data_list)

# ინტერფეისის აწყობა
placeholder = st.empty()

# ავტომატური განახლების ციკლი
while True:
    with placeholder.container():
        # მონაცემების მიღება
        df = get_data()

        if not df.empty:
            # ტოპ კომპანიის გამოვლენა
            top_gainer = df.loc[df['ცვლილება (%)'].idxmax()]
            
            # მეტრიკების ჩვენება
            col1, col2 = st.columns(2)
            col1.metric(label="🔥 დღის ლიდერი", value=top_gainer['კომპანია'], delta=f"{top_gainer['ცვლილება (%)']}%")
            col2.metric(label="სულ კომპანია", value=len(df))

            # ფერადი ცხრილის ჩვენება
            def color_status(val):
                color = 'green' if val == '🟢 ზრდა' else 'red'
                return f'color: {color}; font-weight: bold'

            st.dataframe(df.style.map(color_status, subset=['სტატუსი']), use_container_width=True)
            
            st.caption(f"ბოლო განახლება: {time.strftime('%H:%M:%S')}")
        else:
            st.error("მონაცემების წამოღება ვერ მოხერხდა. გთხოვთ დაელოდოთ...")
            
    # 1 წუთიანი პაუზა შემდეგ განახლებამდე
    time.sleep(60)
