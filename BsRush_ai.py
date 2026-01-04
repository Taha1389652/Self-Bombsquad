# ba_meta require api 9
# coding: utf-8
#کصمادرت اسکی بری کیر تو ناموس اونی که اسکی بره حتی اگه یک خط باشه کصمادرت حتی یک خط کد رو هم ببینی
import babase
import bauiv1 as bui
import bascenev1 as bs
import threading
import json
import urllib.request
import time

GITHUB_RAW_URL = "https://raw.githubusercontent.com/Taha1389652/Self-Bombsquad/refs/heads/main/Test.txt"

ADVERTISEMENT_MESSAGE = u"🎮 @BsRush_Mod : مرجع دانلود مود های بمب اسکواد 🚀"
ADVERTISEMENT_INTERVAL = 300
advertisement_timer = None

# Global variables
stop_current_response = False
is_processing = False
current_question = ""
OPENAI_API_KEY = ""  
reload_in_progress = False

def load_api_key_from_github():
    global OPENAI_API_KEY, reload_in_progress
    
    try:
        print("🔗 Loading API key from GitHub...")

        req = urllib.request.Request(
            GITHUB_RAW_URL,
            headers={
                'User-Agent': 'BombSquad-ChatGPT-Plugin/1.0'
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            api_key = response.read().decode('utf-8').strip()

            if api_key and len(api_key) > 20:
                OPENAI_API_KEY = api_key
                print("✅ API key loaded successfully")
                return True
            else:
                print("⚠️ Invalid API key format")
                return False
                
    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTP Error loading key: {e.code}")
        if e.code == 404:
            print("❌ File not found. Check the URL.")
    except urllib.error.URLError as e:
        print(f"⚠️ URL Error loading key: {e.reason}")
    except Exception as e:
        print(f"⚠️ Error loading key: {e}")
    finally:
        reload_in_progress = False
    
    return False

def split_words(text, n=5):
    words = text.split()
    lines = []
    for i in range(0, len(words), n):
        line = " ".join(words[i:i+n])
        lines.append(line)
    return lines

def send_advertisement():
    try:
        bs.chatmessage(ADVERTISEMENT_MESSAGE)
        print("✅ Advertisement sent")
    except Exception as e:
        print(f"⚠️ Error sending ad: {e}")

def advertisement_loop():
    global advertisement_timer
    
    while True:
        try:
            time.sleep(ADVERTISEMENT_INTERVAL)
            babase.pushcall(send_advertisement, from_other_thread=True)
        except Exception as e:
            print(f"⚠️ Error in ad loop: {e}")
            time.sleep(10)

def start_advertisement_timer():
    global advertisement_timer
    
    advertisement_timer = threading.Thread(target=advertisement_loop, daemon=True)
    advertisement_timer.start()
    print("✅ Advertisement timer started")

_original_chatmessage = bs.chatmessage
def chatmessage_hook(msg: str, clients=None):
    global stop_current_response, is_processing, current_question, OPENAI_API_KEY, reload_in_progress
    
    _original_chatmessage(msg, clients)

    if msg.startswith("/ask "):
        if not OPENAI_API_KEY:
            bs.chatmessage("❌ API key not loaded. Plugin not ready.")
            return
            
        if is_processing:
            bs.chatmessage("⏳ Processing previous question... Please wait")
            return
            
        if reload_in_progress:
            bs.chatmessage("⏳ Reload in progress... Please wait")
            return
            
        question = msg[5:].strip()
        if not question:
            bs.chatmessage("❌ Please write your question after /ask")
            return
            
        stop_current_response = False
        current_question = question
        bs.chatmessage("🤖 Thinking...")
        
        thread = threading.Thread(target=process_question, args=(question,), daemon=True)
        thread.start()

    elif msg == "/stop":
        if is_processing:
            stop_current_response = True
            bs.chatmessage("⏸️ Current response stopped")
            print(f"Stop requested for: {current_question[:50]}")
        else:
            bs.chatmessage("✅ No processing in progress")

    elif msg == "/reload":
        if reload_in_progress:
            bs.chatmessage("⏳ Reload already in progress...")
            return
            
        if is_processing:
            bs.chatmessage("⚠️ Cannot reload while processing a question")
            bs.chatmessage("Use /stop first, then /reload")
            return
            
        reload_in_progress = True
        bs.chatmessage("🔄 Reloading API key from GitHub...")
        
        # Clear old key first
        OPENAI_API_KEY = ""
        
        # Start reload in background thread
        def reload_thread():
            success = load_api_key_from_github()
            babase.pushcall(
                lambda: bs.chatmessage("✅ API key reloaded successfully" if success else "❌ Failed to reload API key"),
                from_other_thread=True
            )
        
        threading.Thread(target=reload_thread, daemon=True).start()

bs.chatmessage = chatmessage_hook

def process_question(prompt: str):
    global stop_current_response, is_processing, current_question
    
    is_processing = True
    current_question = prompt
    
    try:
        response = send_to_chatgpt(prompt)
        
        if stop_current_response:
            babase.pushcall(
                lambda: bs.chatmessage("🚫 Response cancelled"),
                from_other_thread=True
            )
            return
            
        if response:
            display_response(response)
        else:
            babase.pushcall(
                lambda: bs.chatmessage("⚠️ No response received"),
                from_other_thread=True
            )
            
    except urllib.error.HTTPError as e:
        if not stop_current_response:
            if e.code == 401:
                babase.pushcall(
                    lambda: bs.chatmessage("❌ Invalid API key (401 Unauthorized)"),
                    from_other_thread=True
                )
                babase.pushcall(
                    lambda: bs.chatmessage("Use /reload to update your API key"),
                    from_other_thread=True
                )
            elif e.code == 429:
                babase.pushcall(
                    lambda: bs.chatmessage("⚠️ Rate limit exceeded. Try again later."),
                    from_other_thread=True
                )
            else:
                babase.pushcall(
                    lambda: bs.chatmessage(f"⚠️ HTTP Error: {e.code}"),
                    from_other_thread=True
                )
    except urllib.error.URLError as e:
        if not stop_current_response:
            babase.pushcall(
                lambda: bs.chatmessage("🌐 Internet connection error"),
                from_other_thread=True
            )
    except Exception as e:
        if not stop_current_response:
            error_msg = str(e)
            if "HTTP" in error_msg:
                babase.pushcall(
                    lambda: bs.chatmessage("⚠️ Server connection error"),
                    from_other_thread=True
                )
            else:
                babase.pushcall(
                    lambda: bs.chatmessage(f"⚠️ Error: {error_msg[:40]}"),
                    from_other_thread=True
                )
    finally:
        is_processing = False
        current_question = ""

def send_to_chatgpt(prompt: str):
    global stop_current_response, OPENAI_API_KEY
    
    if stop_current_response:
        return None
    
    if not OPENAI_API_KEY or OPENAI_API_KEY.strip() == "":
        raise Exception("API key not available")
    
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY.strip()}"
    }
    data = {
        "model": "gpt-4.1-mini",
        "input": prompt,
        "max_output_tokens": 200
    }

    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode(), 
            headers=headers
        )
        
        with urllib.request.urlopen(req, timeout=15) as r:
            res = json.loads(r.read().decode())
            
            if stop_current_response:
                return None
                
            return res["output"][0]["content"][0]["text"]
            
    except Exception as e:
        if not stop_current_response:
            raise e
        return None

def display_response(answer: str):
    global stop_current_response
    
    lines = split_words(answer, 6)
    
    babase.pushcall(
        lambda: bs.chatmessage("💬 Response:"),
        from_other_thread=True
    )
    time.sleep(0.5)
    
    line_count = 0
    for line in lines:
        if stop_current_response:
            return
            
        if line.strip():
            babase.pushcall(
                lambda l=line: bs.chatmessage(l),
                from_other_thread=True
            )
            line_count += 1

            if line_count < len(lines):
                time.sleep(3.0)
    
    if not stop_current_response:
        babase.pushcall(
            lambda: bs.chatmessage("✅ Response completed"),
            from_other_thread=True
        )

# -------- PLUGIN EXPORT --------
# ba_meta export babase.Plugin
class ChatGPTPlugin(babase.Plugin):
    def on_app_running(self):
        global stop_current_response, is_processing, current_question, reload_in_progress
        
        stop_current_response = False
        is_processing = False
        current_question = ""
        reload_in_progress = False

        key_loaded = load_api_key_from_github()

        start_advertisement_timer()
        
        if key_loaded:
            bs.chatmessage("✅ ChatGPT Plugin activated")
            bs.chatmessage("🔑 API key loaded from GitHub")
        else:
            bs.chatmessage("⚠️ ChatGPT Plugin - API key not loaded")
            bs.chatmessage("❌ Use /reload to retry")
        
        bs.chatmessage("📢 Ads every 5 minutes")
        bs.chatmessage(u"⚡ @BsRush_Mod : بهترین مودهای بازی")
        bs.chatmessage("📝 Commands:")
        bs.chatmessage("/ask [question] - Ask a question")
        bs.chatmessage("/stop - Stop current response")
        bs.chatmessage("/reload - Reload API key")

        def send_first_ad():
            time.sleep(15)
            bs.chatmessage(ADVERTISEMENT_MESSAGE)
        
        threading.Thread(target=send_first_ad, daemon=True).start()
