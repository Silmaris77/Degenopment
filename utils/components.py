import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import random

# Komponenty kart

def degen_card(title, description, icon=None, badge=None, badges=None, progress=None, button_text=None, button_action=None, status_text=None, color=None, background=None, status=None):
    """
    Wyświetla kartę z tytułem, opisem i opcjonalnie ikoną, odznaką i paskiem postępu.
    
    Parametry:
    - title: Tytuł karty
    - description: Opis zawartości
    - icon: Emoji lub ikona (opcjonalne)
    - badge: Treść odznaki (opcjonalne)
    - badges: Lista odznak (opcjonalne) - alternatywa dla pojedynczej odznaki
      Może być listą stringów lub listą słowników {'text': '...', 'type': '...'}
    - progress: Wartość procentowa postępu (opcjonalne)
    - button_text: Tekst przycisku (opcjonalne)
    - button_action: Funkcja wywoływana po kliknięciu przycisku (opcjonalne)
    - status_text: Tekst statusu (opcjonalne)
    - color: Kolor obramowania/akcentu (opcjonalne)
    - background: Kolor tła (opcjonalne)
    - status: Alias dla status_text (dla zgodności wstecznej)
    """
    # Utwórz unikalny klucz dla przycisku
    button_key = f"degen_card_{hash(title)}_{hash(description) if description else ''}_{random.randint(1000, 9999)}"
    
    # Obsłuż alias status -> status_text dla zgodności wstecznej
    if status is not None and status_text is None:
        status_text = status
    
    # Ustawienia stylu
    color_style = f"border-color: {color};" if color else ""
    bg_style = f"background-color: {background};" if background else ""
    
    # HTML struktury karty
    html = f"""
    <div class="degen-card" style="{color_style} {bg_style}">
        <div class="degen-card-header">
    """
    
    # Dodaj ikonę jeśli istnieje
    if icon:
        html += f'<div class="degen-card-icon">{icon}</div>'
    
    html += f'<div class="degen-card-title">{title}</div>'
    
    # Dodaj odznakę jeśli istnieje
    if badge:
        html += f'<div class="degen-card-badge">{badge}</div>'
    elif badges:
        # Obsługa wielu odznak
        badges_html = ""
        for b in badges:
            if isinstance(b, dict) and 'text' in b:
                badge_text = b['text']
                badge_type = b.get('type', '')
                badges_html += f'<span class="degen-card-badge-item badge-{badge_type}">{badge_text}</span> '
            else:
                badges_html += f'<span class="degen-card-badge-item">{b}</span> '
                
        html += f'<div class="degen-card-badges">{badges_html}</div>'
    
    html += """
        </div>
        <div class="degen-card-content">
    """
    
    # Dodaj opis jeśli istnieje
    if description:
        html += f'<div class="degen-card-description">{description}</div>'
    
    # Dodaj status jeśli istnieje
    if status_text:
        html += f'<div class="degen-card-status">{status_text}</div>'
    
    # Dodaj pasek postępu jeśli istnieje
    if progress is not None:
        html += f"""
        <div class="degen-card-progress-container">
            <div class="degen-card-progress-bar" style="width: {progress}%;"></div>
        </div>
        <div class="degen-card-progress-text">{progress}% ukończone</div>
        """
    
    html += """
        </div>
    </div>
    """
    
    # Wyświetl kartę
    st.markdown(html, unsafe_allow_html=True)
    
    # Dodaj przycisk jeśli istnieje
    if button_text:
        if zen_button(button_text, key=button_key):
            if button_action:
                button_action()

def mission_card(title, description, badge_emoji, xp, progress=0, completed=False):
    """
    Tworzy kartę misji z paskiem postępu.
    
    Parametry:
    - title: Tytuł misji
    - description: Opis misji
    - badge_emoji: Emoji odznaki
    - xp: Ilość punktów XP za ukończenie
    - progress: Postęp w procentach (0-100)
    - completed: Czy misja została ukończona
    """
    completed_class = "completed" if completed else ""
    
    mission_html = f"""
    <div class="mission-card {completed_class}">
        <div class="mission-header">
            <div class="mission-badge">{badge_emoji}</div>
            <div>
                <div class="mission-title">{title}</div>
                <div class="mission-desc">{description}</div>
            </div>
        </div>
        <div class="mission-progress-container">
            <div class="mission-progress-bar" style="width: {progress}%">{progress}%</div>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <span class="mission-xp">+{xp} XP</span>
        </div>
    </div>
    """
    
    st.markdown(mission_html, unsafe_allow_html=True)

def goal_card(title, description, end_date, progress=0, completed=False):
    """
    Tworzy kartę celu z paskiem postępu.
    
    Parametry:
    - title: Tytuł celu
    - description: Opis celu
    - end_date: Data ukończenia celu (str)
    - progress: Postęp w procentach (0-100)
    - completed: Czy cel został ukończony
    """
    completed_class = "completed" if completed else ""
    progress_color = "#27ae60" if completed else "#2980B9"
    
    goal_html = f"""
    <div class="goal-card {completed_class}">
        <div class="goal-header">
            <h4>{title}</h4>
            <div class="goal-date">{end_date}</div>
        </div>
        <p>{description}</p>
        <div class="goal-progress-container">
            <div class="goal-progress-bar" style="width: {progress}%; background-color: {progress_color}"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
            <span>{progress}% ukończone</span>
            <span>{end_date}</span>
        </div>
    </div>
    """
    
    st.markdown(goal_html, unsafe_allow_html=True)

def badge_card(icon, title, description, earned=False):
    """
    Tworzy kartę odznaki.
    
    Parametry:
    - icon: Emoji odznaki
    - title: Nazwa odznaki
    - description: Opis odznaki
    - earned: Czy odznaka została zdobyta
    """
    earned_class = "earned" if earned else "not-earned"
    opacity = "1.0" if earned else "0.5"
    
    badge_html = f"""
    <div class="badge-card {earned_class}" style="opacity: {opacity}">
        <div class="badge-icon">{icon}</div>
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)

# Komponenty przycisków i akcji

def zen_button(label, on_click=None, key=None, disabled=False, help=None, use_container_width=False):
    """
    Tworzy stylizowany przycisk Zen.
    
    Parametry:
    - label: Etykieta przycisku
    - on_click: Funkcja do wykonania po kliknięciu
    - key: Unikalny klucz przycisku
    - disabled: Czy przycisk jest wyłączony
    - help: Tekst pomocy pokazywany po najechaniu
    - use_container_width: Czy przycisk ma używać pełnej szerokości kontenera
    
    Zwraca:
    - Bool: True jeśli przycisk został kliknięty
    """
    return st.button(
        label, 
        on_click=on_click, 
        key=key, 
        disabled=disabled, 
        help=help, 
        use_container_width=use_container_width
    )

def notification(message, type="info"):
    """
    Wyświetla powiadomienie.
    
    Parametry:
    - message: Treść powiadomienia
    - type: Typ powiadomienia (info, success, warning, error)
    """
    if type == "info":
        st.info(message)
    elif type == "success":
        st.success(message)
    elif type == "warning":
        st.warning(message)
    elif type == "error":
        st.error(message)

# Komponenty nawigacyjne

def zen_header(title, subtitle=None):
    """
    Tworzy nagłówek dla strony.
    
    Parametry:
    - title: Tytuł strony
    - subtitle: Podtytuł (opcjonalny)
    """
    st.markdown(f"<h1 class='zen-header'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='zen-subtitle'>{subtitle}</p>", unsafe_allow_html=True)

def navigation_menu(items, current_page=None):
    """
    Tworzy menu nawigacyjne.
    
    Parametry:
    - items: Lista słowników z kluczami 'name', 'page', 'icon'
    - current_page: Obecnie aktywna strona
    """
    for item in items:
        icon = item.get('icon', '')
        label = f"{icon} {item['name']}"
        disabled = current_page == item['page']
        
        if zen_button(label, key=f"nav_{item['page']}", 
                    disabled=disabled, use_container_width=True):
            st.session_state.page = item['page']
            st.rerun()

# Komponenty statystyk i danych

def stat_card(label, value, icon=None, change=None, change_type=None):
    """
    Tworzy kartę statystyki.
    
    Parametry:
    - label: Etykieta statystyki
    - value: Wartość statystyki
    - icon: Emoji ikony
    - change: Zmiana wartości (z podanym znakiem)
    - change_type: Typ zmiany (positive, negative, neutral)
    """
    change_html = ""
    if change:
        change_color = "#27ae60" if change_type == "positive" else (
            "#e74c3c" if change_type == "negative" else "#7f8c8d")
        change_html = f'<span style="color: {change_color}; font-size: 12px;">({change})</span>'
    
    icon_html = f'<span style="font-size: 24px; margin-right: 10px;">{icon}</span>' if icon else ""
    
    stat_html = f"""
    <div style="background-color: white; border-radius: 10px; padding: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.08);">
        <div style="display: flex; align-items: center;">
            {icon_html}
            <div>
                <div style="color: #7f8c8d; font-size: 14px;">{label}</div>
                <div style="font-size: 24px; font-weight: bold; color: #2c3e50;">{value} {change_html}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(stat_html, unsafe_allow_html=True)

def progress_bar(value, max_value, label=None):
    """
    Tworzy pasek postępu.
    
    Parametry:
    - value: Obecna wartość
    - max_value: Maksymalna wartość
    - label: Etykieta (opcjonalnie)
    """
    progress_percent = min(100, int((value / max_value) * 100)) if max_value > 0 else 0
    
    label_html = f'<div style="margin-bottom: 5px;">{label}</div>' if label else ""
    
    progress_html = f"""
    {label_html}
    <div class="mission-progress-container">
        <div class="mission-progress-bar" style="width: {progress_percent}%">{progress_percent}%</div>
    </div>
    <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 12px; color: #7f8c8d;">
        <span>0</span>
        <span>{max_value}</span>
    </div>
    """
    
    st.markdown(progress_html, unsafe_allow_html=True)

def xp_level_display(xp, level, next_level_xp):
    """
    Wyświetla poziom XP użytkownika z paskiem postępu.
    
    Parametry:
    - xp: Obecna liczba punktów XP
    - level: Obecny poziom
    - next_level_xp: XP wymagane do następnego poziomu
    """
    previous_level_xp = 0  # Można dostosować na podstawie konfiguracji poziomów
    xp_progress = xp - previous_level_xp
    xp_needed = next_level_xp - previous_level_xp
    progress_percent = min(100, int((xp_progress / xp_needed) * 100)) if xp_needed > 0 else 0
    
    level_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <div style="background-color: #2980B9; color: white; width: 50px; height: 50px; border-radius: 50%; 
                  display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold;
                  margin-right: 15px;">{level}</div>
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-weight: bold;">Poziom {level}</span>
                <span>XP: {xp} / {next_level_xp}</span>
            </div>
            <div class="mission-progress-container">
                <div class="mission-progress-bar" style="width: {progress_percent}%"></div>
            </div>
            <div style="text-align: right; font-size: 12px; margin-top: 5px;">
                {xp_needed - xp_progress} XP do poziomu {level + 1}
            </div>
        </div>
    </div>
    """
    
    st.markdown(level_html, unsafe_allow_html=True)

# Komponenty treści edukacyjnych

def content_section(title, content, collapsed=False, icon=None, border_color=None):
    """
    Tworzy sekcję treści z możliwością zwijania.
    
    Parametry:
    - title: Tytuł sekcji
    - content: Zawartość sekcji (HTML lub markdown)
    - collapsed: Czy sekcja ma być domyślnie zwinięta
    - icon: Ikona (emoji) wyświetlana przed tytułem
    - border_color: Kolor obramowania sekcji (np. "#27ae60")
    """
    icon_html = f"{icon} " if icon else ""
    title_with_icon = f"{icon_html}{title}"
    
    with st.expander(title_with_icon, expanded=not collapsed):
        if border_color:
            st.markdown(f'<div style="border-left: 4px solid {border_color}; padding-left: 10px;">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(content, unsafe_allow_html=True)

def quote_block(text, author=None):
    """
    Tworzy blok cytatu.
    
    Parametry:
    - text: Tekst cytatu
    - author: Autor cytatu (opcjonalnie)
    """
    author_html = f'<div style="text-align: right; font-style: italic;">— {author}</div>' if author else ""
    
    quote_html = f"""
    <div style="background-color: #f8f9fa; border-left: 4px solid #2980B9; padding: 15px; margin: 15px 0; border-radius: 0 5px 5px 0;">
        <div style="font-style: italic; font-size: 16px;">{text}</div>
        {author_html}
    </div>
    """
    
    st.markdown(quote_html, unsafe_allow_html=True)

def tip_block(text, type="tip", title=None, icon=None):
    """
    Tworzy blok ze wskazówką, ostrzeżeniem lub informacją.
    
    Parametry:
    - text: Tekst wskazówki
    - type: Typ bloku (tip, warning, info)
    - title: Opcjonalny tytuł bloku
    - icon: Niestandardowa ikona (zastępuje domyślną ikonę)
    """
    default_icon = "💡" if type == "tip" else ("⚠️" if type == "warning" else "ℹ️")
    background = "#e3f4eb" if type == "tip" else ("#fef7e6" if type == "warning" else "#e6f3fc")
    border = "#27ae60" if type == "tip" else ("#f39c12" if type == "warning" else "#3498db")
    
    # Użyj niestandardowej ikony, jeśli podana, w przeciwnym razie użyj domyślnej
    display_icon = icon if icon else default_icon
    
    # Dodaj tytuł, jeśli jest podany
    title_html = f'<div style="font-weight: bold; margin-bottom: 8px;">{title}</div>' if title else ""
    
    tip_html = f"""
    <div style="background-color: {background}; border-left: 4px solid {border}; padding: 15px; margin: 15px 0; border-radius: 0 5px 5px 0;">
        <div style="display: flex; align-items: flex-start;">
            <span style="font-size: 24px; margin-right: 10px;">{display_icon}</span>
            <div>
                {title_html}
                <div>{text}</div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(tip_html, unsafe_allow_html=True)

def leaderboard_item(rank, username, points, is_current_user=False):
    """
    Tworzy element rankingu XP.
    
    Parametry:
    - rank: Pozycja w rankingu
    - username: Nazwa użytkownika
    - points: Liczba punktów XP
    - is_current_user: Czy element dotyczy bieżącego użytkownika
    """
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
    bg_color = "#f0f7fb" if is_current_user else "#ffffff"
    border = "2px solid #2980B9" if is_current_user else "1px solid #f0f0f0"
    
    leaderboard_html = f"""    <div style="display: flex; align-items: center; margin-bottom: 8px; padding: 10px; 
               border-radius: 8px; background-color: {bg_color}; border: {border};">
        <div style="width: 30px; text-align: center; font-size: 16px;">{medal}</div>
        <div style="flex-grow: 1; padding-left: 10px; font-weight: {500 if is_current_user else 400};">
            {username}{" (Ty)" if is_current_user else ""}
        </div>
        <div style="font-weight: bold; color: #2980B9;">{points} XP</div>
    </div>
    """
    
    st.markdown(leaderboard_html, unsafe_allow_html=True)

def embed_content(url, width="100%", height="600px", title=None):
    """
    Tworzy osadzony element (iframe) dla interaktywnych treści.
    
    Parametry:
    - url: URL do osadzenia 
    - width: Szerokość elementu (domyślnie: '100%')
    - height: Wysokość elementu (domyślnie: '600px')
    - title: Opcjonalny tytuł nad osadzonym elementem
    """
    if title:
        st.subheader(title)
        
    embed_html = f"""
    <div style="margin: 15px 0;">
        <iframe src="{url}"
                width="{width}" height="{height}" 
                style="border:none; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" 
                allowfullscreen>
        </iframe>
    </div>
    """
    
    st.markdown(embed_html, unsafe_allow_html=True)

def add_animations_css():
    st.markdown("""
    <style>
    /* Animacje */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInRight {
        0% { opacity: 0; transform: translateX(30px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .fadeIn {
        animation: fadeIn 0.6s ease forwards;
    }
    .slideInRight {
        animation: slideInRight 0.5s ease forwards;
    }
    .pulse {
        animation: pulse 2s ease infinite;
    }
    .delay-1 {
        animation-delay: 0.1s;
    }
    .delay-2 {
        animation-delay: 0.2s;
    }
    .delay-3 {
        animation-delay: 0.3s;
    }
    .tab-content {
        animation: fadeIn 0.6s ease forwards;
    }
    
    /* Style dla odznak */
    .degen-card-badge-item {
        display: inline-block;
        margin-right: 5px;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        background-color: #f0f0f0;
        color: #666;
    }
    .badge-xp {
        background-color: #FFD700;
        color: #333;
    }
    .badge-difficulty-beginner {
        background-color: #27ae60;
        color: white;
    }
    .badge-difficulty-intermediate {
        background-color: #f39c12;
        color: white;
    }
    .badge-difficulty-advanced {
        background-color: #e74c3c;
        color: white;
    }
    .badge-time {
        background-color: #3498db;
        color: white;
    }
    .badge-tag {
        background-color: #9b59b6;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def data_chart(data, chart_type="bar", title=None, x_label=None, y_label=None, height=400):
    """
    Tworzy wykres na podstawie danych.
    
    Parametry:
    - data: Dane do wykresu (lista słowników lub pandas DataFrame)
    - chart_type: Typ wykresu ("bar", "line", "area", "pie")
    - title: Tytuł wykresu
    - x_label: Etykieta osi X
    - y_label: Etykieta osi Y
    - height: Wysokość wykresu w pikselach
    """
    if title:
        st.subheader(title)
    
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    if chart_type == "bar":
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X(data.columns[0], title=x_label or data.columns[0]),
            y=alt.Y(data.columns[1], title=y_label or data.columns[1])
        ).properties(height=height)
        st.altair_chart(chart, use_container_width=True)
    
    elif chart_type == "line":
        chart = alt.Chart(data).mark_line().encode(
            x=alt.X(data.columns[0], title=x_label or data.columns[0]),
            y=alt.Y(data.columns[1], title=y_label or data.columns[1])
        ).properties(height=height)
        st.altair_chart(chart, use_container_width=True)
    
    elif chart_type == "area":
        chart = alt.Chart(data).mark_area().encode(
            x=alt.X(data.columns[0], title=x_label or data.columns[0]),
            y=alt.Y(data.columns[1], title=y_label or data.columns[1])
        ).properties(height=height)
        st.altair_chart(chart, use_container_width=True)
    elif chart_type == "pie":
        # For pie charts, we use matplotlib
        fig, ax = plt.subplots()
        ax.pie(data[data.columns[1]], labels=data[data.columns[0]], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        if title:
            ax.set_title(title)
        st.pyplot(fig)

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
