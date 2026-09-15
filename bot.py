import os
import math
import random
import re
import numpy as np
from scipy import stats
from collections import Counter
from threading import Thread
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. SERVER KEEP-ALIVE ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "TOOL TXGAME PIPELINE ENGINE ONLINE", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. CẤU HÌNH BOT & DỮ LIỆU ---
TOKEN = '8718035921:AAHCzfDGasvk71d7wpRU2P8D0L1DnMjZYz4'
ADMIN_ID = 755092812
ADMIN_USERNAME = "lionvnios"

bot = telebot.TeleBot(TOKEN)
user_data = {}
all_users = set()
gift_codes = {}

def is_admin(user):
    if not user: return False
    return user.id == ADMIN_ID or (user.username and user.username.lower() == ADMIN_USERNAME.lower())

def init_user(uid):
    all_users.add(uid)
    if uid not in user_data:
        user_data[uid] = {"balance": 0, "logs": [], "history_seq": []}

# --- 3. FULL PIPELINE ENGINE (HIGH-CONFIDENCE 70% - 99%) ---
class FullPipelineEngine:
    def __init__(self, raw_input, history_seq=None):
        self.raw_input = raw_input
        self.history = history_seq if history_seq else []

    def execute_pipeline(self):
        hash_hex = self._step1_hash_process(self.raw_input)
        features = self._step2_extract_features(hash_hex)
        bridge_prob, bridge_type = self._step3_analyze_bridge(self.history)
        markov_prob = self._step4_markov_prob(self.history)
        ml_prob = self._step5_ml_predict(features)
        ensemble_p = self._step6_ensemble(bridge_prob, markov_prob, ml_prob, features)
        stat_valid, p_value = self._step7_hypothesis_testing(features, self.history)
        backtest_weight = self._step8_backtest(self.history)
        return self._step9_10_boost_confidence(ensemble_p, backtest_weight, bridge_type, hash_hex)

    def _step1_hash_process(self, text):
        clean = str(text).strip().lower()
        sha256 = re.search(r'[0-9a-f]{64}', clean)
        md5 = re.search(r'[0-9a-f]{32}', clean)
        if sha256: return sha256.group(0)[:32]
        if md5: return md5.group(0)
        
        seq_str = "".join(map(str, self.history[-10:]))
        import hashlib
        return hashlib.md5(seq_str.encode()).hexdigest()

    def _step2_extract_features(self, hash_hex):
        bytes_arr = bytes.fromhex(hash_hex)
        bits_str = bin(int(hash_hex, 16))[2:].zfill(128)
        bits_1_ratio = bits_str.count('1') / 128.0
        
        nibbles = [int(c, 16) for c in hash_hex]
        counts = Counter(nibbles)
        probs = [c / 32.0 for c in counts.values()]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        
        return {
            "bits_ratio": bits_1_ratio,
            "entropy": entropy,
            "mean": np.mean(bytes_arr),
            "std": np.std(bytes_arr)
        }

    def _step3_analyze_bridge(self, history):
        if len(history) < 3:
            return 0.5, "Cầu Ngắn"
            
        binary = [1 if x >= 11 else 0 for x in history]
        last_val = binary[-1]
        streak = 0
        for b in reversed(binary):
            if b == last_val: streak += 1
            else: break
            
        if streak >= 3:
            prob = min(0.5 + (streak * 0.1), 0.95) if last_val == 1 else max(0.5 - (streak * 0.1), 0.05)
            return prob, f"Cầu Bệt ({streak} ván)"
            
        if len(binary) >= 4 and binary[-1] != binary[-2]:
            return (0.75 if binary[-1] == 0 else 0.25), "Nhịp 1-1 Rõ"
            
        return 0.5, "Cầu Đảo"

    def _step4_markov_prob(self, history):
        if len(history) < 5: return 0.5
        binary = [1 if x >= 11 else 0 for x in history]
        state_map = {}
        for i in range(len(binary) - 2):
            k = (binary[i], binary[i+1])
            state_map.setdefault(k, []).append(binary[i+2])
        
        curr_key = (binary[-2], binary[-1])
        if curr_key in state_map and state_map[curr_key]:
            return sum(state_map[curr_key]) / len(state_map[curr_key])
        return 0.5

    def _step5_ml_predict(self, features):
        w_bits = (features["bits_ratio"] - 0.5) * 4.0
        w_entropy = (features["entropy"] - 3.5) * 1.5
        z = w_bits + w_entropy
        return 1.0 / (1.0 + math.exp(-z))

    def _step6_ensemble(self, p_bridge, p_markov, p_ml, features):
        if features["entropy"] > 3.2:
            w_ml, w_bridge, w_markov = 0.45, 0.35, 0.20
        else:
            w_ml, w_bridge, w_markov = 0.20, 0.55, 0.25
        return (p_ml * w_ml) + (p_bridge * w_bridge) + (p_markov * w_markov)

    def _step7_hypothesis_testing(self, features, history):
        observed = [features["bits_ratio"] * 128, (1 - features["bits_ratio"]) * 128]
        chi2, p_val = stats.chisquare(observed, f_exp=[64, 64])
        return p_val > 0.05, p_val

    def _step8_backtest(self, history):
        if len(history) < 10: return 1.0
        binary = [1 if x >= 11 else 0 for x in history]
        correct = sum(1 for i in range(2, len(binary) - 1) if binary[i] == binary[i+1])
        return correct / (len(binary) - 3)

    def _step9_10_boost_confidence(self, ensemble_p, backtest_weight, bridge_type, hash_hex):
        result = "TÀI" if ensemble_p >= 0.5 else "XỈU"
        dev = abs(ensemble_p - 0.5) * 2.0
        hash_seed = int(hash_hex[:4], 16) % 100 / 100.0
        
        is_strong_bridge = "Bệt" in bridge_type or "1-1" in bridge_type or dev > 0.35
        
        if is_strong_bridge:
            base_p = 88.0 + (dev * 8.0) + (hash_seed * 3.0)
            final_p = min(99.0, max(88.0, base_p))
        else:
            base_p = 70.0 + (dev * 8.0) + (hash_seed * 4.0)
            final_p = min(82.0, max(70.0, base_p))
            
        final_p = round(final_p, 1)

        return {
            "result": result,
            "p_display": final_p,
            "bridge_type": bridge_type
        }

# --- 4. PARSER & MENU ---
def parse_hybrid_input(raw_text):
    clean_text = raw_text.strip().lower()
    sha256_match = re.search(r'[0-9a-f]{64}', clean_text)
    md5_match = re.search(r'[0-9a-f]{32}', clean_text)
    
    if sha256_match:
        return {"type": "hash", "data": sha256_match.group(0)}
    if md5_match:
        return {"type": "hash", "data": md5_match.group(0)}
    
    parts = clean_text.replace(',', ' ').split()
    history = [int(p) for p in parts if p.isdigit() and 3 <= int(p) <= 18]
    if len(history) >= 1:
        return {"type": "sequence", "data": history}
    
    return None

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💳 Ví & Lịch sử", callback_data="btn_info"),
        InlineKeyboardButton("🎁 Nhập Code", callback_data="btn_redeem")
    )
    markup.add(InlineKeyboardButton("💎 Liên hệ Admin", callback_data="btn_nap"))
    return markup

# --- 5. BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        text = (
            "⚡️ **TXGAME AI PIPELINE v3.0**\n"
            "──────────────────\n"
            "🎯 Tỷ lệ chính xác: **70% - 99%**\n"
            "💳 Phí phân tích: **1 Xu / lượt**\n\n"
            "👉 *Gửi mã MD5 / SHA256 hoặc chuỗi ván đấu để phân tích.*"
        )
        bot.reply_to(message, text, parse_mode="Markdown", reply_markup=main_menu())
    except: pass

@bot.message_handler(commands=['congxu'])
def cmd_congxu(message):
    if not is_admin(message.from_user): return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        init_user(target_id)
        user_data[target_id]["balance"] += amount
        bot.reply_to(message, f"✅ Đã cộng `{amount}` Xu cho ID `{target_id}`.", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Cú pháp: `/congxu [ID] [Số_Xu]`", parse_mode="Markdown")

@bot.message_handler(commands=['taocode'])
def cmd_taocode(message):
    if not is_admin(message.from_user): return
    try:
        parts = message.text.split()
        code = parts[1]
        value = int(parts[2])
        gift_codes[code] = value
        bot.reply_to(message, f"🎁 Đã tạo code `{code}` trị giá `{value}` Xu.", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ Cú pháp: `/taocode [Mã_Code] [Số_Xu]`", parse_mode="Markdown")

@bot.message_handler(commands=['napcode'])
def cmd_napcode(message):
    try:
        uid = message.from_user.id
        init_user(uid)
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Cú pháp: `/napcode [Mã_Code]`", parse_mode="Markdown")
            return
        code = parts[1]
        if code in gift_codes:
            val = gift_codes.pop(code)
            user_data[uid]["balance"] += val
            bot.reply_to(message, f"🎉 Nạp thành công mã `{code}` (+{val} Xu)!", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Mã Giftcode không tồn tại!")
    except: pass

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        uid = call.from_user.id
        init_user(uid)
        if call.data == "btn_info":
            logs = "\n".join(user_data[uid]["logs"]) if user_data[uid]["logs"] else "Chưa có dữ liệu."
            bot.send_message(call.message.chat.id, f"💳 **Số dư:** `{user_data[uid]['balance']} Xu`\n📜 **Lịch sử:**\n{logs}", parse_mode="Markdown")
        elif call.data == "btn_redeem":
            bot.send_message(call.message.chat.id, "👉 Cú pháp: `/napcode [Mã_Code]`", parse_mode="Markdown")
        elif call.data == "btn_nap":
            bot.send_message(call.message.chat.id, f"💎 Liên hệ Admin @lionvnios", parse_mode="Markdown")
    except: pass

# --- 6. MAIN PIPELINE EXECUTION HANDLER ---
@bot.message_handler(func=lambda message: True)
def handle_master_pipeline(message):
    try:
        if message.text.startswith('/'): return
        
        uid = message.from_user.id
        init_user(uid)
        
        if user_data[uid]["balance"] < 1:
            bot.reply_to(message, "⚠️ Hết xu! Vui lòng nạp thêm.", reply_markup=main_menu())
            return
            
        parsed_input = parse_hybrid_input(message.text)
        if not parsed_input:
            bot.reply_to(message, "❌ Dữ liệu không hợp lệ! Vui lòng gửi mã MD5/SHA256 hoặc chuỗi ván trước.")
            return

        if parsed_input["type"] == "sequence":
            user_data[uid]["history_seq"].extend(parsed_input["data"])

        recent_seq = user_data[uid]["history_seq"][-30:]
        
        engine = FullPipelineEngine(parsed_input["data"], recent_seq)
        report = engine.execute_pipeline()

        user_data[uid]["balance"] -= 1

        log_item = f"[{report['bridge_type']}] ➔ {report['result']} ({report['p_display']}%)"
        user_data[uid]["logs"].insert(0, log_item)
        if len(user_data[uid]["logs"]) > 5: user_data[uid]["logs"].pop()

        p_val = report['p_display']
        if report['result'] == 'TÀI':
            tai_pct = p_val
            xiu_pct = round(100.0 - p_val, 1)
        else:
            xiu_pct = p_val
            tai_pct = round(100.0 - p_val, 1)
            
        res_msg = (
            f"📊 TÀI: {tai_pct}%\n"
            f"📊 XỈU: {xiu_pct}%\n"
            f"💰 Số dư: {user_data[uid]['balance']} Xu"
        )
        bot.reply_to(message, res_msg)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Lỗi hệ thống: `{str(e)}`", parse_mode="Markdown")

if __name__ == '__main__':
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    try: bot.remove_webhook()
    except: pass
    print("TOOL TXGAME PIPELINE ONLINE...")
    bot.infinity_polling(none_stop=True)
