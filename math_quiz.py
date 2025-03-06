import streamlit as st
import random
import time

# Set judul aplikasi
st.title("Math Quiz dengan Timer ⏳")

# **Batas waktu per soal (25 detik)**
batas_waktu = 25  

# **Inisialisasi session state**
if "score" not in st.session_state:
    st.session_state.score = 0  # Skor awal

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()  # Waktu mulai

if "num1" not in st.session_state or "num2" not in st.session_state:
    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.operation = random.choice(["+", "-"])
    
    # Pastikan hasil pengurangan tidak negatif
    if st.session_state.operation == "-" and st.session_state.num1 < st.session_state.num2:
        st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1

    st.session_state.correct_answer = (
        st.session_state.num1 + st.session_state.num2
        if st.session_state.operation == "+"
        else st.session_state.num1 - st.session_state.num2
    )

if "checked" not in st.session_state:
    st.session_state.checked = False  # Status apakah jawaban sudah diperiksa

# **Menghitung waktu tersisa**
waktu_tersisa = batas_waktu - (time.time() - st.session_state.start_time)
st.write(f"🕒 Waktu tersisa: {max(0, int(waktu_tersisa))} detik")

# Menampilkan soal matematika
st.subheader(f"{st.session_state.num1} {st.session_state.operation} {st.session_state.num2} = ?")

# **Input jawaban**
user_answer = st.text_input("Jawaban kamu:", value="", key="answer")

# **Fungsi untuk menampilkan penyelesaian dengan kotak**
def tampilkan_penyelesaian(num1, num2, operasi):
    if operasi == "+":
        penyelesaian = f"📖 Penyelesaian:\n"
        penyelesaian += f"{'😄' * num1} + {'😄' * num2} = {'😄' * (num1 + num2)}"
    else:
        penyelesaian = f"📖 Penyelesaian:\n"
        penyelesaian += f"{'😄' * num1} - {'😄' * num2} = {'😄' * (num1 - num2)}"
    return penyelesaian

# **Jika waktu habis, tampilkan jawaban dan penyelesaian**
if waktu_tersisa <= 0:
    st.error("⏳ Waktu habis! Soal baru muncul.")
    st.info(f"Jawaban yang benar adalah: {st.session_state.correct_answer}")
    
    # **Menampilkan penyelesaian visual dengan kotak**
    st.write(tampilkan_penyelesaian(st.session_state.num1, st.session_state.num2, st.session_state.operation))

    # **Tunda sebelum mereset soal agar pengguna bisa melihat jawabannya**
    time.sleep(5)
    
    # Reset soal baru
    st.session_state.start_time = time.time()
    st.session_state.checked = False

    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.operation = random.choice(["+", "-"])

    if st.session_state.operation == "-" and st.session_state.num1 < st.session_state.num2:
        st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1

    st.session_state.correct_answer = (
        st.session_state.num1 + st.session_state.num2
        if st.session_state.operation == "+"
        else st.session_state.num1 - st.session_state.num2
    )

    st.rerun()

# **Cek jawaban jika tombol ditekan**
if st.button("Cek Jawaban"):
    if user_answer.isdigit() or (user_answer.startswith("-") and user_answer[1:].isdigit()):
        user_answer = int(user_answer)
        if user_answer == st.session_state.correct_answer:
            st.success("✅ Jawaban benar!")
            st.session_state.score += 1  # Tambah skor
        else:
            st.error(f"❌ Salah! Jawaban yang benar adalah {st.session_state.correct_answer}.")
            # **Tampilkan penyelesaian visual dengan kotak**
            st.write(tampilkan_penyelesaian(st.session_state.num1, st.session_state.num2, st.session_state.operation))

        # **Tunda refresh agar jawaban bisa terlihat**
        st.session_state.checked = True  
    else:
        st.warning("⚠️ Masukkan angka yang valid!")

# **Reset soal jika jawaban sudah diperiksa**
if st.session_state.checked:
    time.sleep(5)  # **Tunggu beberapa detik sebelum soal baru muncul**
    st.session_state.start_time = time.time()
    st.session_state.checked = False

    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.operation = random.choice(["+", "-"])

    if st.session_state.operation == "-" and st.session_state.num1 < st.session_state.num2:
        st.session_state.num1, st.session_state.num2 = st.session_state.num2, st.session_state.num1

    st.session_state.correct_answer = (
        st.session_state.num1 + st.session_state.num2
        if st.session_state.operation == "+"
        else st.session_state.num1 - st.session_state.num2
    )

    st.rerun()

# **Menampilkan total skor**
st.write(f"⭐ Skor kamu: {st.session_state.score}")