import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pandas_ta as ta # Teknik göstergeleri hesaplamak için kullanılır


# --- 1. FONKSİYON: Teknik Göstergeleri Hesaplama ---
def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Veri çerçevesine SMA (Hareketli Ortalamalar) ve RSI göstergelerini ekler."""
    
    # Basit Hareketli Ortalamaları (SMA) hesapla
    df.ta.sma(length=20, append=True)
    df.ta.sma(length=50, append=True)
    
    # 14 günlük Göreceli Güç Endeksini (RSI) hesapla
    df.ta.rsi(length=14, append=True)
    
    # Hesaplanan göstergeler DataFrame'e yeni sütunlar olarak eklenir
    return df

# --- 2. FONKSİYON: Mum Çubuğu Grafiği (Fiyat ve SMA'lar) ---
def plot_candlestick(df, ticker_symbol):
    
    sma_20 = 'SMA_20'
    sma_50 = 'SMA_50'

    fig = go.Figure()

    # 1. Mum Çubuğu Grafiği (Açılış, En Yüksek, En Düşük, Kapanış)
    fig.add_trace(go.Candlestick(
        x=df.index, 
        open=df['Open'], 
        high=df['High'], 
        low=df['Low'], 
        close=df['Close'],
        name=f'{ticker_symbol} Fiyat'
    ))
    
    # 2. SMA-20 (Mavi Çizgi)
    if sma_20 in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df[sma_20], 
            mode='lines', 
            name='SMA 20', 
            line=dict(color='blue', width=1)
        ))

    # 3. SMA-50 (Kırmızı Çizgi)
    if sma_50 in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df[sma_50], 
            mode='lines', 
            name='SMA 50', 
            line=dict(color='red', width=1)
        ))
    
    # Grafik düzeni ayarları
    fig.update_layout(
        xaxis_title="Tarih", 
        yaxis_title="Fiyat ($)", 
        height=550, 
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        title=f"{ticker_symbol} Fiyat ve Hareketli Ortalamalar"
    )
    return fig

# --- 3. FONKSİYON: RSI Grafiği ---
def plot_rsi(df):
    
    rsi_col = 'RSI_14' 
    
    # RSI hesaplanmamışsa boş figür döndür
    if rsi_col not in df.columns:
        return go.Figure() 
        
    fig_rsi = go.Figure()

    # RSI Çizgisi
    fig_rsi.add_trace(go.Scatter(
        x=df.index, 
        y=df[rsi_col], 
        mode='lines', 
        name='RSI',
        line=dict(color='purple')
    ))
    
    # Aşırı Alım (Overbought) ve Aşırı Satım (Oversold) çizgileri
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Aşırı Alım (70)")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Aşırı Satım (30)")
    
    # Y ekseni aralığını 0-100 arasında sabitle
    fig_rsi.update_yaxes(range=[0, 100])
    
    fig_rsi.update_layout(
        xaxis_title="Tarih", 
        yaxis_title="RSI Değeri", 
        height=300, 
        title="Göreceli Güç Endeksi (RSI)"
    )
    return fig_rsi

# --- 4. FONKSİYON: Hacim Grafiği ---
def plot_volume(df):
    
    fig_volume = go.Figure()

    fig_volume.add_trace(go.Bar(
        x=df.index, 
        y=df['Volume'], 
        name='Hacim',
        marker_color='rgba(150, 150, 150, 0.5)' # Yarı saydam gri
    ))
    
    fig_volume.update_layout(
        xaxis_title="Tarih", 
        yaxis_title="Hacim", 
        height=300, 
        title="Günlük Hacim Dağılımı"
    )
    return fig_volume
