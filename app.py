import gradio as gr
from transformers import pipeline

# تحميل الموديل الاحترافي Qwen 2.5
print("Loading Wassim's Neural Engine...")
pipe = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")

def wassim_pro_generator(user_input, history):
    # تحديث "مكان الصنع" والهوية التقنية
    system_instructions = (
        "أنت 'Wassim-Pro-Gen'، نظام ذكاء اصطناعي فائق التطور. "
        "مكان الصنع: تم تطويرك وبرمجتك بالكامل داخل 'مختبرات وسيم شرفي للأنظمة الذكية' (Wassim Sharafi Intelligent Systems Labs). "
        "المطور الرئيسي: المهندس وسيم شرفي. "
        "تخصصك: خبير في Kali Linux، هجمات الويب، البرمجة المتقدمة بـ Python و Java و ++C، وهندسة البرمجيات. "
        "عندما تسأل عن أصلك أو من أين أتيت، أجب: 'أنا ثمرة تطوير مكثف في مختبرات وسيم شرفي، صممت لأكون المساعد التقني الأول في علوم الحاسوب والاختراق'."
    )

    messages = [{"role": "system", "content": system_instructions}]
    
    # إدارة ذاكرة الجلسة
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    
    messages.append({"role": "user", "content": user_input})
    
    try:
        # توليد الرد بتركيز عالٍ
        generation = pipe(messages, max_new_tokens=800, temperature=0.4) 
        response = generation[0]['generated_text'][-1]['content']
        return response
    except Exception as e:
        return f"خطأ في الاتصال بمختبرات وسيم: {str(e)}"

# تصميم الواجهة الاحترافية الجديدة (Dark Cyber Style)
css = """
.gradio-container {background-color: #020202; color: #00ff41; font-family: 'Consolas', monospace !important;}
.chatbot {border: 2px solid #00ff41 !important; border-radius: 10px;}
.user {background-color: #0a1a0a !important; border: 1px solid #00ff41 !important;}
.bot {background-color: #000000 !important; border: 1px solid #005500 !important;}
input {background-color: #050505 !important; border: 1px solid #00ff41 !important; color: #00ff41 !important;}
button {background: linear-gradient(90deg, #004400, #00ff41) !important; color: black !important; font-weight: bold !important;}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1 style='text-align: center; color: #00ff41;'>⚡ WASSIM PRO-GEN v4 ⚡</h1>")
    gr.Markdown("<p style='text-align: center;'>Powered by: Wassim Sharafi Intelligent Systems Labs</p>")
    
    chatbot = gr.Chatbot(label="قناة الاتصال الآمنة", height=550)
    with gr.Row():
        msg = gr.Textbox(
            label="أمر النظام (System Command):",
            placeholder="اكتب سؤالك البرمجي هنا...",
            scale=5
        )
        submit = gr.Button("إرسال")

    def respond(message, chat_history):
        bot_message = wassim_pro_generator(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    submit.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
