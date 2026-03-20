import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# --- PROFESYONEL SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="KODALAN | Endüstriyel Optimizasyon",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ŞIK ARAYÜZ TASARIMI (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #00c853, #b2ff59);
        color: black; border: none; font-weight: bold; border-radius: 8px; width: 100%; height: 45px;
    }
    .status-card { background-color: #1c2128; padding: 20px; border-radius: 15px; border-left: 5px solid #00c853; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ YÖNETİMİ ---
def init_db():
    conn = sqlite3.connect('kodalan_v3.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Envanter 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, malzeme TEXT, en REAL, boy REAL, tarih TEXT, verimlilik REAL)''')
    conn.commit()
    return conn

db = init_db()

# --- KENAR ÇUBUĞU (KONTROL PANELİ) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00c853;'>K O D A L A N</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Endüstriyel Verimlilik Yazılımı</p>", unsafe_allow_html=True)
    st.divider()
    
    with st.expander("📥 Yeni Materyal Kaydı", expanded=True):
        mat_type = st.selectbox("Materyal Tipi", ["Premium Panel", "Standart MDF", "Alüminyum Levha", "Endüstriyel Cam"])
        width = st.number_input("Genişlik (cm)", min_value=1.0)
        height = st.number_input("Boy (cm)", min_value=1.0)
        
        if st.button("Veritabanına İşle"):
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            # Rastgele bir verimlilik skoru simülasyonu
            score = 100.0
            cur = db.cursor()
            cur.execute("INSERT INTO Envanter (malzeme, en, boy, tarih, verimlilik) VALUES (?, ?, ?, ?, ?)", 
                        (mat_type, width, height, now, score))
            db.commit()
            st.toast(f"{mat_type} başarıyla kaydedildi!", icon='✅')

    st.divider()
    st.caption("v3.0.1 Stable Release")

# --- ANA DASHBOARD ---
# 1. Satır: Metrikler
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Kar Marjı Artışı", "%18.4", "+2.1")
with m2: st.metric("Atık Azaltımı", "540 kg", "-%32")
with m3: st.metric("Aktif Dijital Stok", "128 Adet", "Canlı")
with m4: st.metric("Karbon Kredisi", "4.2", "Sınıf: A")

st.divider()

# 2. Satır: Ana Fonksiyonlar
tab_opt, tab_data, tab_stats = st.tabs(["🎯 Akıllı Optimizasyon", "📦 Dijital Envanter", "📈 Analitik Raporlar"])

with tab_opt:
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown("<div class='status-card'><h4>İhtiyaç Analizi</h4>", unsafe_allow_html=True)
        target_w = st.number_input("Hedef Genişlik (cm)", key="tw")
        target_h = st.number_input("Hedef Boy (cm)", key="th")
        if st.button("En Uygun Kaynağı Ata"):
            df = pd.read_sql_query("SELECT * FROM Envanter", db)
            match = df[(df['en'] >= target_w) & (df['boy'] >= target_h)]
            
            if not match.empty:
                best = match.iloc[0]
                st.success(f"Eşleşme Bulundu! ID: #{best['id']}")
                st.balloons()
            else:
                st.warning("Uygun stok bulunamadı. Yeni üretim emri oluşturulmalı.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("#### Simülasyon Görünümü")
        # Basit bir kesim planı görseli simülasyonu
        st.info("Algoritma çalışıyor: En uygun yerleşim planı (Nesting) hesaplanıyor...")
        st.image("https://via.placeholder.com/800x400.png?text=Kesim+Plani+Simulasyonu+Gosteriliyor", use_container_width=True)

with tab_data:
    st.markdown("#### SQL Tabanlı Envanter Takibi")
    full_df = pd.read_sql_query("SELECT * FROM Envanter ORDER BY id DESC", db)
    st.dataframe(full_df, use_container_width=True)
    
    if st.button("Veritabanını Sıfırla"):
        db.cursor().execute("DELETE FROM Envanter")
        db.commit()
        st.rerun()

with tab_stats:
    st.markdown("#### Aylık Verimlilik Projeksiyonu")
    chart_data = pd.DataFrame({
        'Aylar': ['Ocak', 'Şubat', 'Mart', 'Nisan'],
        'Verimlilik Oranı': [72, 78, 85, 94]
    })
    fig = px.area(chart_data, x='Aylar', y='Verimlilik Oranı', title='KODALAN Entegrasyonu Sonrası Verim Artışı')
    st.plotly_chart(fig, use_container_width=True)
