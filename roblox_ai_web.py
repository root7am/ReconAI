import streamlit as st
import openai

# Configuration de la page
st.set_page_config(page_title="Roblox Script Master AI", page_icon="🎮")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #1e1e1e; color: white; }
    .stTextInput textarea { color: #00ff00 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE (CONFIG) ---
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Entre ta clé API OpenAI :", type="password")
    model_choice = st.selectbox("Modèle", ["gpt-4o", "gpt-3.5-turbo"])
    st.info("Cette IA est spécialisée en Luau et API Roblox.")

# --- LOGIQUE DE L'IA ---
def generate_roblox_script(prompt):
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """
    Tu es RobloxDev-GPT. 
    1. Réponds EXCLUSIVEMENT en Luau (Roblox).
    2. Utilise 'task.wait()' et non 'wait()'.
    3. Explique TOUJOURS où placer le script dans l'explorateur Roblox Studio.
    4. Si l'utilisateur demande un GUI, donne les propriétés des instances.
    """
    
    response = client.chat.completions.create(
        model=model_choice,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# --- INTERFACE WEB ---
st.title("🎮 Roblox Script Master AI")
st.subheader("Génère tes scripts Luau en un clic")

user_input = st.text_area("Décris le système que tu veux (ex: Un système de vente d'objets) :", height=150)

if st.button("Générer le code"):
    if not api_key:
        st.error("⚠️ Tu dois entrer une clé API dans la barre latérale !")
    elif user_input:
        with st.spinner("L'IA réfléchit au meilleur code..."):
            try:
                result = generate_roblox_script(user_input)
                st.markdown("### 📜 Résultat :")
                st.code(result, language="lua")
                st.success("Code généré ! Copie-le dans Roblox Studio.")
            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.warning("Écris quelque chose avant de valider.")