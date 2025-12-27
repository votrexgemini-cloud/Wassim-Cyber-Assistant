import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Wassim Cyber Assistant", page_icon="🛡️")

# إعداد المفتاح السري
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("الرجاء إضافة المفتاح في Secrets")

st.title("Wassim Cyber Assistant 🛡️")
st.caption("المساعد الرقمي الرسمي لخبير الأمن وسيم")

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
            # استخدام أحدث تسمية للموديل المستقر لتجنب خطأ 404
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest') 
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # محاولة أخيرة بموديل بديل إذا فشل الأول
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error(f"حدث خطأ تقني: {e}")
