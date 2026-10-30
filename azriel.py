import base64
from html import escape
from pathlib import Path
 
import streamlit as st
 
# ---------------------------------------------------------------
# Konfigurasi halaman
# ---------------------------------------------------------------
st.set_page_config(page_title="Profil Saya", page_icon="🏔️", layout="centered")
 
# Simpan foto Anda dengan nama foto.jpg di folder yang sama dengan file ini
GAMBAR_DEFAULT = "foto.jpg"
 
# ---------------------------------------------------------------
# Background gunung (SVG dibuat langsung, jadi tidak perlu internet)
# ---------------------------------------------------------------
MOUNTAIN_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1e3c72"/>
      <stop offset="0.55" stop-color="#4a7fb5"/>
      <stop offset="1" stop-color="#f6c28b"/>
    </linearGradient>
    <linearGradient id="far" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7a8fb8"/>
      <stop offset="1" stop-color="#a9b8d6"/>
    </linearGradient>
    <linearGradient id="mid" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4b5f8f"/>
      <stop offset="1" stop-color="#6d80ad"/>
    </linearGradient>
    <linearGradient id="near" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1f3b4d"/>
      <stop offset="1" stop-color="#2f5d62"/>
    </linearGradient>
  </defs>
 
  <rect width="1600" height="900" fill="url(#sky)"/>
  <circle cx="1250" cy="260" r="70" fill="#fff4d6" opacity="0.9"/>
 
  <!-- awan -->
  <g fill="#ffffff" opacity="0.55">
    <ellipse cx="300" cy="190" rx="130" ry="26"/>
    <ellipse cx="380" cy="170" rx="90" ry="24"/>
    <ellipse cx="900" cy="130" rx="150" ry="24"/>
    <ellipse cx="990" cy="112" rx="90" ry="22"/>
  </g>
 
  <!-- gunung jauh -->
  <path d="M0 620 L180 440 L300 540 L470 360 L640 560 L800 420 L980 580
           L1150 400 L1330 560 L1480 450 L1600 540 L1600 900 L0 900 Z" fill="url(#far)"/>
 
  <!-- gunung tengah + puncak salju -->
  <path d="M0 700 L220 470 L420 680 L640 330 L880 660 L1080 420 L1300 680
           L1450 520 L1600 650 L1600 900 L0 900 Z" fill="url(#mid)"/>
  <path d="M640 330 L585 400 L615 388 L640 415 L668 388 L698 402 Z" fill="#ffffff" opacity="0.92"/>
  <path d="M1080 420 L1040 470 L1065 460 L1085 482 L1108 460 L1130 472 Z" fill="#ffffff" opacity="0.9"/>
  <path d="M220 470 L190 505 L212 497 L226 512 L244 496 L258 506 Z" fill="#ffffff" opacity="0.85"/>
 
  <!-- gunung dekat + pohon -->
  <path d="M0 800 L260 600 L520 780 L780 640 L1050 790 L1320 620 L1600 780 L1600 900 L0 900 Z"
        fill="url(#near)"/>
  <g fill="#14302f">
    <path d="M90 820 l24 -70 l24 70 z"/><path d="M130 830 l20 -58 l20 58 z"/>
    <path d="M1380 820 l24 -72 l24 72 z"/><path d="M1430 830 l20 -58 l20 58 z"/>
    <path d="M1490 825 l22 -64 l22 64 z"/>
  </g>
</svg>
"""
bg_b64 = base64.b64encode(MOUNTAIN_SVG.encode()).decode()
 
# ---------------------------------------------------------------
# CSS
# ---------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/svg+xml;base64,{bg_b64}") no-repeat center bottom fixed;
        background-size: cover;
    }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ padding-top: 2.5rem; max-width: 760px; }}
 
    .judul {{ text-align: center; color: #ffffff; margin-bottom: 1.5rem;
              text-shadow: 0 2px 12px rgba(0,0,0,.45); }}
    .judul h1 {{ font-size: 2.4rem; margin: 0; font-weight: 800; }}
    .judul p  {{ margin: .3rem 0 0; font-size: 1.05rem; opacity: .92; }}
 
    /* Kartu form */
    [data-testid="stForm"] {{
        background: rgba(255,255,255,.88);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,.6);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 12px 36px rgba(0,0,0,.28);
    }}
    [data-testid="stForm"] label p {{ color: #1f2d3d; font-weight: 600; }}
 
    /* Tombol */
    [data-testid="stForm"] button {{
        width: 100%;
        background: linear-gradient(90deg, #2f6f8f, #3fa796);
        color: #fff; border: none; border-radius: 12px;
        padding: .6rem 0; font-weight: 700; letter-spacing: .3px;
        transition: transform .15s ease, box-shadow .15s ease;
    }}
    [data-testid="stForm"] button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(47,111,143,.45);
        color: #fff;
    }}
 
    /* Kartu hasil */
    .st-key-hasil {{
        background: rgba(255,255,255,.92);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        margin-top: 1.4rem;
        box-shadow: 0 12px 36px rgba(0,0,0,.28);
    }}
    .st-key-hasil img {{ border-radius: 16px; box-shadow: 0 6px 16px rgba(0,0,0,.25); }}
    .info-nama {{ font-size: 1.6rem; font-weight: 800; color: #17324d; margin: 0 0 .2rem; }}
    .info-gender {{ color: #4b5f78; margin-bottom: .9rem; font-weight: 500; }}
    .info-label {{ font-size: .8rem; text-transform: uppercase; letter-spacing: 1px;
                   color: #6b7f95; margin-bottom: .35rem; font-weight: 700; }}
    .chip {{ display: inline-block; background: #e3f2ef; color: #1d6b5f;
             padding: .3rem .85rem; border-radius: 999px; margin: 0 .35rem .35rem 0;
             font-size: .9rem; font-weight: 600; border: 1px solid #b9e0d8; }}
    </style>
    """,
    unsafe_allow_html=True,
)
 
# ---------------------------------------------------------------
# Judul
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="judul">
        <h1>🏔️ Profil Saya</h1>
        <p>Isi data diri Anda, lalu lihat hasilnya di bawah</p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
# ---------------------------------------------------------------
# Form
# ---------------------------------------------------------------
with st.form(key="my_form"):
    nama = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")
    jenis_kelamin = st.radio("Jenis Kelamin", ("Laki-Laki", "Perempuan"), horizontal=True)
    hobi = st.multiselect(
        "Hobi",
        ["Tour Guide", "Traveling", "Menggambar"],
        placeholder="Pilih satu atau lebih hobi",
    )
    gambar = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button(label="Kirim")
 
# ---------------------------------------------------------------
# Hasil
# ---------------------------------------------------------------
if submit:
    if not nama.strip():
        st.warning("Nama lengkap belum diisi.")
    else:
        st.success("Data berhasil dikirim!")
 
        with st.container(key="hasil"):
            col1, col2 = st.columns([1, 2], gap="large")
 
            with col1:
                if gambar is not None:
                    st.image(gambar, use_container_width=True)
                elif Path(GAMBAR_DEFAULT).exists():
                    st.image(GAMBAR_DEFAULT, use_container_width=True)
                else:
                    st.info("Belum ada gambar")
 
            with col2:
                ikon = "👨" if jenis_kelamin == "Laki-Laki" else "👩"
                chips = (
                    "".join(f'<span class="chip">{escape(h)}</span>' for h in hobi)
                    if hobi
                    else "-"
                )
                st.markdown(
                    f"""
                    <p class="info-nama">{escape(nama.strip())}</p>
                    <p class="info-gender">{ikon} {jenis_kelamin}</p>
                    <p class="info-label">Hobi</p>
                    <div>{chips}</div>
                    """,
                    unsafe_allow_html=True,
                )