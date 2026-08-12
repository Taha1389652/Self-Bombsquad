# database.py
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class UserDatabase:
    def __init__(self, data_file="database.json"):
        self.data_file = data_file
        self.users = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def get_user(self, user_id):
        return self.users.get(str(user_id))
    
    def register_user(self, user_id, phone_number):
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            self.users[user_id_str] = {
                'user_id': user_id,
                'phone_number': phone_number,
                'balance': 0,
                'self_bots': [],
                'is_active': False,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'transfers': []
            }
            self.save_data()
        return self.users[user_id_str]
    
    def update_user_session(self, user_id, session_file):
        user = self.get_user(user_id)
        if user:
            user['session_file'] = session_file
            user['is_active'] = True
            self.save_data()
            return True
        return False
    
    def update_balance(self, user_id, amount):
        user = self.get_user(user_id)
        if user:
            user['balance'] = user.get('balance', 0) + amount
            self.save_data()
            return True
        return False
    
    def deduct_balance(self, user_id, amount):
        user = self.get_user(user_id)
        if user and user.get('balance', 0) >= amount:
            user['balance'] -= amount
            self.save_data()
            return True
        return False
    
    def transfer_balance(self, from_user_id, to_user_id, amount):
        from_user = self.get_user(from_user_id)
        to_user = self.get_user(to_user_id)
        
        if not from_user or not to_user:
            return False
        
        if from_user.get('balance', 0) < amount:
            return False
        
        from_user['balance'] -= amount
        to_user['balance'] = to_user.get('balance', 0) + amount
        
        # ثبت انتقال
        transfer_record = {
            'from_user': from_user_id,
            'to_user': to_user_id,
            'amount': amount,
            'date': datetime.now().isoformat()
        }
        
        from_user.setdefault('transfers', []).append(transfer_record)
        to_user.setdefault('transfers', []).append(transfer_record)
        
        self.save_data()
        return True
    
    def create_self_bot(self, user_id, session_name):
        user = self.get_user(user_id)
        if user:
            bot_info = {
                'session_name': session_name,
                'created_at': datetime.now().isoformat(),
                'is_active': False,
                'settings': {}
            }
            user.setdefault('self_bots', []).append(bot_info)
            self.save_data()
            return True
        return False
    
    def activate_self_bot(self, user_id, session_name):
        user = self.get_user(user_id)
        if user:
            for bot in user.get('self_bots', []):
                if bot.get('session_name') == session_name:
                    bot['is_active'] = True
                    bot['activated_at'] = datetime.now().isoformat()
                    self.save_data()
                    return True
        return False

# ایجاد نمونه
db = UserDatabase()