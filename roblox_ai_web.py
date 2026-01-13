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
    
    /* Bandeau de Crédits */
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
    
    /* Boutique VIP */
    .vip-card {
        background: #0d0d0d;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .vip-card:hover { border-color: #ff4b4b; background: #111; }
    .price { color: #ff4b4b; font-weight: bold; font-size: 1.1rem; }
    .benefit { font-size: 0.85rem; color: #aaa; margin-top: 5px; }
    
    .owner-badge { color: #ff4b4b; border: 1px solid #ff4b4b; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }
    </style>
    """, unsafe_allow_html=True)


try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY manquante.")


with st.sidebar:
    st.title("📡 RECON HUB")
    
   
    tab_acc, tab_shop = st.tabs(["🔑 ACCÈS", "🛒 BOUTIQUE VIP"])
    
    with tab_acc:
        access_code = st.text_input("Code secret :", type="password")
        if access_code == "OWNER_RECON_2026":
            rank = "OWNER"
            user_name = "RECON_ROOT"
            credits_val = "∞"
        else:
            rank = "FREE"
            user_name = "CIVILIAN"
            credits_val = str(st.session_state.credits)
            
        st.divider()
        st.subheader("📜 LOGS")
        for log in reversed(st.session_state.full_history):
            with st.expander(f"{log['time']} - {log['query']}"):
                st.code(log['code'], language="lua")

    with tab_shop:
        st.subheader("Améliore ton Rank")
        
        
        st.markdown("""
        <div class="vip-card">
            <div style="font-weight:bold;">💠 RANK PREMIUM</div>
            <div class="price">4.99€ / mois</div>
            <div class="benefit">• 500 Crédits / mois<br>• Accès au modèle Llama 3.3<br>• Support prioritaire</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("S'abonner au PREMIUM", use_container_width=True):
            st.link_button("Payer via Stripe/PayPal", "https://ton-lien-de-paiement.com")

        
        st.markdown("""
        <div class="vip-card">
            <div style="font-weight:bold; color:#ff4b4b;">👑 RANK OWNER</div>
            <div class="price">14.99€ (À VIE)</div>
            <div class="benefit">• Crédits ILLIMITÉS<br>• Historique de session infini<br>• Pas de limite de texte</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acheter le GRADE OWNER", use_container_width=True):
            st.link_button("Payer via Stripe/PayPal", "https://ton-lien-de-paiement.com")


custom_avatar = "https://cdn-icons-png.flaticon.com/512/6033/6033716.png"
st.markdown(f"""
    <div class="credit-header">
        <div class="user-info">
            <img src="{custom_avatar}" class="user-avatar">
            <div>
                <div style="font-weight: bold;">{user_name}</div>
                <span class="owner-badge">{rank} ACCESS</span>
            </div>
        </div>
        <div class="stat-box">
            <div style="font-size: 0.7rem; color: #666;">CRÉDITS RESTANTS</div>
            <div class="credit-amount">{credits_val}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Initialisation..."):
    
    if rank == "FREE" and st.session_state.credits <= 0:
        st.error("❌ CRÉDITS ÉPUISÉS (0/5). Achète un Rank ou entre ton code d'accès.")
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
                            {"role": "system", "content": "Tu es ReconAI. Expert Roblox Luau."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        ]
                    )
                    full_response = response.choices[0].message.content
                    st.markdown(full_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
                    # Logique de consommation et historique
                    now = datetime.datetime.now().strftime("%H:%M")
                    st.session_state.full_history.append({"time": now, "query": prompt[:20], "code": full_response})
                    
                    if rank == "FREE":
                        st.session_state.credits -= 1  # Consomme 1 crédit
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"SYSTEM ERROR: {e}")
