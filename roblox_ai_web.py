import streamlit as st
from groq import Groq
import datetime


st.set_page_config(page_title="RECON API - Terminal", page_icon="🕵️‍♂️", layout="wide")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "full_history" not in st.session_state:
    st.session_state.full_history = []
if "credits" not in st.session_state:
    st.session_state.credits = 5


st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .credit-header {
        background: rgba(15, 15, 15, 0.95);
        border: 1px solid #1f1f1f;
        padding: 15px 25px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        border-left: 5px solid #ff4b4b;
    }
    .user-avatar { width: 50px; height: 50px; border-radius: 50%; border: 2px solid #ff4b4b; object-fit: cover; }
    .credit-amount { color: #ff4b4b; font-weight: bold; font-size: 1.2rem; }
    .owner-badge { color: #ff4b4b; border: 1px solid #ff4b4b; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }
    
    /* Style spécifique pour les LOGS */
    .log-entry {
        background: #0d0d0d;
        border: 1px solid #1f1f1f;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .log-time { color: #ff4b4b; font-size: 0.8rem; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)


try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY manquante.")


with st.sidebar:
    st.title("📡 RECON HUB")
    tab_acc, tab_shop, tab_logs = st.tabs(["🔑 ACCÈS", "🛒 BOUTIQUE", "📜 LOGS"])
    
    with tab_acc:
        access_code = st.text_input("Code secret :", type="password")
        if access_code == "OWNER_RECON_2026":
            rank, user_name, credits_val = "OWNER", "RECON_ROOT", "∞"
        else:
            rank, user_name, credits_val = "FREE", "CIVILIAN", str(st.session_state.credits)
        
        st.divider()
        if st.button("🗑️ RESET SESSION"):
            st.session_state.messages = []
            st.rerun()

    with tab_shop:
        st.subheader("VIP Upgrades")
        st.info("💠 PREMIUM: 4.99€/mois\n👑 OWNER: 14.99€ (À VIE)")
        st.button("Accéder à la boutique", use_container_width=True)

    with tab_logs:
        st.subheader("HISTORIQUE")
        if not st.session_state.full_history:
            st.write("Aucun log détecté.")
        else:
            
            for log in reversed(st.session_state.full_history):
                with st.expander(f"🕒 {log['time']} | {log['query']}"):
                    st.code(log['code'], language="lua")


custom_avatar = "https://cdn-icons-png.flaticon.com/512/6033/6033716.png" # Ton image Meta
st.markdown(f"""
    <div class="credit-header">
        <div class="user-info" style="display:flex; align-items:center; gap:15px;">
            <img src="{custom_avatar}" class="user-avatar">
            <div>
                <div style="font-weight: bold;">{user_name}</div>
                <span class="owner-badge">{rank} ACCESS</span>
            </div>
        </div>
        <div class="stat-box" style="text-align:right;">
            <div style="font-size: 0.7rem; color: #666;">CRÉDITS</div>
            <div class="credit-amount">{credits_val}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Initialisation..."):
    if rank == "FREE" and st.session_state.credits <= 0:
        st.error("❌ CRÉDITS ÉPUISÉS.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("PROCESSING..."):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Tu es ReconAI. Expert Roblox Luau. Réponds en Luau."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        ]
                    )
                    full_response = response.choices[0].message.content
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    # SAUVEGARDE DANS LES LOGS
                    now = datetime.datetime.now().strftime("%H:%M")
                    st.session_state.full_history.append({
                        "time": now,
                        "query": prompt[:20] + "...",
                        "code": full_response
                    })
                    
                    if rank == "FREE":
                        st.session_state.credits -= 1
                    
                    st.rerun() # Obligatoire pour rafraîchir les onglets et crédits
                        
                except Exception as e:
                    st.error(f"SYSTEM ERROR: {e}")
