import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Wassim Cyber Assistant", page_icon="🛡️")

# التأكد من وجود المفتاح
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("المفتاح السري غير موجود في الإعدادات!")

st.title("Wassim Cyber Assistant 🛡️")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسأل خبير الأمن وسيم..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تم تغيير الموديل هنا لضمان العمل 100%
            model = genai.GenerativeModel('gemini-pro') 
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
