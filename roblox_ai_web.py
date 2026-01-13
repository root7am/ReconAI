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
    /* Fond global */
    .stApp { background-color: #050505; color: #e0e0e0; }
    
    /* Bandeau de Crédits en haut */
    .credit-header {
        background: rgba(15, 15, 15, 0.95);
        border: 1px solid #1f1f1f;
        padding: 15px 25px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 25px;
        border-left: 5px solid #ff4b4b;
    }
    .user-avatar {
        width: 55px;
        height: 55px;
        border-radius: 50%;
        border: 2px solid #ff4b4b;
        object-fit: cover;
    }
    .credit-amount { color: #ff4b4b; font-weight: bold; font-size: 1.3rem; }
    .owner-badge { color: #ff4b4b; border: 1px solid #ff4b4b; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; }
    
    /* Sidebar et Logs */
    [data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #1f1f1f; }
    .log-section-title {
        color: #ff4b4b;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #1f1f1f;
        padding-bottom: 5px;
    }
    
    /* Bulles de Chat */
    .stChatMessage { 
        background-color: #0d0d0d !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 10px !important;
    }
    code { color: #00ff88 !important; }
    </style>
    """, unsafe_allow_html=True)


try:
    
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("ERREUR : GROQ_API_KEY non configurée.")


with st.sidebar:
    st.title("📡 RECON HUB")
    
   
    st.subheader("🔑 ACCÈS SYSTÈME")
    access_code = st.text_input("Saisir code :", type="password")
    
    
    if access_code == "OWNER_RECON_2026":
        rank, user_name, credits_val = "OWNER", "RECON_ROOT", "∞"
    else:
        rank, user_name, credits_val = "FREE", "CIVILIAN", str(st.session_state.credits)

    
    st.markdown('<div class="log-section-title">📜 LOGS DE SESSION</div>', unsafe_allow_html=True)
    
    if not st.session_state.full_history:
        st.caption("En attente de données...")
    else:
        for i, log in enumerate(reversed(st.session_state.full_history)):
            with st.expander(f"🕒 {log['time']} | {log['query']}"):
                st.code(log['code'], language="lua")

    st.divider()
    
    
    if st.checkbox("🛒 VOIR LA BOUTIQUE"):
        st.info("💠 PREMIUM: 4.99€/m (500 crédits)\n👑 OWNER: 14.99€ (À VIE - ILLIMITÉ)")
        st.button("Commander via PayPal", use_container_width=True)

    if st.button("🗑️ RESET SESSION"):
        st.session_state.messages = []
        st.rerun()


custom_avatar = "https://cdn-icons-png.flaticon.com/512/6033/6033716.png" 

st.markdown(f"""
    <div class="credit-header">
        <div class="user-info" style="display:flex; align-items:center; gap:15px;">
            <img src="{custom_avatar}" class="user-avatar">
            <div>
                <div style="font-weight: bold; font-size: 1.1rem;">{user_name}</div>
                <span class="owner-badge">{rank} ACCESS</span>
            </div>
        </div>
        <div class="stat-box" style="text-align:right;">
            <div style="font-size: 0.75rem; color: #666;">CRÉDITS DISPONIBLES</div>
            <div class="credit-amount">{credits_val}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Initialisation de la commande..."):
    
    if rank == "FREE" and st.session_state.credits <= 0:
        st.error("❌ CRÉDITS ÉPUISÉS. Passez en mode OWNER pour continuer.")
    else:
        # Enregistrement utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Réponse IA
        with st.chat_message("assistant"):
            with st.spinner("TRAITEMENT EN COURS..."):
                try:
                    # Modèle Llama 3.3 via Groq
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Tu es ReconAI. Expert Roblox Luau. Réponds en Luau technique."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        ]
                    )
                    
                    response = completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Mise à jour des Logs et Crédits
                    now = datetime.datetime.now().strftime("%H:%M")
                    st.session_state.full_history.append({
                        "time": now,
                        "query": prompt[:20] + "...",
                        "code": response
                    })
                    
                    if rank == "FREE":
                        st.session_state.credits -= 1
                    
                    st.rerun() # Rafraîchissement pour les logs et crédits
                        
                except Exception as e:
                    st.error(f"ERREUR SYSTÈME : {e}")
