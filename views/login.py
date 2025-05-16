import streamlit as st
from data.users import register_user, login_user
from utils.components import zen_header, notification, zen_button, add_animations_css
from PIL import Image
import os
import base64

# Funkcja do konwersji obrazu na Base64
def img_to_base64(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

# Ścieżka do logo
logo_path = os.path.join("assets", "images", "zen_degen_logo.png")
logo_base64 = img_to_base64(logo_path)

def show_login_page():
    # Dodaj CSS dla układu split-screen
    

    # Główny kontener
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Logo z lokalnego pliku
    from PIL import Image
    import os
    import base64

    # Funkcja do konwersji obrazu na Base64
    def img_to_base64(img_path):
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        return ""

    # Ścieżka do logo
    logo_path = os.path.join("assets", "images", "zen_degen_logo.png")
    logo_base64 = img_to_base64(logo_path)

    if logo_base64:
        st.markdown(f"""
        <div class="zen-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="Zen Degen Academy">
            <div class="logo-glow"></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Jeśli nie znaleziono pliku, wyświetl samo nazwę
        st.markdown("""
        <div class="zen-logo">
            <h1>Zen Degen Academy</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Nagłówek z podtytułem
    st.markdown("""
    <div class="login-header">
        <p>Witaj w społeczności Zen Degen Academy</p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">Zaloguj się do swojego konta lub utwórz nowe</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Zakładki logowania/rejestracji z ulepszonymi etykietami
    tab1, tab2 = st.tabs([
        "📝 Logowanie", 
        "✨ Rejestracja"
    ])
    
    # Zakładka logowania
    with tab1:
        # Nazwa użytkownika z ikoną
        st.markdown('<div class="input-with-icon"><span class="input-icon">👤</span></div>', unsafe_allow_html=True)
        username = st.text_input("Nazwa użytkownika", key="login_username")
        
        # Hasło z ikoną
        st.markdown('<div class="input-with-icon"><span class="input-icon">🔒</span></div>', unsafe_allow_html=True)
        password = st.text_input("Hasło", type="password", key="login_password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.checkbox("Zapamiętaj mnie", key="remember_me")
        with col2:
            st.markdown('<div style="text-align: right;"><a href="#">Zapomniałem hasła</a></div>', unsafe_allow_html=True)
        
        # Dodajemy animowaną klasę do przycisku (efekt jest dodawany przez CSS)
        if zen_button("Zaloguj się", key="login_button"):
            success = login_user(username, password)
            if success:
                st.session_state.username = username
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Błędna nazwa użytkownika lub hasło.")
        
        # Ulepszone przyciski logowania społecznościowego
        st.markdown("""
        <div class="social-login">
            <a href="#" class="social-btn" title="Google"><i class="fab fa-google"></i></a>
            <a href="#" class="social-btn" title="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social-btn" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
        </div>
        <div style="text-align: center; margin-top: 10px; font-size: 0.9rem; color: rgba(255,255,255,0.6);">
            Zaloguj się za pomocą konta społecznościowego
        </div>
        """, unsafe_allow_html=True)
        

    
    # Zakładka rejestracji
    with tab2:
        # Nazwa użytkownika z ikoną
        st.markdown('<div class="input-with-icon"><span class="input-icon">👤</span></div>', unsafe_allow_html=True)
        new_username = st.text_input("Nazwa użytkownika", key="register_username")
        
        # Email z ikoną
        st.markdown('<div class="input-with-icon"><span class="input-icon">📧</span></div>', unsafe_allow_html=True)
        email = st.text_input("Email", key="register_email")
        
        # Hasło z ikoną
        st.markdown('<div class="input-with-icon"><span class="input-icon">🔒</span></div>', unsafe_allow_html=True)
        new_password = st.text_input("Hasło", type="password", key="register_password")
        
        # Potwierdzenie hasła z ikoną
        st.markdown('<div class="input-with-icon"><span class="input-icon">🔐</span></div>', unsafe_allow_html=True)
        confirm_password = st.text_input("Potwierdź hasło", type="password", key="confirm_password")
        
        # Ulepszony checkbox z warunkami
        col1, col2 = st.columns([1, 3])
        with col1:
            accept_terms = st.checkbox("", key="accept_terms")
        with col2:
            st.markdown('<div style="margin-top: 8px;">Akceptuję <a href="#">regulamin</a> i <a href="#">politykę prywatności</a></div>', unsafe_allow_html=True)
        
        # Przycisk z animacją (efekt jest dodawany przez CSS)
        if zen_button("Zarejestruj się", key="register_button"):
            if new_password != confirm_password:
                st.error("Hasła nie są identyczne.")
            elif not accept_terms:
                st.error("Musisz zaakceptować regulamin i politykę prywatności.")
            else:
                success = register_user(new_username, new_password, email)
                if success:
                    notification("Konto zostało utworzone! Możesz się zalogować.", type="success")
                    # Przełącz na zakładkę logowania
                    st.rerun()
                else:
                    st.error("Nazwa użytkownika jest już zajęta.")
        
        # Informacja o szybkiej rejestracji
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 1rem;">
                Szybka rejestracja przez media społecznościowe
            </div>
            <div class="social-login">
                <a href="#" class="social-btn" title="Google"><i class="fab fa-google"></i></a>
                <a href="#" class="social-btn" title="Facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="#" class="social-btn" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Zamknięcie kontenera
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dodajemy efekty cząsteczek w tle za pomocą JavaScript
    st.markdown("""
    <script>
    // Kod JavaScript do dodania w przyszłości - obecnie Streamlit blokuje takie skrypty
    </script>
    """, unsafe_allow_html=True)

    # Tworzenie katalogu na obrazy, jeśli nie istnieje
    os.makedirs(r"c:\Users\Anna\Dropbox\Maverick\DegApp\degenopment_roboczy\assets\images", exist_ok=True)
    
    st.markdown("""
    <style>
    .login-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .login-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    </style>
    <div class="login-card">
        <!-- Formularz logowania -->
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
.form-container {
    position: relative;
    min-height: 400px;
}
.form {
    position: absolute;
    width: 100%;
    transition: all 0.5s ease-in-out;
}
.login-form {
    opacity: 1;
    transform: translateX(0);
}
.register-form {
    opacity: 0;
    transform: translateX(50px);
    pointer-events: none;
}
.show-register .login-form {
    opacity: 0;
    transform: translateX(-50px);
    pointer-events: none;
}
.show-register .register-form {
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
}
</style>
""", unsafe_allow_html=True)

    # W JavaScript (dodaj na końcu strony)
    st.markdown("""
<script>
function toggleForms() {
    document.querySelector('.form-container').classList.toggle('show-register');
}
</script>
""", unsafe_allow_html=True)
