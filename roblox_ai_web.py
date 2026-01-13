import streamlit as st
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="ReconAI - Rank System", page_icon="👑")

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTextArea textarea { background-color: #161b22; color: #00ff00; border: 1px solid #30363d; }
    .owner-text { color: #ff4b4b; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURATION GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Clé GROQ_API_KEY manquante !")

# --- SYSTÈME DE RANK ---
with st.sidebar:
    st.title("👤 Profil Utilisateur")
    user_key = st.text_input("Entre ton code d'accès :", type="password")
    
    # Définition du Rank
    if user_key == "OWNER_RECON_2026": # C'est ton code secret !
        rank = "OWNER"
        st.markdown("<p class='owner-text'>RANK: OWNER (ILLIMITÉ)</p>", unsafe_allow_html=True)
    elif user_key == "FRIEND":
        rank = "PREMIUM"
        st.info("RANK: PREMIUM")
    else:
        rank = "FREE"
        st.warning("RANK: FREE (Limité)")

def generate_roblox_script(prompt):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Tu es ReconAI, expert Roblox. Réponds en Luau."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# --- INTERFACE PRINCIPALE ---
st.title("🤖 ReconAI Assistant")

if rank == "OWNER":
    st.success("Bienvenue Maître. Vos crédits sont infinis.")
else:
    st.write("Mode gratuit activé.")

user_input = st.text_area("Décris ton script Roblox :", height=150)

if st.button("🚀 Générer le Script"):
    if rank == "FREE" and len(user_input) > 100:
        st.error("❌ Ton texte est trop long pour le mode FREE. Passe en OWNER !")
    elif user_input:
        with st.spinner("Génération en cours..."):
            try:
                result = generate_roblox_script(user_input)
                st.code(result, language="lua")
            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.warning("Écris quelque chose !")
