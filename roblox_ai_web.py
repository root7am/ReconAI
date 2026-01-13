import streamlit as st
from groq import Groq


st.set_page_config(page_title="ReconAI - Rank & History", page_icon="👑")


if "history" not in st.session_state:
    st.session_state.history = []


st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextArea textarea { background-color: #161b22; color: #00ff00; border: 1px solid #30363d; }
    .owner-text { color: #ff4b4b; font-weight: bold; font-size: 20px; }
    .history-item { padding: 10px; border-bottom: 1px solid #30363d; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)


try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Clé GROQ_API_KEY manquante dans les Secrets !")


with st.sidebar:
    st.title("👤 Profil & Logs")
    user_key = st.text_input("Entre ton code d'accès :", type="password")
    
    if user_key == "OWNER_RECON_2026":
        rank = "OWNER"
        st.markdown("<p class='owner-text'>RANK: OWNER (ILLIMITÉ)</p>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("📜 Historique des Scripts")
        if not st.session_state.history:
            st.write("Aucun script dans cette session.")
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Script {len(st.session_state.history)-i}: {item['title']}"):
                st.code(item['code'], language="lua")
    else:
        rank = "FREE"
        st.warning("RANK: FREE")

def generate_roblox_script(prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Tu es ReconAI, expert Roblox. Réponds en Luau."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


st.title("🤖 ReconAI Assistant")

user_input = st.text_area("Décris ton script Roblox :", height=150)

if st.button("🚀 Générer le Script"):
    if user_input:
        with st.spinner("Génération en cours..."):
            try:
                result = generate_roblox_script(user_input)
                st.code(result, language="lua")
                
                
                st.session_state.history.append({
                    "title": user_input[:30] + "...",
                    "code": result
                })
                
            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.warning("Écris quelque chose !")
