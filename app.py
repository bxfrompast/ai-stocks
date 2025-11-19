import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# გვერდის კონფიგურაცია
st.set_page_config(page_title="AI Battle Arena", layout="wide", page_icon="⚔️")

st.title("⚔️ AI Battle Arena: შეაჯიბრე გიგანტები")
st.markdown("აირჩიე ორი კომპანია და გაარკვიე, ვინ არის დღეს ბაზრის მეფე.")
st.markdown("---")

# კომპანიების სია
tickers = {
    'NVIDIA': 'NVDA', 'Microsoft': 'MSFT', 'Google': 'GOOGL', 
    'Meta': 'META', 'AMD': 'AMD', 'Tesla': 'TSLA', 
    'Intel': 'INTC', 'IBM': 'IBM', 'Palantir': 'PLTR'
}

# მებრძოლების არჩევა
col_select1, col_mid, col_select2 = st.columns([1, 0.2, 1])

with col_select1:
    fighter1_name = st.selectbox("აირჩიე მებრძოლი 1 (ლურჯი კუთხე)", list(tickers.keys()), index=0)
    fighter1_ticker = tickers[fighter1_name]

with col_select2:
    # რომ არ აირჩიოს იგივე, მეორე სიას ვაფილტრავთ
    remaining_tickers = [x for x in tickers.keys() if x != fighter1_name]
    fighter2_name = st.selectbox("აირჩიე მებრძოლი 2 (წითელი კუთხე)", remaining_tickers, index=0)
    fighter2_ticker = tickers[fighter2_name]

# მონაცემების წამოღება
def get_fighter_stats(ticker):
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    
    price = info.last_price
    prev_close = info.previous_close
    change_pct = ((price - prev_close) / prev_close) * 100
    market_cap = info.market_cap
    volume = info.last_volume
    
    return {
        "price": price,
        "change": change_pct,
        "cap": market_cap,
        "volume": volume
    }

if st.button("🔥 ბრძოლის დაწყება!"):
    with st.spinner("მონაცემების დამუშავება..."):
        f1_stats = get_fighter_stats(fighter1_ticker)
        f2_stats = get_fighter_stats(fighter2_ticker)
        
        # ქულების დათვლა
        f1_score = 0
        f2_score = 0
        
        # 1. რაუნდი: ზრდა
        if f1_stats['change'] > f2_stats['change']:
            f1_score += 1
            round1 = f"{fighter1_name}"
        else:
            f2_score += 1
            round1 = f"{fighter2_name}"
            
        # 2. რაუნდი: კაპიტალიზაცია (Market Cap)
        if f1_stats['cap'] > f2_stats['cap']:
            f1_score += 1
            round2 = f"{fighter1_name}"
        else:
            f2_score += 1
            round2 = f"{fighter2_name}"
            
        # 3. რაუნდი: ინტერესი (Volume)
        if f1_stats['volume'] > f2_stats['volume']:
            f1_score += 1
            round3 = f"{fighter1_name}"
        else:
            f2_score += 1
            round3 = f"{fighter2_name}"

        # --- ვიზუალიზაცია ---
        
        # მთავარი შედეგი
        st.markdown("### 🏆 ბრძოლის შედეგი")
        
        res_col1, res_col2, res_col3 = st.columns([1,1,1])
        
        res_col1.markdown(f"<h2 style='text-align: center; color: blue;'>{fighter1_name}</h2>", unsafe_allow_html=True)
        res_col1.markdown(f"<h1 style='text-align: center;'>{f1_score}</h1>", unsafe_allow_html=True)
        
        res_col2.markdown("<h1 style='text-align: center;'>VS</h1>", unsafe_allow_html=True)
        
        res_col3.markdown(f"<h2 style='text-align: center; color: red;'>{fighter2_name}</h2>", unsafe_allow_html=True)
        res_col3.markdown(f"<h1 style='text-align: center;'>{f2_score}</h1>", unsafe_allow_html=True)
        
        st.divider()
        
        # დეტალური შედარება
        c1, c2 = st.columns(2)
        
        # მებრძოლი 1
        with c1:
            st.info(f"🔵 {fighter1_name}")
            st.metric("ზრდა (დღეს)", f"{f1_stats['change']:.2f}%")
            st.metric("ღირებულება (Market Cap)", f"${f1_stats['cap']/1e9:.1f} B")
            st.metric("ვაჭრობის მოცულობა", f"{f1_stats['volume']:,}")

        # მებრძოლი 2
        with c2:
            st.error(f"🔴 {fighter2_name}")
            st.metric("ზრდა (დღეს)", f"{f2_stats['change']:.2f}%")
            st.metric("ღირებულება (Market Cap)", f"${f2_stats['cap']/1e9:.1f} B")
            st.metric("ვაჭრობის მოცულობა", f"{f2_stats['volume']:,}")

        # გამარჯვებულის გამოცხადება
        st.divider()
        if f1_score > f2_score:
            st.success(f"🎉 გამარჯვებულია: **{fighter1_name}**!")
            st.balloons()
        else:
            st.success(f"🎉 გამარჯვებულია: **{fighter2_name}**!")
            st.balloons()
            
else:
    st.info("აირჩიე ორი კომპანია და დააჭირე ღილაკს")

# ფუტერი
st.markdown("---")
st.caption("მონაცემები ეყრდნობა Yahoo Finance-ის ლაივ ინდიკატორებს.")
