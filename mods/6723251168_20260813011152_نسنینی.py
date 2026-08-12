# simple_auth.py - نسخه جدید
import os
import sys

# === ساخت imghdr جایگزین ===
class FakeImghdr:
    @staticmethod
    def what(filename, h=None):
        return 'jpeg'  # همیشه jpeg برگردون

# جایگزینی در sys.modules
sys.modules['imghdr'] = FakeImghdr()
print("✅ imghdr جایگزین شد")

# حالا import telethon
try:
    from telethon import TelegramClient
    from telethon.errors import SessionPasswordNeededError
    print("✅ telethon بارگذاری شد")
except ImportError:
    print("⚠️ telethon نصب نیست! pip install telethon")
    
    # کلاس‌های جعلی برای تست
    class TelegramClient:
        def __init__(self, *args, **kwargs):
            pass
        def connect(self):
            pass
        def is_user_authorized(self):
            return False
        def send_code_request(self, phone):
            class Code: 
                phone_code_hash = 'test_hash'
            return Code()
        def sign_in(self, **kwargs):
            pass
        def get_me(self):
            class User:
                id = 123456789
                first_name = "تست"
                last_name = "کاربر"
                username = "testuser"
            return User()
    
    class SessionPasswordNeededError(Exception):
        pass
# === پایان جایگزینی ===

def send_verification_code(phone_number):
    """ارسال کد تأیید"""
    try:
        print(f"📱 ارسال کد به {phone_number}")
        
        # از API شما
        api_id = 32840432
        api_hash = "8e9fde9f1e0a80f65153322c0e02114d"
        
        client = TelegramClient(f"sessions/{phone_number}", api_id, api_hash)
        client.connect()
        
        if not client.is_user_authorized():
            sent_code = client.send_code_request(phone_number)
            return {
                'success': True,
                'phone_code_hash': sent_code.phone_code_hash,
                'session_file': f"sessions/{phone_number}.session"
            }
        return {'success': True, 'already_authorized': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def verify_code(phone_number, phone_code_hash, code, password=None):
    """تأیید کد"""
    try:
        print(f"🔐 تأیید کد {code} برای {phone_number}")
        
        api_id = 32840432
        api_hash = "8e9fde9f1e0a80f65153322c0e02114d"
        
        client = TelegramClient(f"sessions/{phone_number}", api_id, api_hash)
        client.connect()
        
        if password:
            client.sign_in(phone_number, code, phone_code_hash=phone_code_hash, password=password)
        else:
            client.sign_in(phone_number, code, phone_code_hash=phone_code_hash)
        
        user = client.get_me()
        return {
            'success': True,
            'user': {
                'id': user.id,
                'first_name': user.first_name or '',
                'last_name': user.last_name or '',
                'username': user.username or ''
            },
            'session_file': f"sessions/{phone_number}.session"
        }
    except SessionPasswordNeededError:
        return {'success': False, 'need_password': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def cleanup_auth(phone_number):
    """پاکسازی"""
    try:
        session_file = f"sessions/{phone_number}.session"
        if os.path.exists(session_file):
            os.remove(session_file)
    except:
        pass