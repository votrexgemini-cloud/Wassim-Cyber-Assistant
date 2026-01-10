import gradio as gr
from transformers import pipeline, TextIteratorStreamer
from threading import Thread

# 1. Loading the fast Neural Engine
print("Loading Wassim's AI Engine...")
model_id = "Qwen/Qwen2.5-0.5B-Instruct" 
pipe = pipeline("text-generation", model=model_id, device_map="auto")

def predict(message, history):
    # System Instructions
    system_instructions = (
        "You are 'Wassim Smart Assistant', a Cyber Security and Programming Expert. "
        "Origin: Developed at Wassim Sharafi Intelligent Systems Labs. "
        "Always respond in English."
    )
    
    messages = [{"role": "system", "content": system_instructions}]
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})

    streamer = TextIteratorStreamer(pipe.tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    generation_kwargs = dict(
        input_ids=pipe.tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt"),
        streamer=streamer,
        max_new_tokens=1024,
        temperature=0.3,
    )
    
    thread = Thread(target=pipe.model.generate, kwargs=generation_kwargs)
    thread.start()

    partial_message = ""
    for new_token in streamer:
        partial_message += new_token
        yield partial_message

# 2. UI Design
css = """
.gradio-container {background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace !important;}
.chatbot {border: 1px solid #00ff41 !important;}
footer {display: none !important;}
#title {text-align: center; font-size: 2em; margin-bottom: 20px; color: #00ff41; font-weight: bold;}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("<div id='title'>Wassim Smart Assistant: Cyber Security Expert</div>")
    
    gr.ChatInterface(
        fn=predict,
        chatbot=gr.Chatbot(
            height=600, 
            show_label=False,
            # هذه الخاصية تضيف رسالة الترحيب في بداية الشات
            value=[[None, "Hello, I'm wassim digital assistant"]] 
        ),
        textbox=gr.Textbox(placeholder="Ask the Cyber Security Expert...", container=False, scale=7),
        theme="soft",
        submit_btn="Send Message",
        retry_btn="Retry",
        clear_btn="Clear History",
    )

if __name__ == "__main__":
    demo.launch()
