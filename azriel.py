import streamlit as st

st.title("Contoh Program Streamlit")

with st.form(key="my_form"):
    nama = st.text_input("Nama Lengkap")
    jenis_kelamin = st.radio("Jenis Kelamin", ("Laki-Laki", "Perempuan"))
    submit = st.form_submit_button(label="Kirim")
    