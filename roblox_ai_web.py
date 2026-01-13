import streamlit as st
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="ReconAI - Chat GPT Mode", page_icon="💬")

# Initialisation de la mémoire du chat (Historique de session)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STYLE PERSONNALISÉ (MODE SOMBRE & CHAT) ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stChatFloatingInputContainer { background-color: #121212; }
    .owner-badge { 
        color: #ff4b4b; 
        background: #331111; 
        padding: 5px 10px; 
        border-radius: 5px; 
        font-weight: bold; 
        border: 1px solid #ff4b4b;
    }
    .stChatMessage { border-radius: 15px; }
    code { color: #00ff00 !important; }
    </style>
    """, unsafe_allow_html=True)


try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erreur : GROQ_API_KEY non trouvée dans les Secrets Streamlit.")


with st.sidebar:
    st.title("👤 Profil ReconAI")
    user_key = st.text_input("Code d'accès secret :", type="password")
    
    if user_key == "OWNER_RECON_2026":
        rank = "OWNER"
        st.markdown("<span class='owner-badge'>👑 RANK: OWNER</span>", unsafe_allow_html=True)
        st.write("✅ Accès illimité activé.")
        if st.button("🗑️ Effacer la discussion"):
            st.session_state.messages = []
            st.rerun()
    else:
        rank = "FREE"
        st.info("RANK: FREE (Limité à 6 messages)")

    st.divider()
    st.subheader("🤖 À propos")
    st.write("Modèle : Llama-3.3-70B")
    st.write("Spécialisation : Roblox Luau")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Pose ta question sur ton projet Roblox..."):
    
   
    if rank == "FREE" and len(st.session_state.messages) >= 12: 
        st.error("❌ Limite atteinte. Entre le code OWNER pour continuer à discuter.")
    else:
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        
        with st.chat_message("assistant"):
            with st.spinner("ReconAI réfléchit..."):
                try:
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system", 
                                "content": "Tu es ReconAI, une IA experte en Roblox Luau. Tu dois toujours fournir du code optimisé (task.wait, task.spawn) et expliquer précisément où placer les scripts dans Roblox Studio."
                            },
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        ],
                        temperature=0.7
                    )
                    full_response = response.choices[0].message.content
                    st.markdown(full_response)
                    
                    
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {e}")
