

import streamlit as st
import sqlite3
import pandas as pd

# --- VERİTABANI BAĞLANTISI (SQL) ---
def tablo_olustur():
    conn = sqlite3.connect('kodalan.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS AtikParcalar 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, malzeme TEXT, en REAL, boy REAL, durum TEXT)''')
    conn.commit()
    conn.close()

def veri_ekle(malzeme, en, boy):
    conn = sqlite3.connect('kodalan.db')
    c = conn.cursor()
    c.execute("INSERT INTO AtikParcalar (malzeme, en, boy, durum) VALUES (?, ?, ?, 'Stokta')", (malzeme, en, boy))
    conn.commit()
    conn.close()

def verileri_getir():
    conn = sqlite3.connect('kodalan.db')
    df = pd.read_sql_query("SELECT * FROM AtikParcalar", conn)
    conn.close()
    return df

# --- ARAYÜZ AYARLARI ---
st.set_page_config(page_title="KODALAN | Akıllı Üretim", layout="wide")
tablo_olustur()

st.title("🌲 KODALAN: Sürdürülebilir Üretim Paneli")
st.subheader("Ryn Door Dijital Atık ve Optimizasyon Yönetimi")

# --- SOL PANEL (VERİ GİRİŞİ) ---
st.sidebar.header("🛠️ Yeni Atık Parça Kaydı")
st.sidebar.info("Kesimden artan kupon parçaları buradan SQL veritabanına ekleyebilirsiniz.")
m_tipi = st.sidebar.selectbox("Malzeme Tipi", ["MDF Panel", "Lake Yüzey", "Ahşap Çıta"])
m_en = st.sidebar.number_input("Parça Eni (cm)", min_value=1.0)
m_boy = st.sidebar.number_input("Parça Boyu (cm)", min_value=1.0)

if st.sidebar.button("SQL Veritabanına Kaydet"):
    veri_ekle(m_tipi, m_en, m_boy)
    st.sidebar.success(f"{m_tipi} başarıyla stoklara eklendi!")

# --- ANA EKRAN (GÖSTERGE PANELİ) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📋 Güncel Atık Stok Listesi (SQL Verileri)")
    df_stok = verileri_getir()
    st.dataframe(df_stok, use_container_width=True)

with col2:
    st.markdown("### 🎯 Optimizasyon Testi")
    st.write("Sistem, SQL'deki verileri kullanarak en uygun kesimi hesaplar.")
    test_en = st.number_input("İhtiyaç Duyulan En (cm)", value=50.0)
    test_boy = st.number_input("İhtiyaç Duyulan Boy (cm)", value=100.0)
    
    if st.button("En Uygun Parçayı Bul"):
        # SQL sorgusu ile uygun parçayı filtreleme
        uygun_parca = df_stok[(df_stok['en'] >= test_en) & (df_stok['boy'] >= test_boy)]
        if not uygun_parca.empty:
            st.success(f"Eşleşme Bulundu! ID: {uygun_parca.iloc[0]['id']} numaralı parça kullanılabilir.")
        else:
            st.error("Stokta uygun parça bulunamadı, ana plakayı kullanmalısınız.")