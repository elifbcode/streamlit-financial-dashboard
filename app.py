import streamlit as st
import yfinance as yf
from datetime import date, timedelta
# data_analyst.py dosyasındaki fonksiyonları içe aktarıyoruz
from fin_funcs import plot_candlestick, plot_volume, calculate_indicators, plot_rsi 
import pandas as pd

# ----------------------------------------------------
# 1. SAYFA YAPILANDIRMASI (KOYU TEMA VE GENİŞ GÖRÜNÜM)
# ----------------------------------------------------
st.set_page_config(
    page_title="Finansal Dashboard Projesi", 
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("📈 Finansal Analiz Dashboard'u")

# ----------------------------------------------------
# 2. YAN PANEL (SIDEBAR) VE GİRİŞLER
# ----------------------------------------------------

default_ticker = 'MSFT' 

st.sidebar.header("Ayarlar")
# Girilen sembolü büyük harfe çeviriyoruz (yfinance büyük harf bekler)
ticker_symbol = st.sidebar.text_input("Hisse Senedi Sembolü (Örn: MSFT, TSLA, ASELS.IS)", default_ticker).upper()

# Tarih Aralığı Seçimi (Varsayılan olarak 1 yıl)
today = date.today()
default_start_date = today - timedelta(days=365) 
start_date = st.sidebar.date_input("Başlangıç Tarihi", default_start_date)
end_date = st.sidebar.date_input("Bitiş Tarihi", today)

# ----------------------------------------------------
# 3. YARDIMCI VERİ ÇEKME FONKSİYONLARI
# ----------------------------------------------------

# Şirket bilgilerini çekme (Önbellekleme ile sadece 1 gün boyunca hafızada tut)
@st.cache_data(ttl=86400)
def get_ticker_info(ticker):
    """Şirket temel bilgilerini yfinance'tan çeker."""
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        required_keys = ['longName', 'sector', 'industry', 'marketCap']
        # Gerekli bilgileri çekiyoruz, Piyasa Değerini milyar dolar formatına çeviriyoruz
        data = {
            "Şirket Adı": info.get('longName', 'Bilinmiyor'),
            "Sektör": info.get('sector', 'Bilinmiyor'),
            "Endüstri": info.get('industry', 'Bilinmiyor'),
            "Piyasa Değeri": f"{info.get('marketCap', 0) / 1_000_000_000:,.2f}B $"
        }
        return data
    except:
        # Hata olursa boş bilgi döndür
        return None


# @st.cache_data: Aynı veriyi tekrar çekerken internetten değil, hafızadan okur.
@st.cache_data(ttl=3600) # Veriyi 1 saat (3600 saniye) boyunca önbellekte tut
def load_data(ticker, start, end):
    """Geleneksel yf.download yerine yf.Ticker objesi kullanarak veriyi çeker."""
    try:
        # Ticker objesi ile daha güvenilir veri çekme yöntemi
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(start=start, end=end) # YENİ YÖNTEM
        
        if data.empty:
            # Veri bulunamadıysa 'None' döndür
            return None
        
        # !!! GÖSTERGELERİ HESAPLAMA VE DATAFRAME'E EKLEME !!!
        data = calculate_indicators(data) # data_analyst.py'den gelen fonksiyon
        
        return data
        
    except Exception as e:
        # Veri çekme hatasını yakalama (Streamlit arayüzünde gösterilecektir)
        # Bu kısımda hata olduğunda bile None dönsün
        return None

# Veriyi yükle
df = load_data(ticker_symbol, start_date, end_date)
company_info = get_ticker_info(ticker_symbol)

# ----------------------------------------------------
# 4. DASHBOARD GÖSTERİMİ
# ----------------------------------------------------

if df is None or df.empty or company_info is None:
    # Veri çekilemediyse veya bulunamadıysa uyarı göster
    st.error(f"⚠️ Hata: '{ticker_symbol}' sembolü için veri bulunamadı veya çekilemedi. Lütfen sembolü (örneğin: GOOGL, TSLA) kontrol edin veya tarih aralığını kısaltın.")
else:
    
    # 4.0 Şirket Temel Bilgileri
    st.subheader(f"{company_info.get('Şirket Adı', ticker_symbol)} ({ticker_symbol})")
    info_cols = st.columns(4)
    info_cols[0].metric("Sektör", company_info.get('Sektör'))
    info_cols[1].metric("Endüstri", company_info.get('Endüstri'))
    info_cols[2].metric("Piyasa Değeri", company_info.get('Piyasa Değeri'))
    
    st.markdown("---") # Ayırıcı Çizgi
    
    # 4.1. TEMEL BİLGİLER VE METRİKLER (KPI)
    latest_close = df['Close'].iloc[-1]
    previous_close = df['Close'].iloc[-2]
    price_change = latest_close - previous_close
    percent_change = (price_change / previous_close) * 100

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Son Kapanış Fiyatı ($)", value=f"{latest_close:,.2f}")
    
    with col2:
        st.metric(
            label="Günlük Değişim", 
            value=f"{price_change:,.2f}", 
            delta=f"{percent_change:.2f}%"
        )
        
    with col3:
        # Son 20 günlük hacim ortalaması
        st.metric(label="Ortalama İşlem Hacmi (20 Gün)", value=f"{df['Volume'].iloc[-20:].mean():,.0f}")

    st.markdown("---")
    
    # ----------------------------------------------------
    # 5. GRAFİK GÖSTERİMİ (Mum Çubuğu ve SMA)
    # ----------------------------------------------------
    st.subheader('Hisse Senedi Fiyat Grafiği ve Hareketli Ortalamalar')
    fig = plot_candlestick(df, ticker_symbol) 
    st.plotly_chart(fig, use_container_width=True) 

    # ----------------------------------------------------
    # 5.1. RSI GRAFİĞİ 
    # ----------------------------------------------------
    st.subheader('RSI (Göreceli Güç Endeksi)')
    fig_rsi = plot_rsi(df) 
    st.plotly_chart(fig_rsi, use_container_width=True)
    
    # ----------------------------------------------------
    # 5.2. İŞLEM HACMİ GRAFİĞİ
    # ----------------------------------------------------
    st.subheader('Günlük İşlem Hacmi')
    fig_volume = plot_volume(df) 
    st.plotly_chart(fig_volume, use_container_width=True)
    
    # ----------------------------------------------------
    # 6. HAM VERİ TABLOSU
    # ----------------------------------------------------
    st.markdown("---")
    if st.checkbox('Ham Veriyi Göster (Teknik Göstergeler Dahil)'):
        st.subheader('Ham Veri (Son 5 Satır)')
        st.dataframe(df.tail(5), use_container_width=True)
