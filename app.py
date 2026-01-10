import gradio as gr
from transformers import pipeline

# 1. تحميل المحرك العصبي لمختبرات وسيم
print("Initializing Wassim's Neural Engine v4...")
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")

# 2. دالة المعالجة والهوية التقنية
def predict(message, history):
    system_instructions = (
        "أنت 'Wassim-Pro-Gen'، مساعد ذكي فائق التطور مخصص للبرمجة والأمن السيبراني. "
        "مكان الصنع: تم تطويرك وبرمجتك بالكامل داخل 'مختبرات وسيم شرفي للأنظمة الذكية'. "
        "المطور الرئيسي: المبرمج المهندس وسيم شرفي. "
        "التخصصات: Kali Linux, Python, Java, C++, اختراق الأنظمة الأخلاقي، وعلوم الحاسوب. "
        "يجب أن تتحدث دائماً باللغة العربية الفصحى وبنبرة خبير تقني محترف."
    )

    messages = [{"role": "system", "content": system_instructions}]
    
    # بناء ذاكرة المحادثة (History)
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    
    messages.append({"role": "user", "content": message})
    
    # توليد الإجابة بدقة عالية
    response = pipe(messages, max_new_tokens=1024, temperature=0.4)
    return response[0]['generated_text'][-1]['content']

# 3. تصميم واجهة الهاكرز المتقدمة (Matrix Style)
css = """
.gradio-container {background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace !important;}
.chatbot {border: 1px solid #00ff41 !important; border-radius: 10px;}
footer {display: none !important;}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1 style='text-align: center; color: #00ff41;'>⚡ WASSIM CYBER-ASSISTANT v4 ⚡</h1>")
    gr.Markdown("<p style='text-align: center; color: #00ff41;'>Official Product of: Wassim Sharafi Intelligent Systems Labs</p>")
    
    gr.ChatInterface(
        fn=predict,
        chatbot=gr.Chatbot(height=600, show_label=False),
        textbox=gr.Textbox(placeholder="أدخل أمرك البرمجي هنا وسيم...", container=False, scale=7),
        theme="soft",
        submit_btn="إرسال عبر القناة الآمنة",
        retry_btn="إعادة المحاولة",
        undo_btn="تراجع",
        clear_btn="مسح السجل",
    )

if __name__ == "__main__":
    demo.launch()
