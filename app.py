import gradio as gr
from transformers import pipeline, TextIteratorStreamer
from threading import Thread

# 1. تحميل المحرك العصبي (نسخة سريعة)
print("Initializing Wassim's Fast Neural Engine...")
# استخدمنا 0.5B بدلاً من 1.5B للسرعة القصوى على المعالج المجاني
model_id = "Qwen/Qwen2.5-0.5B-Instruct" 
pipe = pipeline("text-generation", model=model_id, device_map="auto")

def predict(message, history):
    system_instructions = (
        "أنت 'Wassim-Pro-Gen' من مختبرات وسيم شرفي. "
        "أجب باختصار وذكاء وباللغة العربية."
    )
    
    messages = [{"role": "system", "content": system_instructions}]
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})

    # إعداد تقنية التدفق (Streaming) للرد السريع
    streamer = TextIteratorStreamer(pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    # تشغيل المعالجة في خلفية منفصلة لعدم تجميد الواجهة
    generation_kwargs = dict(
        input_ids=pipe.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt"),
        streamer=streamer,
        max_new_tokens=512,
        temperature=0.4,
    )
    
    thread = Thread(target=pipe.model.generate, kwargs=generation_kwargs)
    thread.start()

    # إرسال الكلمات فور توليدها للواجهة
    partial_message = ""
    for new_token in streamer:
        partial_message += new_token
        yield partial_message

# تصميم الواجهة الاحترافية السريعة
with gr.Blocks(css=".gradio-container {background-color: #050505; color: #00ff41;}") as demo:
    gr.Markdown("<h1 style='text-align: center;'>⚡ WASSIM FAST-GEN v5 ⚡</h1>")
    gr.ChatInterface(fn=predict, type="messages")

if __name__ == "__main__":
    demo.launch()
