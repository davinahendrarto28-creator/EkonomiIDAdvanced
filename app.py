import streamlit as st
import pandas as pd
import random
import datetime
import math

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="EkonomiID — Portal Ekonomi Indonesia",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: #080c14;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.25rem 2rem 4rem !important; max-width: 1280px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b0f1a 0%, #0d1220 100%) !important;
  border-right: 1px solid #1a2333 !important;
}
[data-testid="stSidebar"] .stRadio label { color: #94a3b8 !important; font-size: .875rem !important; }
[data-testid="stSidebar"] .stRadio label:hover { color: #e2e8f0 !important; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
  background: linear-gradient(135deg, #0f1623 0%, #111e2e 100%) !important;
  border: 1px solid #1a2c3d !important;
  border-radius: 14px !important;
  padding: 1.1rem 1.3rem !important;
  position: relative; overflow: hidden;
  transition: border-color .25s, transform .2s;
}
[data-testid="metric-container"]::before {
  content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at top right, rgba(201,168,76,.06), transparent 60%);
}
[data-testid="metric-container"]:hover { border-color: #c9a84c !important; transform: translateY(-2px); }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: .78rem !important; font-weight: 600 !important; letter-spacing: .04em; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family: 'DM Mono', monospace !important; font-size: 1.35rem !important; font-weight: 500 !important; }
[data-testid="stMetricDelta"] { font-size: .78rem !important; font-weight: 600 !important; }

/* ── Tabs ── */
[data-testid="stTabs"] { border-bottom: 1px solid #1a2333; }
[data-testid="stTabs"] button { color: #64748b !important; font-weight: 500 !important; font-size: .875rem !important; padding: .5rem 1rem !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #c9a84c !important; border-bottom: 2px solid #c9a84c !important; }
[data-testid="stTabs"] button:hover { color: #e2e8f0 !important; background: rgba(255,255,255,.03) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
  background: #0f1623 !important;
  border: 1px solid #1a2333 !important;
  border-left: 3px solid #c9a84c !important;
  border-radius: 0 10px 10px 0 !important;
  margin-bottom: .6rem !important;
}
[data-testid="stExpander"] summary { color: #e8c97a !important; font-weight: 600 !important; font-size: .9rem !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] select,
div[data-testid="stSelectbox"] > div > div {
  background: #0f1623 !important;
  border: 1px solid #1a2333 !important;
  color: #e2e8f0 !important;
  border-radius: 8px !important;
}
[data-testid="stTextInput"] input:focus { border-color: #c9a84c !important; box-shadow: 0 0 0 2px rgba(201,168,76,.15) !important; }
.stSlider > div > div > div > div { background: #c9a84c !important; }
.stSlider [data-testid="stSliderThumb"] { background: #c9a84c !important; border: 2px solid #0f1623 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] iframe { border-radius: 10px !important; }

/* ── Alerts ── */
.stInfo { background: rgba(45,212,191,.07) !important; border-left: 3px solid #2dd4bf !important; color: #94a3b8 !important; border-radius: 8px !important; }
.stSuccess { background: rgba(74,222,128,.07) !important; border-left: 3px solid #4ade80 !important; color: #94a3b8 !important; border-radius: 8px !important; }
.stWarning { background: rgba(251,191,36,.07) !important; border-left: 3px solid #fbbf24 !important; color: #94a3b8 !important; border-radius: 8px !important; }

/* ── Chart containers ── */
[data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"],
iframe { border-radius: 10px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #1a2c3d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c9a84c; }

/* ── hr ── */
hr { border-color: #1a2333 !important; margin: 1.5rem 0 !important; }

/* ── Section header helper ── */
.sec-head { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: .25rem; }
.sec-sub  { color: #64748b; font-size: .875rem; margin-bottom: 1.25rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA ENGINE
# ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def gen_gdp():
    tahun = list(range(2010, 2026))
    nilai = [755.1,788.7,850.4,912.5,888.5,931.9,1015.4,1042.2,1119.2,1058.4,1186.5,1319.1,1371.2,1475.6,1580.3,1652.8]
    growth = [None] + [round((nilai[i]/nilai[i-1]-1)*100,2) for i in range(1,len(nilai))]
    return pd.DataFrame({"Tahun":tahun,"PDB (Triliun Rp)":nilai,"Pertumbuhan (%)":growth})

@st.cache_data(ttl=300)
def gen_inflasi_bulanan():
    bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
    data = {
        2022:[2.18,2.06,2.64,3.47,3.55,4.35,4.94,4.69,5.95,5.71,5.42,5.51],
        2023:[5.28,5.47,4.97,4.33,4.00,3.52,3.08,3.27,2.28,2.56,2.86,2.61],
        2024:[2.57,2.75,3.05,3.00,2.84,2.51,2.13,2.12,1.84,1.71,1.55,1.57],
        2025:[2.48,2.65,2.72,2.58,2.60,2.55,None,None,None,None,None,None],
    }
    rows = []
    for thn, vals in data.items():
        for i, v in enumerate(vals):
            if v is not None:
                rows.append({"Periode": f"{bulan[i]} {thn}", "Tahun": thn, "Bulan": bulan[i], "Inflasi (%)": v})
    return pd.DataFrame(rows)

@st.cache_data(ttl=300)
def gen_kurs(days=90):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days-1,-1,-1)]
    random.seed(7)
    base = 15900
    values, v = [], base
    for i in range(days):
        v += random.gauss(0, 80) + math.sin(i/10)*30
        v = max(14800, min(16800, v))
        values.append(round(v,0))
    return pd.DataFrame({"Tanggal": dates, "USD/IDR": values})

@st.cache_data(ttl=300)
def gen_ekspor_impor():
    bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
    random.seed(3)
    ekspor = [round(random.uniform(17,22) + math.sin(i/2)*1.5, 2) for i in range(12)]
    impor  = [round(random.uniform(14,19) + math.cos(i/2)*1.2, 2) for i in range(12)]
    neraca = [round(e-m,2) for e,m in zip(ekspor,impor)]
    return pd.DataFrame({"Bulan":bulan,"Ekspor (USD M)":ekspor,"Impor (USD M)":impor,"Neraca (USD M)":neraca})

@st.cache_data(ttl=300)
def gen_sektoral():
    sektor = ["Pertanian","Pertambangan","Manufaktur","Konstruksi","Perdagangan",
              "Transportasi","Keuangan","Informasi","Jasa Lain"]
    kontribusi = [13.1, 10.8, 19.6, 9.4, 13.2, 5.7, 4.9, 4.3, 19.0]
    growth = [3.1, 5.8, 4.2, 6.7, 5.9, 8.4, 7.1, 12.3, 4.5]
    return pd.DataFrame({"Sektor":sektor,"Kontribusi PDB (%)":kontribusi,"Pertumbuhan (%)":growth})

@st.cache_data(ttl=300)
def gen_ihsg(days=180):
    random.seed(11)
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days-1,-1,-1)]
    v, vals = 7200.0, []
    for i in range(days):
        v += random.gauss(8, 55) + math.sin(i/15)*20
        v = max(6200, min(8200, v))
        vals.append(round(v,2))
    return pd.DataFrame({"Tanggal":dates,"IHSG":vals})

@st.cache_data(ttl=300)
def gen_investasi():
    kuartal = [f"Q{q} {y}" for y in range(2021,2026) for q in range(1,5)][:16]
    random.seed(5)
    fdi  = [round(random.uniform(120,210)+i*3,1) for i in range(16)]
    pmdn = [round(random.uniform(90,170)+i*2.5,1) for i in range(16)]
    return pd.DataFrame({"Kuartal":kuartal,"FDI (Triliun Rp)":fdi,"PMDN (Triliun Rp)":pmdn})

@st.cache_data(ttl=300)
def gen_pengangguran():
    tahun = list(range(2015,2026))
    tpr = [6.18,5.61,5.50,5.34,5.28,7.07,6.49,5.86,5.45,5.32,5.30]
    return pd.DataFrame({"Tahun":tahun,"TPT (%)":tpr})

# ─────────────────────────────────────────────────────────────
# STATIC DATA
# ─────────────────────────────────────────────────────────────

INDIKATOR = [
    {"nama":"PDB 2025","nilai":"Rp 22.143 T","delta":"+5,11%","positif":True,"icon":"🏛️","sub":"Pertumbuhan YoY"},
    {"nama":"Inflasi Mei 2026","nilai":"2,60%","delta":"-0,02%","positif":True,"icon":"📊","sub":"IHK YoY"},
    {"nama":"USD/IDR","nilai":"15.620","delta":"+0,3%","positif":False,"icon":"💵","sub":"Kurs tengah BI"},
    {"nama":"Cadangan Devisa","nilai":"$145,4 M","delta":"+1,2%","positif":True,"icon":"🏅","sub":"Per Apr 2026"},
    {"nama":"TPT","nilai":"5,32%","delta":"-0,08%","positif":True,"icon":"👥","sub":"Tingkat Pengangguran"},
    {"nama":"BI Rate","nilai":"6,25%","delta":"Stabil","positif":True,"icon":"⚖️","sub":"Apr 2026"},
    {"nama":"IHSG","nilai":"7.843","delta":"+1,2%","positif":True,"icon":"📈","sub":"Penutupan terakhir"},
    {"nama":"Ekspor Apr 2026","nilai":"$19,2 M","delta":"+12%","positif":True,"icon":"🚢","sub":"YoY Nonmigas"},
]

BERITA = [
    {"judul":"BI Tahan Suku Bunga 6,25%","kat":"Moneter","tgl":"26 Mei 2026","icon":"🏦",
     "isi":"Rapat Dewan Gubernur BI memutuskan mempertahankan BI Rate pada 6,25% guna menjaga stabilitas nilai tukar rupiah dan mengendalikan inflasi di tengah tekanan global.",
     "dampak":"Kredit perbankan diperkirakan tetap ketat. Saham sektor keuangan berpotensi tertekan jangka pendek.","sentiment":"netral"},
    {"judul":"PDB Q1 2026 Tumbuh 5,11%","kat":"Makro","tgl":"25 Mei 2026","icon":"📈",
     "isi":"BPS mencatat pertumbuhan ekonomi 5,11% YoY pada Q1 2026, melampaui ekspektasi konsensus 4,9%. Konsumsi RT dan investasi menjadi motor utama.",
     "dampak":"Sinyal positif bagi investor. Rupiah berpotensi menguat dan IHSG diproyeksi bullish jangka menengah.","sentiment":"positif"},
    {"judul":"Ekspor Nonmigas Melonjak 12%","kat":"Perdagangan","tgl":"24 Mei 2026","icon":"🚢",
     "isi":"Ekspor nonmigas April 2026 mencapai USD 18,9 miliar, naik 12% YoY. CPO, batu bara, dan produk manufaktur menjadi komoditas unggulan.",
     "dampak":"Surplus neraca dagang makin solid. Cadangan devisa diproyeksikan terus meningkat.","sentiment":"positif"},
    {"judul":"FDI Q1 2026 Capai Rp 186,9 T","kat":"Investasi","tgl":"23 Mei 2026","icon":"💼",
     "isi":"BKPM melaporkan realisasi FDI Rp 186,9 triliun pada Q1 2026, naik 8,5% YoY. Manufaktur EV dan energi terbarukan mendominasi.",
     "dampak":"Penciptaan lapangan kerja diproyeksikan naik. Nilai tukar rupiah mendapat dukungan struktural.","sentiment":"positif"},
    {"judul":"Inflasi Pangan Terkendali di 2,3%","kat":"Pangan","tgl":"22 Mei 2026","icon":"🌾",
     "isi":"Intervensi Bulog menstabilkan harga beras di bawah HET. Inflasi pangan YoY terjaga di 2,3%, jauh di bawah rata-rata 2022–2023.",
     "dampak":"Daya beli masyarakat terjaga. BI berpeluang mempertahankan atau memangkas suku bunga H2 2026.","sentiment":"positif"},
    {"judul":"Rupiah Menguat ke Rp15.600","kat":"Kurs","tgl":"21 Mei 2026","icon":"💱",
     "isi":"Rupiah menguat ke Rp15.600/USD didorong arus masuk modal asing senilai Rp 4,2 triliun dan data PDB yang kuat.",
     "dampak":"Impor bahan baku lebih murah. Eksportir perlu hedging lebih aktif untuk lindungi margin.","sentiment":"positif"},
    {"judul":"IHSG Tembus 7.800 untuk Pertama Kali","kat":"Pasar Modal","tgl":"20 Mei 2026","icon":"📊",
     "isi":"IHSG ditutup di level 7.843 pada perdagangan Selasa, menembus all-time high baru didorong sektor perbankan dan konsumer.",
     "dampak":"Kapitalisasi pasar BEI naik ke Rp 12.100 triliun. Sentimen investor domestik sangat positif.","sentiment":"positif"},
    {"judul":"Utang Pemerintah Capai Rp 8.756 T","kat":"Fiskal","tgl":"19 Mei 2026","icon":"📋",
     "isi":"Kemenkeu mencatat total utang pemerintah per April 2026 sebesar Rp 8.756 triliun atau 37,8% terhadap PDB, masih di bawah batas aman 60%.",
     "dampak":"Ruang fiskal masih memadai untuk stimulus. Yield SBN diperkirakan stabil.","sentiment":"netral"},
]

KAMUS = [
    ("PDB (Produk Domestik Bruto)","Nilai total semua barang dan jasa yang diproduksi di dalam suatu negara selama periode tertentu. Indikator utama ukuran dan kesehatan ekonomi suatu negara.","Makro"),
    ("Inflasi","Kenaikan harga barang dan jasa secara umum dan berkelanjutan. Diukur dengan IHK (Indeks Harga Konsumen). Target inflasi BI: 1,5–3,5%.","Moneter"),
    ("Deflasi","Penurunan harga barang dan jasa secara umum. Dapat memicu spiral deflasi yang berbahaya bagi perekonomian karena konsumen dan produsen menunda aktivitas ekonomi.","Moneter"),
    ("BI Rate (Suku Bunga Acuan)","Tingkat bunga kebijakan Bank Indonesia. Dinaikkan untuk meredam inflasi/menguatkan rupiah; diturunkan untuk mendorong pertumbuhan ekonomi.","Moneter"),
    ("Neraca Perdagangan","Selisih nilai ekspor vs impor. Surplus = ekspor > impor (baik). Defisit = impor > ekspor. Komponen penting neraca pembayaran.","Perdagangan"),
    ("Cadangan Devisa","Aset luar negeri milik Bank Indonesia berupa valuta asing, emas, dan SDR (IMF). Berfungsi sebagai bantalan eksternal dan penjaga stabilitas kurs.","Moneter"),
    ("FDI (Foreign Direct Investment)","Investasi langsung dari entitas asing berupa pendirian usaha, akuisisi, atau ekspansi pabrik. Berbeda dengan investasi portofolio yang lebih mudah keluar-masuk.","Investasi"),
    ("Kebijakan Fiskal","Penggunaan belanja pemerintah (APBN) dan perpajakan untuk mempengaruhi ekonomi. Ekspansif = defisit, kontraktif = surplus anggaran.","Fiskal"),
    ("Kebijakan Moneter","Pengaturan jumlah uang beredar dan suku bunga oleh bank sentral. Konvensional (suku bunga) dan non-konvensional (QE, forward guidance).","Moneter"),
    ("IHSG (Indeks Harga Saham Gabungan)","Indeks kapitalisasi-tertimbang semua saham di BEI. Cerminan kinerja pasar modal dan sentimen investor terhadap ekonomi Indonesia.","Pasar Modal"),
    ("Yield Obligasi","Imbal hasil efektif obligasi berdasarkan harga pasar. Naik jika harga turun (inverse). Yield SBN 10 tahun adalah acuan suku bunga jangka panjang.","Pasar Modal"),
    ("Neraca Pembayaran","Catatan sistematis semua transaksi ekonomi antarnegara dalam periode tertentu. Terdiri dari transaksi berjalan, modal & finansial, serta cadangan devisa.","Makro"),
    ("Rasio Utang/PDB","Perbandingan total utang pemerintah terhadap PDB. Indonesia menetapkan batas 60% (UU No.17/2003). Per April 2026: ~37,8%.","Fiskal"),
    ("TPT (Tingkat Pengangguran Terbuka)","Persentase angkatan kerja yang tidak bekerja namun aktif mencari pekerjaan. Berbeda dengan setengah pengangguran yang bekerja di bawah kapasitas.","Ketenagakerjaan"),
    ("Stagflasi","Kondisi berbahaya: inflasi tinggi + pertumbuhan ekonomi rendah + pengangguran tinggi secara bersamaan. Contoh: krisis minyak 1970-an.","Makro"),
    ("Quantitative Easing (QE)","Kebijakan moneter non-konvensional: bank sentral membeli aset finansial untuk menambah likuiditas saat suku bunga sudah mendekati nol.","Moneter"),
    ("PMI (Purchasing Managers' Index)","Indeks survei kepada manajer pembelian sektor manufaktur/jasa. Di atas 50 = ekspansi; di bawah 50 = kontraksi. Leading indicator ekonomi.","Indikator"),
    ("Current Account Deficit (CAD)","Defisit transaksi berjalan: impor barang, jasa, dan transfer lebih besar dari ekspor. Jika besar dan persisten, dapat menekan nilai tukar.","Makro"),
]

PROYEKSI = {
    "PDB (%)":     {"2026":5.2,"2027":5.4,"2028":5.5,"2029":5.6,"2030":5.8},
    "Inflasi (%)": {"2026":2.7,"2027":2.5,"2028":2.4,"2029":2.3,"2030":2.2},
    "USD/IDR":     {"2026":15500,"2027":15200,"2028":14900,"2029":14600,"2030":14300},
    "Pengangguran (%)":{"2026":5.1,"2027":4.9,"2028":4.7,"2029":4.5,"2030":4.3},
}

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def card(icon, judul, nilai, delta="", warna_delta="#4ade80", sub="", border="#1a2c3d"):
    tanda = delta
    return f"""
    <div style='background:linear-gradient(135deg,#0f1623,#111e2e);border:1px solid {border};
                border-radius:14px;padding:1.1rem 1.3rem;transition:border-color .2s;'>
      <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.6rem'>
        <span style='font-size:1.5rem'>{icon}</span>
        {'<span style="font-size:.78rem;font-weight:600;color:'+warna_delta+'">'+tanda+'</span>' if delta else ''}
      </div>
      <div style='font-family:"DM Mono",monospace;font-size:1.35rem;color:#e2e8f0;font-weight:500'>{nilai}</div>
      <div style='font-size:.75rem;color:#64748b;margin-top:.2rem;font-weight:600;letter-spacing:.03em'>{judul}</div>
      {'<div style="font-size:.72rem;color:#475569;margin-top:.15rem">'+sub+'</div>' if sub else ''}
    </div>"""

def badge(text, color="#c9a84c", bg="rgba(201,168,76,.12)", border="rgba(201,168,76,.3)"):
    return f"<span style='background:{bg};color:{color};border:1px solid {border};padding:.2rem .65rem;border-radius:100px;font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.04em'>{text}</span>"

def section_header(title, sub=""):
    sub_html = f"<div class='sec-sub'>{sub}</div>" if sub else ""
    st.markdown(f"<div class='sec-head'>{title}</div>{sub_html}", unsafe_allow_html=True)

SENT_COLOR = {"positif":"#4ade80","netral":"#e8c97a","negatif":"#f87171"}
SENT_BG    = {"positif":"rgba(74,222,128,.08)","netral":"rgba(232,201,122,.08)","negatif":"rgba(248,113,113,.08)"}

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.5rem 0 2rem'>
      <div style='font-family:"Playfair Display",serif;font-size:2rem;font-weight:900;color:#c9a84c'>
        Ekonomi<span style='color:#2dd4bf'>ID</span></div>
      <div style='color:#334155;font-size:.72rem;margin-top:.3rem;letter-spacing:.08em;text-transform:uppercase'>
        Portal Ekonomi Indonesia
      </div>
    </div>
    """, unsafe_allow_html=True)

    halaman = st.radio("nav", [
        "🏠  Dashboard",
        "📰  Berita & Analisis",
        "📊  Data Makro",
        "📈  Pasar Keuangan",
        "🏭  Sektor Ekonomi",
        "🔭  Proyeksi & Outlook",
        "📚  Kamus Ekonomi",
        "🧮  Kalkulator Ekonomi",
        "ℹ️  Tentang",
    ], label_visibility="collapsed")

    st.markdown("---")
    now = datetime.datetime.now().strftime("%d %b %Y, %H:%M")
    st.markdown(f"<div style='color:#334155;font-size:.72rem;text-align:center'>🕐 {now} WIB</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#334155;font-size:.72rem;margin-top:1rem;line-height:2;padding:0 .25rem'>
    <strong style='color:#475569'>Sumber Data Resmi</strong><br>
    <a href='https://bi.go.id' target='_blank' style='color:#475569;text-decoration:none'>🏦 Bank Indonesia</a><br>
    <a href='https://bps.go.id' target='_blank' style='color:#475569;text-decoration:none'>📋 BPS</a><br>
    <a href='https://kemenkeu.go.id' target='_blank' style='color:#475569;text-decoration:none'>💰 Kemenkeu</a><br>
    <a href='https://idx.co.id' target='_blank' style='color:#475569;text-decoration:none'>📈 IDX / BEI</a>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════

if halaman == "🏠  Dashboard":
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f1a2e 0%,#0a1020 100%);
                border:1px solid #1a2c3d;border-radius:18px;padding:2.5rem 2.5rem 2rem;
                margin-bottom:2rem;position:relative;overflow:hidden'>
      <div style='position:absolute;top:-40px;right:-40px;width:300px;height:300px;
                  background:radial-gradient(circle,rgba(201,168,76,.07),transparent 70%);pointer-events:none'></div>
      <span style='background:rgba(201,168,76,.12);color:#c9a84c;border:1px solid rgba(201,168,76,.3);
                   padding:.25rem .85rem;border-radius:100px;font-size:.72rem;font-weight:600;
                   letter-spacing:.1em;text-transform:uppercase'>🇮🇩 Portal Ekonomi Indonesia</span>
      <h1 style='font-family:"Playfair Display",serif;font-size:2.8rem;font-weight:900;
                 color:#fff;line-height:1.1;margin:.9rem 0 .7rem'>
        Pantau <span style='color:#c9a84c'>Ekonomi</span><br>Indonesia
      </h1>
      <p style='color:#64748b;font-size:1rem;max-width:520px;line-height:1.7'>
        Dashboard komprehensif data makroekonomi, pasar keuangan, dan analisis sektoral Indonesia — real-time & interaktif.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # ── 8 Indikator Utama ──
    section_header("📌 Indikator Ekonomi Utama", "Posisi terkini per Mei 2026")
    cols = st.columns(4)
    for i, ind in enumerate(INDIKATOR):
        warna = "#4ade80" if ind["positif"] else "#f87171"
        with cols[i % 4]:
            st.markdown(card(ind["icon"], ind["nama"], ind["nilai"], ind["delta"], warna, ind["sub"]), unsafe_allow_html=True)
        if i == 3:
            st.markdown("<div style='margin:.5rem 0'></div>", unsafe_allow_html=True)
            cols = st.columns(4)

    st.markdown("<div style='margin:1.5rem 0'></div>", unsafe_allow_html=True)

    # ── Row: PDB + Inflasi ──
    c1, c2 = st.columns([3,2])
    with c1:
        section_header("🏛️ PDB Indonesia 2010–2025", "Triliun Rupiah, harga berlaku")
        df = gen_gdp()
        st.bar_chart(df.set_index("Tahun")[["PDB (Triliun Rp)"]], color="#c9a84c", height=260)
    with c2:
        section_header("📊 Inflasi YoY 2024", "Bulanan, IHK (%)")
        inf = gen_inflasi_bulanan()
        df24 = inf[inf["Tahun"]==2024].set_index("Bulan")[["Inflasi (%)"]]
        st.area_chart(df24, color="#e8c97a", height=260)

    st.markdown("---")

    # ── Row: IHSG + Kurs ──
    c1, c2 = st.columns(2)
    with c1:
        section_header("📈 IHSG — 180 Hari Terakhir")
        ihsg = gen_ihsg()
        st.line_chart(ihsg.set_index("Tanggal"), color="#4ade80", height=220)
    with c2:
        section_header("💵 USD/IDR — 90 Hari Terakhir")
        kurs = gen_kurs()
        st.line_chart(kurs.set_index("Tanggal"), color="#2dd4bf", height=220)

    st.markdown("---")

    # ── Berita Kilat ──
    section_header("⚡ Berita Kilat")
    b_cols = st.columns(4)
    for i, b in enumerate(BERITA[:4]):
        sc = SENT_COLOR[b["sentiment"]]
        sb = SENT_BG[b["sentiment"]]
        with b_cols[i]:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#0f1623,#111e2e);border:1px solid #1a2333;
                        border-radius:12px;padding:1.1rem;height:180px;overflow:hidden'>
              <div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.6rem;flex-wrap:wrap'>
                <span style='font-size:1.25rem'>{b['icon']}</span>
                <span style='background:{sb};color:{sc};border:1px solid {sc}33;padding:.15rem .5rem;
                             border-radius:100px;font-size:.68rem;font-weight:600;text-transform:uppercase'>{b['kat']}</span>
              </div>
              <div style='color:#e2e8f0;font-size:.87rem;font-weight:600;line-height:1.4;margin-bottom:.5rem'>{b['judul']}</div>
              <div style='color:#64748b;font-size:.76rem;line-height:1.5'>{b['isi'][:90]}…</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: BERITA & ANALISIS
# ══════════════════════════════════════════════════════════════

elif halaman == "📰  Berita & Analisis":
    section_header("📰 Berita & Analisis Ekonomi", "Berita terkini dengan dampak dan analisis pasar")

    # Filter bar
    fc1, fc2 = st.columns([2,1])
    with fc1:
        cari = st.text_input("🔍 Cari berita...", placeholder="Contoh: inflasi, BI Rate, rupiah...")
    with fc2:
        semua_kat = ["Semua"] + sorted({b["kat"] for b in BERITA})
        kat_filter = st.selectbox("Kategori", semua_kat)

    filtered = BERITA
    if cari:
        filtered = [b for b in filtered if cari.lower() in b["judul"].lower() or cari.lower() in b["isi"].lower()]
    if kat_filter != "Semua":
        filtered = [b for b in filtered if b["kat"] == kat_filter]

    st.markdown(f"<div style='color:#475569;font-size:.8rem;margin-bottom:1rem'>Menampilkan {len(filtered)} artikel</div>", unsafe_allow_html=True)

    for b in filtered:
        sc = SENT_COLOR[b["sentiment"]]
        sb = SENT_BG[b["sentiment"]]
        sent_label = {"positif":"🟢 Positif","netral":"🟡 Netral","negatif":"🔴 Negatif"}[b["sentiment"]]
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0f1623,#111e2e);border:1px solid #1a2333;
                    border-radius:14px;padding:1.5rem;margin-bottom:1rem'>
          <div style='display:flex;align-items:center;gap:.6rem;margin-bottom:.75rem;flex-wrap:wrap'>
            <span style='font-size:1.5rem'>{b['icon']}</span>
            {badge(b['kat'])}
            <span style='color:#475569;font-size:.78rem'>{b['tgl']}</span>
            <span style='background:{sb};color:{sc};border:1px solid {sc}33;padding:.15rem .55rem;
                         border-radius:100px;font-size:.7rem;font-weight:600'>{sent_label}</span>
          </div>
          <div style='font-size:1.05rem;font-weight:700;color:#e2e8f0;margin-bottom:.6rem;line-height:1.4'>{b['judul']}</div>
          <div style='font-size:.875rem;color:#94a3b8;line-height:1.75;margin-bottom:.75rem'>{b['isi']}</div>
          <div style='background:rgba(45,212,191,.06);border:1px solid rgba(45,212,191,.15);
                      border-radius:8px;padding:.75rem 1rem'>
            <div style='font-size:.72rem;font-weight:600;color:#2dd4bf;text-transform:uppercase;
                        letter-spacing:.06em;margin-bottom:.3rem'>💡 Analisis Dampak</div>
            <div style='font-size:.83rem;color:#94a3b8;line-height:1.65'>{b['dampak']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.warning("⚠️ Seluruh konten bersifat ilustratif untuk keperluan edukasi.")

# ══════════════════════════════════════════════════════════════
# PAGE: DATA MAKRO
# ══════════════════════════════════════════════════════════════

elif halaman == "📊  Data Makro":
    section_header("📊 Data Ekonomi Makro Indonesia", "Visualisasi komprehensif indikator makroekonomi")

    tab_gdp, tab_inf, tab_ner, tab_inv, tab_tpk = st.tabs([
        "🏛️ PDB & Pertumbuhan", "📊 Inflasi", "🚢 Ekspor-Impor", "💼 Investasi", "👥 Ketenagakerjaan"
    ])

    with tab_gdp:
        df = gen_gdp()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### PDB Nominal (Triliun Rp)")
            st.bar_chart(df.set_index("Tahun")[["PDB (Triliun Rp)"]], color="#c9a84c", height=320)
        with c2:
            st.markdown("#### Laju Pertumbuhan PDB (%)")
            df2 = df.dropna().set_index("Tahun")[["Pertumbuhan (%)"]]
            st.line_chart(df2, color="#4ade80", height=320)
        st.markdown("#### 📋 Data Lengkap PDB")
        st.dataframe(df.dropna().sort_values("Tahun",ascending=False).reset_index(drop=True), use_container_width=True, height=250)

    with tab_inf:
        df_inf = gen_inflasi_bulanan()
        tahun_opsi = sorted(df_inf["Tahun"].unique(), reverse=True)
        sel = st.multiselect("Pilih Tahun", tahun_opsi, default=[2024,2023])
        if sel:
            df_f = df_inf[df_inf["Tahun"].isin(sel)].pivot(index="Bulan",columns="Tahun",values="Inflasi (%)")
            bulan_order = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
            df_f = df_f.reindex([b for b in bulan_order if b in df_f.index])
            st.line_chart(df_f, height=360)
        st.markdown("#### 📋 Data Inflasi Lengkap")
        st.dataframe(df_inf[["Periode","Inflasi (%)"]].sort_values("Periode",ascending=False).reset_index(drop=True), use_container_width=True, height=250)

    with tab_ner:
        df_ne = gen_ekspor_impor()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Ekspor vs Impor 2025 (USD Miliar)")
            st.bar_chart(df_ne.set_index("Bulan")[["Ekspor (USD M)","Impor (USD M)"]], height=320)
        with c2:
            st.markdown("#### Neraca Perdagangan (Surplus/Defisit)")
            st.bar_chart(df_ne.set_index("Bulan")[["Neraca (USD M)"]], color="#2dd4bf", height=320)
        surplus = df_ne["Neraca (USD M)"].sum()
        st.success(f"✅ Total Surplus Neraca Perdagangan 2025: **USD {surplus:.2f} Miliar**")
        st.dataframe(df_ne, use_container_width=True)

    with tab_inv:
        df_inv = gen_investasi()
        st.markdown("#### FDI & PMDN per Kuartal (Triliun Rp)")
        st.bar_chart(df_inv.set_index("Kuartal"), height=360)
        c1,c2 = st.columns(2)
        with c1:
            total_fdi = df_inv["FDI (Triliun Rp)"].sum()
            st.metric("Total FDI (2021–Q1 2026)", f"Rp {total_fdi:,.1f} T")
        with c2:
            total_pmdn = df_inv["PMDN (Triliun Rp)"].sum()
            st.metric("Total PMDN (2021–Q1 2026)", f"Rp {total_pmdn:,.1f} T")

    with tab_tpk:
        df_tpk = gen_pengangguran()
        c1, c2 = st.columns([2,1])
        with c1:
            st.markdown("#### Tingkat Pengangguran Terbuka (%) 2015–2025")
            st.line_chart(df_tpk.set_index("Tahun"), color="#f87171", height=320)
        with c2:
            st.markdown("#### Statistik TPT")
            st.metric("TPT Terendah", f"{df_tpk['TPT (%)'].min():.2f}%", "2019")
            st.metric("TPT Tertinggi (COVID)", f"{df_tpk[df_tpk['Tahun']==2020]['TPT (%)'].values[0]:.2f}%", "2020")
            st.metric("TPT Terkini (2025)", f"{df_tpk[df_tpk['Tahun']==2025]['TPT (%)'].values[0]:.2f}%", "-0,02%")

# ══════════════════════════════════════════════════════════════
# PAGE: PASAR KEUANGAN
# ══════════════════════════════════════════════════════════════

elif halaman == "📈  Pasar Keuangan":
    section_header("📈 Pasar Keuangan Indonesia", "IHSG, Nilai Tukar, dan Pasar Obligasi")

    tab_ihsg, tab_kurs, tab_obl = st.tabs(["📈 IHSG","💵 Nilai Tukar","🏛️ Obligasi Negara"])

    with tab_ihsg:
        ihsg = gen_ihsg()
        periode = st.select_slider("Periode", options=[30,60,90,180], value=90, format_func=lambda x: f"{x} hari")
        df_p = ihsg.tail(periode)
        st.markdown(f"#### IHSG — {periode} Hari Terakhir")

        # Stats row
        cs = st.columns(4)
        val_now = df_p["IHSG"].iloc[-1]
        val_old = df_p["IHSG"].iloc[0]
        chg = val_now - val_old
        pct = (chg / val_old) * 100
        cs[0].metric("Terakhir", f"{val_now:,.0f}", f"{chg:+.0f}")
        cs[1].metric("Tertinggi", f"{df_p['IHSG'].max():,.0f}")
        cs[2].metric("Terendah",  f"{df_p['IHSG'].min():,.0f}")
        cs[3].metric(f"Return {periode}h", f"{pct:+.2f}%")

        st.line_chart(df_p.set_index("Tanggal")[["IHSG"]], color="#4ade80", height=380)

    with tab_kurs:
        kurs_df = gen_kurs(90)
        pasangan = st.selectbox("Pasangan Mata Uang", ["USD/IDR","EUR/IDR (Simulasi)","JPY/IDR (Simulasi)","SGD/IDR (Simulasi)"])
        multiplier = {"USD/IDR":1.0,"EUR/IDR (Simulasi)":1.08,"JPY/IDR (Simulasi)":0.0066,"SGD/IDR (Simulasi)":0.74}
        m = multiplier[pasangan]
        kurs_show = kurs_df.copy()
        kurs_show["Nilai"] = (kurs_show["USD/IDR"] * m).round(2)
        kurs_show = kurs_show.rename(columns={"Nilai":pasangan})

        cs = st.columns(4)
        now_v = kurs_show[pasangan].iloc[-1]
        old_v = kurs_show[pasangan].iloc[0]
        cs[0].metric("Kurs Terkini", f"{now_v:,.0f}")
        cs[1].metric("Tertinggi 90h", f"{kurs_show[pasangan].max():,.0f}")
        cs[2].metric("Terendah 90h", f"{kurs_show[pasangan].min():,.0f}")
        cs[3].metric("Volatilitas", f"{kurs_show[pasangan].std():.0f}")

        st.line_chart(kurs_show.set_index("Tanggal")[[pasangan]], color="#2dd4bf", height=380)
        st.info("📌 Data simulasi berbasis kurs USD/IDR sebagai acuan.")

    with tab_obl:
        tenor = [1,2,3,5,7,10,15,20,30]
        random.seed(9)
        yield_sbn = [5.1,5.4,5.7,6.0,6.3,6.6,6.85,7.0,7.2]
        df_obl = pd.DataFrame({"Tenor (Tahun)":tenor,"Yield SBN (%)":yield_sbn}).set_index("Tenor (Tahun)")
        st.markdown("#### Yield Curve SBN Indonesia (Simulasi Mei 2026)")
        st.area_chart(df_obl, color="#c9a84c", height=360)

        cs = st.columns(3)
        cs[0].metric("Yield 10Y",  "6,60%", "+0,05%")
        cs[1].metric("Yield 2Y",   "5,40%", "-0,03%")
        cs[2].metric("Spread 10Y-2Y","1,20%","Steepening")
        st.info("📌 Yield curve normal (upward sloping) mengindikasikan ekspektasi pertumbuhan positif.")

# ══════════════════════════════════════════════════════════════
# PAGE: SEKTOR EKONOMI
# ══════════════════════════════════════════════════════════════

elif halaman == "🏭  Sektor Ekonomi":
    section_header("🏭 Analisis Sektoral Ekonomi Indonesia", "Kontribusi dan pertumbuhan per sektor PDB")

    df_sek = gen_sektoral()

    c1, c2 = st.columns([3,2])
    with c1:
        st.markdown("#### Kontribusi Sektor terhadap PDB (%)")
        st.bar_chart(df_sek.set_index("Sektor")[["Kontribusi PDB (%)"]], color="#c9a84c", height=380)
    with c2:
        st.markdown("#### Pertumbuhan per Sektor (% YoY)")
        st.bar_chart(df_sek.set_index("Sektor")[["Pertumbuhan (%)"]], color="#4ade80", height=380)

    st.markdown("---")
    st.markdown("#### 📋 Tabel Lengkap Kinerja Sektoral")
    df_disp = df_sek.copy()
    df_disp["Kontribusi PDB (%)"] = df_disp["Kontribusi PDB (%)"].apply(lambda x: f"{x:.1f}%")
    df_disp["Pertumbuhan (%)"] = df_disp["Pertumbuhan (%)"].apply(lambda x: f"▲ {x:.1f}%")
    st.dataframe(df_disp.set_index("Sektor"), use_container_width=True)

    st.markdown("---")
    # Sektor spotlight
    section_header("🔦 Spotlight Sektor", "Pilih sektor untuk melihat tren historis simulasi")
    sel_sek = st.selectbox("Pilih Sektor", df_sek["Sektor"].tolist())
    base_g = float(df_sek[df_sek["Sektor"]==sel_sek]["Pertumbuhan (%)"].values[0])
    random.seed(hash(sel_sek) % 100)
    qtrs = [f"Q{q} {y}" for y in range(2022,2026) for q in range(1,5)]
    growth_hist = [round(base_g + random.uniform(-2,2),2) for _ in qtrs]
    df_spot = pd.DataFrame({"Kuartal":qtrs, "Pertumbuhan (%)":growth_hist}).set_index("Kuartal")
    st.line_chart(df_spot, color="#2dd4bf", height=280)
    avg = sum(growth_hist)/len(growth_hist)
    st.info(f"📊 Rata-rata pertumbuhan **{sel_sek}** (2022–2025): **{avg:.2f}% per kuartal**")

# ══════════════════════════════════════════════════════════════
# PAGE: PROYEKSI & OUTLOOK
# ══════════════════════════════════════════════════════════════

elif halaman == "🔭  Proyeksi & Outlook":
    section_header("🔭 Proyeksi & Outlook Ekonomi 2026–2030", "Berdasarkan skenario baseline konsensus analis")

    st.markdown("""
    <div style='background:rgba(201,168,76,.05);border:1px solid rgba(201,168,76,.2);
                border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.5rem'>
      <span style='color:#c9a84c;font-weight:600;font-size:.85rem'>⚠️ Disclaimer Proyeksi</span>
      <span style='color:#64748b;font-size:.82rem;margin-left:.5rem'>
        Proyeksi bersifat ilustratif berdasarkan simulasi. Bukan rekomendasi investasi.
      </span>
    </div>
    """, unsafe_allow_html=True)

    indikator_list = list(PROYEKSI.keys())
    tab_list = st.tabs([f"📌 {k}" for k in indikator_list])

    for ti, (ind, tab) in enumerate(zip(indikator_list, tab_list)):
        with tab:
            data = PROYEKSI[ind]
            df_p = pd.DataFrame({"Tahun": list(data.keys()), ind: list(data.values())}).set_index("Tahun")
            c1, c2 = st.columns([2,1])
            with c1:
                st.markdown(f"#### Proyeksi {ind} 2026–2030")
                st.line_chart(df_p, color="#c9a84c", height=300)
            with c2:
                st.markdown("#### Ringkasan")
                vals = list(data.values())
                st.metric("2026", f"{vals[0]:,}")
                st.metric("2028", f"{vals[2]:,}")
                st.metric("2030", f"{vals[4]:,}")
                total_delta = ((vals[4] - vals[0]) / vals[0]) * 100
                st.metric(f"Perubahan 5 Tahun", f"{total_delta:+.1f}%")

    st.markdown("---")
    section_header("🌍 Perbandingan Regional", "Proyeksi pertumbuhan PDB 2026 (IMF, simulasi)")
    negara = ["Indonesia","Vietnam","Filipina","Malaysia","Thailand","Singapura","India","China"]
    gdp_proj = [5.2, 6.1, 5.8, 4.4, 3.1, 2.4, 6.5, 4.8]
    df_reg = pd.DataFrame({"Negara":negara,"Proyeksi PDB 2026 (%)":gdp_proj}).set_index("Negara")
    st.bar_chart(df_reg, color="#2dd4bf", height=320)
    st.info("🇮🇩 Indonesia diproyeksikan tumbuh 5,2% — di atas rata-rata ASEAN (4,3%).")

# ══════════════════════════════════════════════════════════════
# PAGE: KAMUS
# ══════════════════════════════════════════════════════════════

elif halaman == "📚  Kamus Ekonomi":
    section_header("📚 Kamus Istilah Ekonomi", f"{len(KAMUS)} istilah penting dengan konteks dan kategori")

    c1, c2 = st.columns([3,1])
    with c1:
        cari = st.text_input("🔍 Cari istilah...", placeholder="Contoh: inflasi, yield, FDI...")
    with c2:
        kat_list = ["Semua"] + sorted({k[2] for k in KAMUS})
        kat_f = st.selectbox("Kategori", kat_list)

    hasil = KAMUS
    if cari:
        hasil = [k for k in hasil if cari.lower() in k[0].lower() or cari.lower() in k[1].lower()]
    if kat_f != "Semua":
        hasil = [k for k in hasil if k[2] == kat_f]

    kat_colors = {
        "Makro":"#4ade80","Moneter":"#c9a84c","Fiskal":"#f87171","Perdagangan":"#2dd4bf",
        "Investasi":"#a78bfa","Pasar Modal":"#fb923c","Ketenagakerjaan":"#38bdf8","Indikator":"#94a3b8"
    }

    st.markdown(f"<div style='color:#475569;font-size:.8rem;margin-bottom:1rem'>Menampilkan {len(hasil)} dari {len(KAMUS)} istilah</div>", unsafe_allow_html=True)

    for ist, dfn, kat in hasil:
        kc = kat_colors.get(kat,"#64748b")
        with st.expander(f"📖  {ist}"):
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.75rem'>
              <span style='background:{kc}22;color:{kc};border:1px solid {kc}44;
                           padding:.15rem .6rem;border-radius:100px;font-size:.7rem;font-weight:600'>{kat}</span>
            </div>
            <p style='color:#94a3b8;line-height:1.8;font-size:.9rem'>{dfn}</p>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: KALKULATOR EKONOMI
# ══════════════════════════════════════════════════════════════

elif halaman == "🧮  Kalkulator Ekonomi":
    section_header("🧮 Kalkulator Ekonomi", "Alat hitung interaktif untuk analisis ekonomi personal")

    tab_inf, tab_bunga, tab_kurs, tab_pdb = st.tabs([
        "📊 Dampak Inflasi","💰 Bunga Majemuk","💱 Konversi Kurs","📈 Estimasi PDB"
    ])

    with tab_inf:
        st.markdown("#### 📊 Kalkulator Daya Beli — Dampak Inflasi")
        st.markdown("<p style='color:#64748b;font-size:.875rem;margin-bottom:1rem'>Hitung berapa nilai uangmu setelah tergerus inflasi</p>", unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: nilai_awal = st.number_input("Nilai Uang Saat Ini (Rp)", min_value=100_000, max_value=10_000_000_000, value=1_000_000, step=100_000)
        with c2: inflasi_r  = st.slider("Tingkat Inflasi (% per tahun)", 1.0, 15.0, 2.7, 0.1)
        with c3: tahun_n    = st.slider("Jangka Waktu (tahun)", 1, 30, 10)

        nilai_riil = nilai_awal / ((1 + inflasi_r/100) ** tahun_n)
        daya_beli_hilang = nilai_awal - nilai_riil
        pct_hilang = (daya_beli_hilang / nilai_awal) * 100

        r1,r2,r3 = st.columns(3)
        r1.metric("Nilai Awal", f"Rp {nilai_awal:,.0f}")
        r2.metric(f"Nilai Riil Setelah {tahun_n} Tahun", f"Rp {nilai_riil:,.0f}", f"-{pct_hilang:.1f}%")
        r3.metric("Daya Beli Hilang", f"Rp {daya_beli_hilang:,.0f}")

        # Tabel proyeksi tahunan
        rows = []
        for y in range(1, tahun_n+1):
            vr = nilai_awal / ((1+inflasi_r/100)**y)
            rows.append({"Tahun ke-":y, "Nilai Riil (Rp)":f"Rp {vr:,.0f}", "Penurunan (%)":f"-{(1-vr/nilai_awal)*100:.1f}%"})
        st.markdown("##### Proyeksi Tahunan")
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=220)

    with tab_bunga:
        st.markdown("#### 💰 Kalkulator Bunga Majemuk")
        st.markdown("<p style='color:#64748b;font-size:.875rem;margin-bottom:1rem'>Simulasi pertumbuhan investasi dengan bunga majemuk</p>", unsafe_allow_html=True)
        c1,c2,c3,c4 = st.columns(4)
        with c1: modal   = st.number_input("Modal Awal (Rp)", 1_000_000, 10_000_000_000, 10_000_000, 1_000_000)
        with c2: bunga   = st.slider("Bunga / Return (%/tahun)", 1.0, 20.0, 8.0, 0.5)
        with c3: setoran = st.number_input("Setoran Bulanan (Rp)", 0, 100_000_000, 1_000_000, 500_000)
        with c4: tahun_b = st.slider("Lama Investasi (tahun)", 1, 40, 20)

        rows = []
        v = float(modal)
        total_setor = float(modal)
        for y in range(1, tahun_b+1):
            for _ in range(12):
                v = v * (1 + bunga/(100*12)) + setoran
                total_setor += setoran
            rows.append({"Tahun ke-":y,"Total Nilai (Rp)":round(v),"Total Disetorkan (Rp)":round(total_setor),"Keuntungan (Rp)":round(v-total_setor)})

        df_bunga = pd.DataFrame(rows)
        r1,r2,r3 = st.columns(3)
        r1.metric("Nilai Akhir", f"Rp {v:,.0f}")
        r2.metric("Total Disetorkan", f"Rp {total_setor:,.0f}")
        r3.metric("Total Keuntungan", f"Rp {v-total_setor:,.0f}", f"+{(v/total_setor-1)*100:.0f}%")

        st.line_chart(df_bunga.set_index("Tahun ke-")[["Total Nilai (Rp)","Total Disetorkan (Rp)"]], height=280)

    with tab_kurs:
        st.markdown("#### 💱 Konversi Nilai Tukar")
        KURS_REF = {"USD":15620,"EUR":16890,"JPY":103,"SGD":11580,"MYR":3320,"AUD":10150,"GBP":19740,"CNY":2148}
        c1,c2,c3 = st.columns(3)
        with c1: amt   = st.number_input("Jumlah", 1.0, 1e9, 1000.0, 100.0)
        with c2: dari  = st.selectbox("Dari", list(KURS_REF.keys()) + ["IDR"])
        with c3: ke    = st.selectbox("Ke", ["IDR"] + list(KURS_REF.keys()), index=0)

        if dari == "IDR":
            hasil_konv = amt / KURS_REF[ke]
        elif ke == "IDR":
            hasil_konv = amt * KURS_REF[dari]
        else:
            idr = amt * KURS_REF[dari]
            hasil_konv = idr / KURS_REF[ke]

        st.success(f"**{amt:,.2f} {dari}** = **{hasil_konv:,.4f} {ke}**")
        st.markdown("##### Tabel Kurs Referensi (terhadap IDR)")
        df_kurs_ref = pd.DataFrame([{"Mata Uang":k,"Kurs (IDR)":f"Rp {v:,.0f}"} for k,v in KURS_REF.items()])
        st.dataframe(df_kurs_ref.set_index("Mata Uang"), use_container_width=True)
        st.caption("*Kurs ilustratif, bukan kurs real-time")

    with tab_pdb:
        st.markdown("#### 📈 Estimasi Waktu Capai Target PDB")
        c1,c2,c3 = st.columns(3)
        with c1: pdb_sekarang = st.number_input("PDB Saat Ini (Triliun Rp)", 100.0, 100000.0, 22143.0, 100.0)
        with c2: target_pdb   = st.number_input("Target PDB (Triliun Rp)", 100.0, 200000.0, 50000.0, 1000.0)
        with c3: growth_rate  = st.slider("Asumsi Pertumbuhan (% per tahun)", 1.0, 15.0, 5.2, 0.1)

        if target_pdb > pdb_sekarang:
            tahun_butuh = math.log(target_pdb / pdb_sekarang) / math.log(1 + growth_rate/100)
            thn_capai = datetime.date.today().year + math.ceil(tahun_butuh)
            st.success(f"🎯 Dengan pertumbuhan **{growth_rate}%/tahun**, target PDB **Rp {target_pdb:,.0f} T** dapat dicapai dalam **{tahun_butuh:.1f} tahun** (sekitar tahun **{thn_capai}**).")

            rows_pdb = []
            v = pdb_sekarang
            for y in range(1, int(math.ceil(tahun_butuh))+2):
                v *= (1 + growth_rate/100)
                rows_pdb.append({"Tahun ke-":y, "Proyeksi PDB (T Rp)":round(v,1)})
                if v >= target_pdb: break
            st.bar_chart(pd.DataFrame(rows_pdb).set_index("Tahun ke-"), color="#4ade80", height=280)
        else:
            st.warning("Target PDB harus lebih besar dari PDB saat ini.")

# ══════════════════════════════════════════════════════════════
# PAGE: TENTANG
# ══════════════════════════════════════════════════════════════

elif halaman == "ℹ️  Tentang":
    section_header("ℹ️ Tentang EkonomiID")

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f1a2e,#0a1020);border:1px solid #1a2c3d;
                border-radius:16px;padding:2.5rem;margin-bottom:1.5rem'>
      <h3 style='font-family:"Playfair Display",serif;color:#e2e8f0;margin-bottom:.75rem'>Apa itu EkonomiID?</h3>
      <p style='color:#94a3b8;line-height:1.85;font-size:.95rem'>
        <strong style='color:#e2e8f0'>EkonomiID</strong> adalah dashboard ekonomi Indonesia versi advanced yang dirancang
        untuk memberikan pemahaman komprehensif tentang kondisi makroekonomi, pasar keuangan, dan proyeksi ekonomi
        dalam antarmuka yang intuitif dan menarik.
      </p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    fitur = [
        ("🏠","Dashboard Utama","8 indikator ekonomi real-time dengan visualisasi premium."),
        ("📰","Berita & Analisis","Berita terkini lengkap dengan analisis dampak pasar."),
        ("📊","Data Makro","5 tab data: PDB, Inflasi, Ekspor-Impor, Investasi, Ketenagakerjaan."),
        ("📈","Pasar Keuangan","IHSG, multi-kurs, dan yield curve obligasi negara."),
        ("🏭","Sektor Ekonomi","Analisis kontribusi dan pertumbuhan 9 sektor PDB."),
        ("🔭","Proyeksi & Outlook","Proyeksi 5 tahun + perbandingan regional ASEAN."),
        ("📚","Kamus Ekonomi","18 istilah dengan kategori dan pencarian pintar."),
        ("🧮","Kalkulator Ekonomi","4 kalkulator: inflasi, bunga majemuk, kurs, PDB."),
    ]
    for i,(ikon,judul,desk) in enumerate(fitur):
        with (c1 if i%2==0 else c2):
            st.markdown(f"""
            <div style='background:#0f1623;border:1px solid #1a2333;border-radius:12px;
                        padding:1.1rem;margin-bottom:.75rem;display:flex;gap:.9rem;align-items:flex-start'>
              <span style='font-size:1.5rem;flex-shrink:0'>{ikon}</span>
              <div><strong style='color:#e2e8f0;font-size:.9rem'>{judul}</strong>
              <p style='color:#64748b;font-size:.82rem;margin-top:.2rem;line-height:1.5'>{desk}</p></div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(201,168,76,.05);border:1px solid rgba(201,168,76,.2);
                border-radius:12px;padding:1.5rem;margin-top:.5rem'>
      <strong style='color:#c9a84c'>⚠️ Disclaimer</strong>
      <p style='color:#64748b;font-size:.875rem;line-height:1.8;margin-top:.5rem'>
        Seluruh data bersifat <strong style='color:#e2e8f0'>ilustratif</strong> dan dibuat untuk tujuan
        edukasi dan demonstrasi teknis. Bukan rekomendasi investasi atau keputusan finansial.<br><br>
        Untuk data resmi: <strong style='color:#e2e8f0'>bi.go.id · bps.go.id · kemenkeu.go.id · idx.co.id</strong>
      </p>
    </div>
    <div style='text-align:center;padding:1.5rem;color:#334155;font-size:.85rem;margin-top:1rem'>
      Dibangun dengan ❤️ menggunakan <strong style='color:#64748b'>Python + Streamlit</strong>
    </div>
    """, unsafe_allow_html=True)

