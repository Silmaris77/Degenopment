import streamlit as st
from utils.components import stat_card, xp_level_display

def user_stats_panel(username, avatar, degen_type, level, xp, completed_lessons=None, next_level_xp=None):
    """
    Tworzy panel z podstawowymi statystykami użytkownika.
    
    Parametry:
    - username: Nazwa użytkownika
    - avatar: Emoji awatara użytkownika
    - degen_type: Typ Degena użytkownika
    - level: Aktualny poziom użytkownika
    - xp: Aktualna ilość punktów XP
    - completed_lessons: Lista ukończonych lekcji (opcjonalna)
    - next_level_xp: Wymagane XP do następnego poziomu (opcjonalne)
    """
    
    # Avatar i informacje podstawowe
    st.markdown(f"""
    <div class="user-panel">
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 5rem; margin-bottom: 10px;">{avatar}</div>
            <div style="font-weight: bold; font-size: 1.2rem;">{username}</div>
            <div style="color: #888;">{degen_type}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statystyki w trzech kolumnach
    stats_cols = st.columns(3)
    
    with stats_cols[0]:
        stat_card("Poziom", level, icon="🏆")
    
    with stats_cols[1]:
        stat_card("XP", xp, icon="💎")
    
    with stats_cols[2]:
        if completed_lessons is not None:
            completed_count = len(completed_lessons) if isinstance(completed_lessons, list) else completed_lessons
            stat_card("Ukończone lekcje", completed_count, icon="📚")
    
    # Pasek postępu XP do następnego poziomu
    if next_level_xp is not None:
        xp_level_display(xp=xp, level=level, next_level_xp=next_level_xp)
