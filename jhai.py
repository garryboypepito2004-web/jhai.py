import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import base64

# ═════════════════ CONFIGURATION ═════════════════
SENDER_EMAIL = "garryboypepito71@gmail.com"
SENDER_PASSWORD = "fhyv cimp gync wjmj"
SENDER_NAME = "AILYN CONSTRUCTION"

RECIPIENTS = [
    "garryboypepito2004@gmail.com",
    "ailyn_peps0678@yahoo.com"     
]

BG_URL = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2070"
DEFAULT_ICON = "https://cdn-icons-png.flaticon.com/512/4333/4333644.png"
# ═════════════════════════════════════════════════

st.set_page_config(page_title="AILYN PRO V34.0 | FULL SYSTEM", layout="wide")

# --- 120Hz HIGH-DENSITY UI ENGINE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), url("{BG_URL}");
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}

    /* Hardware-accelerated 120Hz Fluidity */
    .stButton>button {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 0.5px solid rgba(0, 255, 136, 0.5) !important;
        color: #00ff88 !important;
        border-radius: 120px !important;
        height: 65px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
        transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
    }}

    .stButton>button:hover {{
        background: #00ff88 !important;
        color: #001a11 !important;
        box-shadow: 0 0 50px rgba(0, 255, 136, 0.6) !important;
        transform: translateY(-4px);
    }}

    .nav-oval {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 200px;
        padding: 40px 70px;
        margin: 30px auto;
        width: 90%;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 30px 60px rgba(0,0,0,0.7);
    }}

    .stat-box {{ text-align: center; }}
    .stat-label {{ color: #00ff88; font-size: 11px; letter-spacing: 6px; font-weight: 900; opacity: 0.8; }}
    .stat-value {{ color: white; font-size: 42px; font-weight: 900; margin-top: 10px; }}

    header, footer {{ visibility: hidden; }}

    .app-icon {{
        width: 80px;
        height: 80px;
        border-radius: 20px;
        object-fit: cover;
        border: 2px solid #00ff88;
        margin-right: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SYSTEM STATE ---
if 'ledger' not in st.session_state: st.session_state.ledger = []
if 'capital' not in st.session_state: st.session_state.capital = 0.0
if 'surplus' not in st.session_state: st.session_state.surplus = 0.0
if 'b_desc' not in st.session_state: st.session_state.b_desc = "INITIAL PROJECT ALLOCATION"
if 'view' not in st.session_state: st.session_state.view = "HOME"
if 'app_icon' not in st.session_state: st.session_state.app_icon = DEFAULT_ICON

# --- CORE CALCULATIONS ---
total_pool = float(st.session_state.capital + st.session_state.surplus)
total_spent = sum(item['Total'] for item in st.session_state.ledger)
current_bal = total_pool - total_spent

# --- EMAIL RECEIPT DESIGN ---
def get_report_html():
    now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
    rows = "".join([f"""
        <tr style="font-size: 11px; color: #333;">
            <td style="padding: 10px 0; border-bottom: 1px solid #eee;">{e['Date']}</td>
            <td style="padding: 10px 0; border-bottom: 1px solid #eee; text-align: center;">{e['Qty']}</td>
            <td style="padding: 10px 0; border-bottom: 1px solid #eee; color: #1a5d3b; font-weight: 700;">{e['Item']}</td>
            <td style="padding: 10px 0; border-bottom: 1px solid #eee; text-align: right;">{e['Price']:,.2f}</td>
            <td style="padding: 10px 0; border-bottom: 1px solid #eee; text-align: right; font-weight: 700;">{e['Total']:,.2f}</td>
        </tr>
    """ for e in st.session_state.ledger])

    return f"""
    <div style="background-color: #f4f7f6; padding: 40px 0; font-family: 'Inter', Arial, sans-serif;">
        <div style="max-width: 650px; margin: auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
            <div style="background-color: #1a472a; color: white; padding: 40px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; letter-spacing: 2px; font-weight: 900;">AILYN CONSTRUCTION</h1>
                <p style="margin: 5px 0 0 0; font-size: 12px; opacity: 0.8; letter-spacing: 1px;">OFFICIAL INVENTORY SYSTEM</p>
                <p style="margin: 15px 0 0 0; font-size: 10px; opacity: 0.6;">{now}</p>
            </div>
            <div style="padding: 30px;">
                <div style="background: #f1f1f1; padding: 8px 15px; font-size: 10px; font-weight: 900; color: #444; letter-spacing: 1px; margin-bottom: 15px;">BUDGET SUMMARY</div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 5px;">
                    <span style="font-weight: 600; color: #555;">{st.session_state.b_desc}</span>
                    <span style="font-weight: 800;">PHP {st.session_state.capital:,.2f}</span>
                </div>
                <div style="background: #f1f1f1; padding: 8px 15px; font-size: 10px; font-weight: 900; color: #444; letter-spacing: 1px; margin: 25px 0 15px 0;">MATERIAL EXPENDITURE</div>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="font-size: 10px; color: #888; text-align: left; border-bottom: 2px solid #1a472a;">
                            <th style="padding-bottom: 5px;">DATE</th>
                            <th style="padding-bottom: 5px; text-align: center;">QTY</th>
                            <th style="padding-bottom: 5px;">DESCRIPTION</th>
                            <th style="padding-bottom: 5px; text-align: right;">PRICE</th>
                            <th style="padding-bottom: 5px; text-align: right;">TOTAL</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
                <div style="margin-top: 30px; width: 280px; background-color: #1a472a; color: white; border-radius: 12px; padding: 20px;">
                    <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.5px;">FINAL BALANCE (LEFTOVER)</div>
                    <div style="font-size: 22px; font-weight: 900; margin-top: 5px;">PHP {current_bal:,.2f}</div>
                </div>
                <div style="margin-top: 40px; text-align: center; color: #666; font-size: 11px; font-weight: 700;">
                    THANK YOU FOR YOUR TIME TO SEE THIS EMAIL TAYLIN LOVE HEART ❤️<br>
                    <span style="font-weight: 400; opacity: 0.6;">Garry Boy Pepito</span>
                </div>
            </div>
        </div>
    </div>
    """

def send_dispatch(targets):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"AILYN CONSTRUCTION REPORT - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = formataddr((SENDER_NAME, SENDER_EMAIL))
        msg['To'] = ", ".join(targets)
        msg.add_alternative(get_report_html(), subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(SENDER_EMAIL, SENDER_PASSWORD)
            s.send_message(msg)
        return True
    except Exception as e:
        return False

# --- UI RENDER ---
st.markdown(f'''
    <div style="display: flex; align-items: center; padding-left: 5%; margin-bottom: 20px;">
        <img src="{st.session_state.app_icon}" class="app-icon">
        <h2 style="color:white; font-weight:900; letter-spacing:6px; font-size:38px; margin:0;">
            AILYN <span style="color:#00ff88;">PRO V34</span>
        </h2>
    </div>
''', unsafe_allow_html=True)

st.markdown(f"""
    <div class="nav-oval">
        <div class="stat-box"><div class="stat-label">TOTAL ALLOCATION</div><div class="stat-value">₱ {total_pool:,.2f}</div></div>
        <div class="stat-box"><div class="stat-label">TOTAL SPENT</div><div class="stat-value" style="color:#ffcc00;">₱ {total_spent:,.2f}</div></div>
        <div class="stat-box"><div class="stat-label">LEFTOVER</div><div class="stat-value">₱ {current_bal:,.2f}</div></div>
    </div>
""", unsafe_allow_html=True)

_, center_col, _ = st.columns([0.5, 9, 0.5])

with center_col:
    if st.session_state.view == "HOME":
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("➕ MATERIAL"): st.session_state.view = "ADD"; st.rerun()
            if st.button("💰 CAPITAL"): st.session_state.view = "FINANCE"; st.rerun()
        with c2:
            if st.button("🚚 DELIVERY"): st.session_state.view = "ADD"; st.rerun()
            if st.button("📤 DISPATCH REPORT"): st.session_state.view = "EXPORT"; st.rerun()
        with c3:
            if st.button("📦 OTHERS"): st.session_state.view = "ADD"; st.rerun()
            if st.button("🔄 RESET"): st.session_state.ledger = []; st.rerun()

    elif st.session_state.view == "ADD":
        st.markdown("### 🛠️ CONTINUOUS MATERIAL LOGGING")
        with st.form("loop_add", clear_on_submit=True):
            desc = st.text_input("DESCRIPTION").upper()
            qty = st.number_input("QTY", min_value=1, step=1)
            prc = st.number_input("PRICE (₱)", min_value=0.0)
            if st.form_submit_button("COMMIT & CONTINUE"):
                if desc:
                    st.session_state.ledger.append({
                        "Date": datetime.now().strftime("%Y-%m-%d"), 
                        "Qty": qty, "Item": desc, "Price": prc, "Total": qty*prc
                    })
                    st.toast(f"✅ Saved {desc}")
                    st.rerun()
        if st.button("🔙 DONE (EXIT TO MAIN)"):
            st.session_state.view = "HOME"; st.rerun()

    elif st.session_state.view == "FINANCE":
        st.markdown("### APP CONFIGURATION")
        uploaded_file = st.file_uploader("🖼️ CHOICE APP ICON", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.session_state.app_icon = f"data:image/png;base64,{base64.b64encode(uploaded_file.getvalue()).decode()}"
            st.success("Icon Updated!")

        st.session_state.b_desc = st.text_input("Budget Label", value=st.session_state.b_desc)
        st.session_state.capital = st.number_input("Funds (₱)", value=st.session_state.capital)
        if st.button("SAVE & RETURN"): st.session_state.view = "HOME"; st.rerun()

    elif st.session_state.view == "EXPORT":
        st.markdown('<h3 style="color:white; text-align:center;">REPORT DISPATCH CENTER</h3>', unsafe_allow_html=True)
        if st.button("SEND TO ALL RECIPIENTS", use_container_width=True):
            if send_dispatch(RECIPIENTS): st.success("Broadcast successful.")
        if st.button("BACK TO DASHBOARD"): st.session_state.view = "HOME"; st.rerun()