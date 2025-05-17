def show_shop():
    st.title("Sklep 🛒")
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Wirtualna waluta użytkownika
    degen_coins = user_data.get('degen_coins', 0)
    st.markdown(f"<div class='coin-display'>🪙 <span class='coin-amount'>{degen_coins}</span> DegenCoins</div>", unsafe_allow_html=True)
    
    # Kategorie produktów
    categories = st.tabs(["Awatary", "Tła", "Specjalne lekcje", "Boostery"])
    
    with categories[0]:
        # Awatary dostępne w sklepie
        avatars = [
            {"id": "diamond_degen", "name": "Diamond Degen", "icon": "💎", "price": 500, "owned": "diamond_degen" in user_data.get('owned_avatars', [])},
            {"id": "crypto_wizard", "name": "Crypto Wizard", "icon": "🧙", "price": 750, "owned": "crypto_wizard" in user_data.get('owned_avatars', [])},
            {"id": "moon_hunter", "name": "Moon Hunter", "icon": "🌕", "price": 1000, "owned": "moon_hunter" in user_data.get('owned_avatars', [])}
        ]
        
        # Wyświetl awatary w siatce
        cols = st.columns(3)
        for i, avatar in enumerate(avatars):
            with cols[i % 3]:
                if avatar["owned"]:
                    st.markdown(f"""
                    <div class="shop-item owned">
                        <div class="shop-item-icon">{avatar['icon']}</div>
                        <div class="shop-item-name">{avatar['name']}</div>
                        <div class="shop-item-status">Posiadasz</div>
                        <button class="shop-use-btn">Użyj</button>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="shop-item">
                        <div class="shop-item-icon">{avatar['icon']}</div>
                        <div class="shop-item-name">{avatar['name']}</div>
                        <div class="shop-item-price">🪙 {avatar['price']}</div>
                        <button class="shop-buy-btn">Kup</button>
                    </div>
                    """, unsafe_allow_html=True)