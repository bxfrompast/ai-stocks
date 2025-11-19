import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. გვერდის დიზაინის გასწორება
st.set_page_config(page_title="AI Market Watch", layout="wide", page_icon="🤖")

# სტილის დამატება (CSS)
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; border-radius: 10px; padding: 15px; margin: 10px 0;}
    h1 {color: #0e1117;}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Market Watch: ინდუსტრიის პულსი")
st.markdown("---")

# გვერდითა პანელი (Sidebar)
st.sidebar.header("პარამეტრები")
selected_period = st.sidebar.selectbox("ისტორიის პერიოდი", ['1mo', '3mo', '6mo', '1y', 'ytd'], index=1)

# ტაბების შექმნა
tab1, tab2 = st.tabs(["📈 საჯარო გიგანტები", "🦄 კერძო Unicorn-ები"])

# --- TAB 1: საჯარო კომპანიები ---
with tab1:
    tickers = ['NVDA', 'MSFT', 'GOOGL', 'META', 'AMD', 'PLTR', 'TSLA', 'IBM', 'AVGO']
    
    # მონაცემების წამოღება
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            change = ((info.last_price - info.previous_close) / info.previous_close) * 100
            data.append({
                "Symbol": ticker,
                "Price": info.last_price,
                "Change": change,
                "Volume": info.last_volume
            })
        except:
            pass
            
    df = pd.DataFrame(data)

    # ტოპ მეტრიკები
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        top_gainer = df.loc[df['Change'].idxmax()]
        col1.metric("დღის ლიდერი", top_gainer['Symbol'], f"{top_gainer['Change']:.2f}%")
        col2.metric("საშუალო ფასი", f"${df['Price'].mean():.2f}")
        col3.metric("სულ კომპანია", len(df))

        # გრაფიკის აწყობა (ყველა კომპანიის შედარება)
        st.subheader("ფასების დინამიკა")
        
        # ისტორიული მონაცემების წამოღება გრაფიკისთვის
        history_df = yf.download(tickers, period=selected_period)['Close']
        fig = px.line(history_df, title=f"აქციების ფასი - ბოლო {selected_period}")
        st.plotly_chart(fig, use_container_width=True)

        # დეტალური ცხრილი
        st.subheader("დეტალური მონაცემები")
        
        def color_change(val):
            color = '#2ecc71' if val > 0 else '#e74c3c'
            return f'color: {color}; font-weight: bold'

        st.dataframe(
            df.style.format({"Price": "${:.2f}", "Change": "{:.2f}%"}).map(color_change, subset=['Change']),
            use_container_width=True
        )

# --- TAB 2: კერძო კომპანიები ---
with tab2:
    st.info("ეს კომპანიები ჯერ არ არის საჯარო ბირჟაზე. ფასები ეფუძნება ბოლო საინვესტიციო რაუნდებს.")
    
    private_companies = [
        {"Name": "OpenAI", "Valuation": "$157 Billion", "Owner/Backer": "Microsoft / Sam Altman", "Status": "🚀 ლიდერი"},
        {"Name": "xAI", "Valuation": "$40 Billion", "Owner/Backer": "Elon Musk", "Status": "⚡ მზარდი"},
        {"Name": "Anthropic", "Valuation": "$18 Billion", "Owner/Backer": "Amazon / Google", "Status": "🛡️ უსაფრთხო AI"},
        {"Name": "Databricks", "Valuation": "$43 Billion", "Owner/Backer": "VCs", "Status": "📊 მონაცემები"},
        {"Name": "Hugging Face", "Valuation": "$4.5 Billion", "Owner/Backer": "Community", "Status": "🤗 Open Source"}
    ]
    
    p_df = pd.DataFrame(private_companies)
    st.table(p_df)
