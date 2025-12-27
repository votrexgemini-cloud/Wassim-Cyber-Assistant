import streamlit as st
import google.generativeai as genai

# إعداد واجهة البوت لتبدو احترافية
st.set_page_config(page_title="Wassim Cyber Assistant", page_icon="🛡️")

# استدعاء المفتاح السري (سنضيفه في Streamlit لاحقاً)
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.warning("الرجاء إضافة المفتاح السري في إعدادات Streamlit.")

st.title("Wassim Cyber Assistant 🛡️")
st.caption("المساعد الرقمي الرسمي لخبير الأمن وسيم")

# نظام ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال أسئلة المستخدم
if prompt := st.chat_input("اسأل وسيم عن الأمن السيبراني..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل Gemini السريع والمستقر
            model = genai.GenerativeModel('gemini-1.5-flash', 
                                        system_instruction="أنت المساعد الرقمي لوسيم، خبير Kali Linux والأمن السيبراني. أجب باختصار واحترافية.")
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
