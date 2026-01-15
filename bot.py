#!/usr/bin/env python3
# Instagram Leak Bot - iPhone Version
import os, json, logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============ CONFIG ============
TOKEN = "8154405833:AAGrMANrXH-7XzsgOEHxoXuMENL70BhLGIA"
OWNER_ID = 6942176313
LEAK_FILE = "leak.json"
# =================================

class InstagramBot:
    def __init__(self):
        print("✅ Bot starting...")
        self.data = {}
        self.load_data()
        self.app = Application.builder().token(TOKEN).build()
        self.setup_handlers()
    
    def load_data(self):
        """تحميل بيانات التسريب"""
        try:
            if os.path.exists(LEAK_FILE):
                with open(LEAK_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"📊 Loaded {len(self.data)} records")
            else:
                print("⚠️ No leak file found, using sample")
                self.data = [
                    {
                        "username": "instagram",
                        "email": "contact@instagram.com",
                        "phone": "+1234567890",
                        "password": "instagram123",
                        "full_name": "Instagram Official"
                    },
                    {
                        "username": "test",
                        "email": "test@example.com",
                        "phone": "+966512345678",
                        "password": "test123456"
                    }
                ]
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def setup_handlers(self):
        """إعداد أوامر البوت"""
        self.app.add_handler(CommandHandler("start", self.start_cmd))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.search_cmd))
    
    async def start_cmd(self, update: Update, context):
        """رسالة البداية"""
        welcome = """
Welcome 👋🏻 This is a bot that leaks Instagram account databases. 

Enter {username <@>} or {email address} or {phone number}

Examples:
• instagram
• @instagram  
• user@email.com
• +1234567890

The bot will search in leaked accounts instantly!
        """
        await update.message.reply_text(welcome)
    
    async def search_cmd(self, update: Update, context):
        """بحث عن الحساب"""
        query = update.message.text.strip().lower()
        user = update.effective_user
        
        # إزالة @ إذا كانت موجودة
        if query.startswith('@'):
            query = query[1:]
        
        await update.message.reply_text(f"🔍 Searching for: {query}")
        
        # البحث في البيانات
        found = None
        for account in self.data:
            # البحث باليوزر
            if 'username' in account and account['username'].lower() == query:
                found = account
                break
            # البحث بالإيميل
            if 'email' in account and account['email'].lower() == query:
                found = account
                break
            # البحث بالهاتف
            if 'phone' in account and account['phone'].replace(' ', '') == query.replace(' ', ''):
                found = account
                break
        
        if found:
            # إعداد النتيجة
            result = f"""
✅ **ACCOUNT FOUND**

👤 **Username:** `{found.get('username', 'N/A')}`
📧 **Email:** `{found.get('email', 'N/A')}`
📱 **Phone:** `{found.get('phone', 'N/A')}`
🔐 **Password:** `{found.get('password', 'N/A')}`
👥 **Name:** {found.get('full_name', 'N/A')}
📊 **Followers:** {found.get('followers', 'N/A')}
📍 **Location:** {found.get('location', 'N/A')}
            """
            await update.message.reply_text(result, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ `{query}` not found in database", parse_mode='Markdown')
    
    def run(self):
        """تشغيل البوت"""
        print("🤖 Bot is running...")
        self.app.run_polling(drop_pending_updates=True)

# ============ تشغيل البوت ============
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        bot = InstagramBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot error: {e}")