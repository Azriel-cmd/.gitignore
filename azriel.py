import streamlit as st

st.title("Contoh Program Streamlit")

with st.form(key="my_form"):
    nama = st.text_input("Nama Lengkap")
    jenis_kelamin = st.radio("Jenis Kelamin", ("Laki-Laki", "Perempuan"))
    hobi = st.multiselect(
        "Hobi",
        ["Membaca", "Olahraga", "Musik", "Memasak", "Traveling", "Gaming", "Menggambar"]
    )
    gambar = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button(label="Kirim")

if submit:
    st.success("Data berhasil dikirim!")
    st.write(f"**Nama:** {nama}")
    st.write(f"**Jenis Kelamin:** {jenis_kelamin}")
    st.write(f"**Hobi:** {', '.join(hobi) if hobi else '-'}")

    if gambar is not None:
        st.image(gambar, caption="Gambar yang diunggah", width=300)
    else:
        st.write("**Gambar:** Tidak ada gambar yang diunggah")