import streamlit as st
import random
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from data.test_questions import DEGEN_TYPES
from config.settings import DAILY_MISSIONS, XP_LEVELS, USER_AVATARS
from data.lessons import load_lessons
from utils.goals import get_user_goals, calculate_goal_metrics
from utils.daily_missions import get_daily_missions_progress
from views.degen_test import plot_radar_chart
from utils.components import (
    zen_header, mission_card, degen_card, progress_bar, stat_card, 
    xp_level_display, zen_button, notification, leaderboard_item, 
    add_animations_css, data_chart, user_stats_panel
)

def calculate_xp_progress(user_data):
    """Calculate XP progress and dynamically determine the user's level"""
    # Dynamically determine the user's level based on XP
    for level, xp_threshold in sorted(XP_LEVELS.items(), reverse=True):
        if user_data['xp'] >= xp_threshold:
            user_data['level'] = level
            break

    # Calculate progress to the next level
    next_level = user_data['level'] + 1
    if next_level in XP_LEVELS:
        current_level_xp = XP_LEVELS[user_data['level']]
        next_level_xp = XP_LEVELS[next_level]
        xp_needed = next_level_xp - current_level_xp
        xp_progress = user_data['xp'] - current_level_xp
        xp_percentage = min(100, int((xp_progress / xp_needed) * 100))
        return xp_percentage, xp_needed - xp_progress

    return 100, 0

def get_top_users(limit=5):
    """Get top users by XP"""
    users_data = load_user_data()
    leaderboard = []
    
    for username, data in users_data.items():
        leaderboard.append({
            'username': username,
            'level': data.get('level', 1),
            'xp': data.get('xp', 0)
        })
    
    # Sort by XP (descending)
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    return leaderboard[:limit]

def get_user_rank(username):
    """Get user rank in the leaderboard"""
    users_data = load_user_data()
    leaderboard = []
    
    for user, data in users_data.items():
        leaderboard.append({
            'username': user,
            'xp': data.get('xp', 0)
        })
    
    # Sort by XP (descending)
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    
    # Find user rank
    for i, user in enumerate(leaderboard):
        if user['username'] == username:
            return {'rank': i + 1, 'xp': user['xp']}
    
    return {'rank': 0, 'xp': 0}

def get_user_xp_history(username, days=30):
    """Simulate XP history data (for now)"""
    # This would normally come from a database
    # For now, we'll generate fictional data
    history = []
    today = datetime.now()
    
    # Generate data points for the last X days
    xp = load_user_data().get(username, {}).get('xp', 0)
    daily_increment = max(1, int(xp / days))
    
    for i in range(days):
        date = today - timedelta(days=days-i)
        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'xp': max(0, int(xp * (i+1) / days))
        })
    
    return history

def display_lesson_cards(lessons_list, tab_name=""):
    """Display lesson cards in a grid layout
    
    Args:
        lessons_list: Dictionary of lessons to display
        tab_name: Name of the tab to use for creating unique button keys
    """
    if not lessons_list:
        st.info("Brak dostępnych lekcji w tej kategorii.")
        return
    
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    
    # Create a 2-column layout for lessons
    cols = st.columns(2)
    
    for i, (lesson_id, lesson) in enumerate(lessons_list.items()):
        # Get lesson properties
        difficulty = lesson.get('difficulty', 'intermediate')
        is_completed = lesson_id in user_data.get('completed_lessons', [])
        
        # Estimate reading time: average adult reads ~250 words per minute
        # We'll approximate based on content length (simplified)
        content_length = len(lesson.get('description', '')) + sum(len(section.get('content', '')) 
                                                                for section in lesson.get('sections', {}).get('learning', {}).get('sections', []))
        estimated_minutes = max(1, round(content_length / 1000))  # Rough estimate        # Color-code based on difficulty
        difficulty_class = f"degen-card-{difficulty.lower()}"
        difficulty_badge_class = f"badge-difficulty-{difficulty.lower()}"
        
        # Przygotuj symbol trudności
        if difficulty == "beginner":
            difficulty_symbol = "🟢"
        elif difficulty == "intermediate":
            difficulty_symbol = "🟠"
        else:
            difficulty_symbol = "🔴"
        
        with cols[i % 2]:
            degen_card(
                title=lesson['title'],
                description=lesson['description'][:100] + ('...' if len(lesson['description']) > 100 else ''),
                badges=[
                    {'text': f'💎 {lesson["xp_reward"]} XP', 'type': 'xp'},
                    {'text': f'{difficulty_symbol} {difficulty.capitalize()}', 'type': f'difficulty-{difficulty.lower()}'},
                    {'text': f'⏱️ {estimated_minutes} min', 'type': 'time'},
                    {'text': f'{lesson["tag"]}', 'type': 'tag'}
                ],
                status='completed' if is_completed else 'incomplete',
                status_text='✓ Ukończono' if is_completed else '○ Nieukończono'            )
            unique_key = f"{tab_name}_start_{lesson_id}_{i}"
            if zen_button(f"Rozpocznij", key=unique_key):
                st.session_state.current_lesson = lesson_id
                st.session_state.page = 'lesson'
                st.rerun()

def get_recommended_lessons(username):
    """Get recommended lessons based on user type"""
    lessons = load_lessons()
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    degen_type = user_data.get('degen_type', None)
    
    # If user has a degen type, filter lessons to match
    if degen_type:
        return {k: v for k, v in lessons.items() if v.get('recommended_for', None) == degen_type}
    
    # Otherwise, return a small selection of beginner lessons
    return {k: v for k, v in lessons.items() if v.get('difficulty', 'medium') == 'beginner'}

def get_popular_lessons():
    """Get most popular lessons based on completion count"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "popular"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def get_newest_lessons():
    """Get newest lessons"""
    # Dla symulanty, zwracamy standardowe lekcje z modyfikatorem "newest"
    # aby zapewnić unikalność kluczy lekcji między różnymi kategoriami
    lessons = load_lessons()
    return lessons

def get_daily_missions(username):
    """Get daily missions for user"""
    # For now, use the missions from settings
    # We're only showing the first 3 missions to the user
    return DAILY_MISSIONS[:3]

def show_dashboard():
    # Używamy naszego komponentu nagłówka
    zen_header("Dashboard Degena")
    
    # Dodajemy animacje CSS
    add_animations_css()

    users_data = load_user_data()
    user_data = users_data[st.session_state.username]

    # WIERSZ 1: Profil użytkownika i profil inwestycyjny w dwóch kolumnach
    st.markdown("<div class='st-bx fadeIn delay-1'>", unsafe_allow_html=True)
    profile_col, investor_profile_col = st.columns(2)
    
    # 1a. PROFIL UŻYTKOWNIKA (kolumna 1)
    with profile_col:
        st.subheader("Profil użytkownika")
        
        # Avatar i typ degena
        user_avatar = USER_AVATARS.get(user_data.get('avatar', 'default'), '👤')
        degen_type = user_data.get('degen_type', 'Nie określono')
        
        # Pasek postępu XP do następnego poziomu
        xp = user_data.get('xp', 0)
        xp_progress, xp_needed = calculate_xp_progress(user_data)
        next_level = user_data.get('level', 1) + 1
        next_level_xp = XP_LEVELS.get(next_level, xp + xp_needed)
        
        # Używamy komponentu user_stats_panel
        user_stats_panel(
            username=st.session_state.username,
            avatar=user_avatar,
            degen_type=degen_type,
            level=user_data.get('level', 1),
            xp=xp,
            completed_lessons=len(user_data.get('completed_lessons', [])),
            next_level_xp=next_level_xp
        )
    
    # 1b. PROFIL INWESTYCYJNY (kolumna 2)
    with investor_profile_col:
        st.subheader("Twój profil inwestycyjny")
        
        if 'test_scores' in user_data:
            radar_fig = plot_radar_chart(user_data['test_scores'])
            st.pyplot(radar_fig)
        elif not user_data.get('test_taken', False):
            st.info("Wykonaj test Degena, aby odkryć swój profil inwestycyjny")
            if zen_button("Wykonaj test Degena"):
                st.session_state.page = 'degen_test'
                st.rerun()
        else:
            st.info("Twój profil inwestycyjny jest jeszcze niekompletny")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # WIERSZ 2: Dostępne lekcje w pełnej szerokości
    st.markdown("<div class='st-bx fadeIn delay-2'>", unsafe_allow_html=True)
    st.subheader("Dostępne lekcje")
    lesson_tabs = st.tabs(["Polecane dla Ciebie", "Popularne", "Najnowsze"])
    
    with lesson_tabs[0]:
        display_lesson_cards(get_recommended_lessons(st.session_state.username), "recommended")
    
    with lesson_tabs[1]:
        display_lesson_cards(get_popular_lessons(), "popular")
    
    with lesson_tabs[2]:
        display_lesson_cards(get_newest_lessons(), "newest")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # WIERSZ 3: Misje dnia i ranking XP w dwóch kolumnach
    st.markdown("<div class='st-bx fadeIn delay-3'>", unsafe_allow_html=True)
    missions_col, leaderboard_col = st.columns([4, 3])
    
    # 3a. MISJE DNIA (kolumna 1)
    with missions_col:
        st.subheader("Misje dnia")
        
        # Get daily missions and progress
        daily_missions = get_daily_missions(st.session_state.username)
        missions_progress = get_daily_missions_progress(st.session_state.username)
        
        # Overall progress indicator
        progress_percentage = missions_progress['progress']
        
        # Add streak indicator
        streak = missions_progress['streak']
        streak_html = ""
        if streak > 0:
            streak_html = f"""
            <div class="streak-container">
                <div class="streak-badge">🔥 {streak} dni</div>
                <div class="streak-label">Twoja seria</div>
            </div>
            """
        
        # Show overall progress
        progress_bar(
            value=missions_progress['completed'],
            max_value=missions_progress['total'],
            label=f"Ukończono: {missions_progress['completed']}/{missions_progress['total']} ({int(progress_percentage)}%)"
        )
        
        if daily_missions:
            for mission in daily_missions:
                # Check if mission is completed
                is_completed = mission['title'] in missions_progress['completed_ids']
                
                # Używamy komponentu mission_card
                mission_card(
                    title=mission['title'], 
                    description=mission['description'], 
                    badge_emoji=mission['badge'], 
                    xp=mission['xp'],
                    progress=100 if is_completed else 0,
                    completed=is_completed
                )
                
                # Complete button (only if not completed)
                if not is_completed:
                    if zen_button("Ukończ misję", key=f"complete_{mission['title'].replace(' ', '_')}"):
                        from utils.daily_missions import complete_daily_mission
                        complete_success = complete_daily_mission(st.session_state.username, mission['title'])
                        
                        if complete_success:
                            # Create a success message
                            notification(f"Misja '{mission['title']}' została ukończona! +{mission['xp']} XP", type="success")
                            st.rerun()
                
            if zen_button("Odśwież misje", key="refresh_missions"):
                st.rerun()
        else:
            st.info("Nie masz dostępnych misji na dziś.")
    
    # 3b. RANKING XP (kolumna 2)
    with leaderboard_col:
        st.subheader("Ranking XP")
        
        # Pobierz najlepszych graczy
        top_users = get_top_users(5)  # Top 5 użytkowników
        
        for i, user in enumerate(top_users):
            leaderboard_item(
                rank=i+1,
                username=user['username'],
                points=user['xp'],
                is_current_user=user['username'] == st.session_state.username
            )
        
        # Pozycja bieżącego użytkownika
        current_user_rank = get_user_rank(st.session_state.username)
        
        # Wyświetl pozycję użytkownika tylko jeśli nie jest w top 5
        if current_user_rank['rank'] > 5:
            st.markdown("---")
            leaderboard_item(
                rank=current_user_rank['rank'],
                username=st.session_state.username,
                points=current_user_rank['xp'],
                is_current_user=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # WIERSZ 4: Wykres postępu
    st.markdown("<div class='st-bx fadeIn delay-4'>", unsafe_allow_html=True)
    progress_col, empty_col = st.columns(2)
    
    # 4a. WYKRES POSTĘPU
    with progress_col:
        st.subheader("Twój postęp")
        
        # Wykres trendu XP przy użyciu komponentu data_chart
        history = get_user_xp_history(st.session_state.username)
        if history:
            chart_data = pd.DataFrame(history)
            data_chart(
                data=chart_data,
                chart_type="area",
                title="Rozwój XP w czasie",
                x_label="Data",
                y_label="Punkty XP",
                height=300
            )
        else:
            st.info("Brak danych o historii XP. Zacznij swój pierwszy kurs!")
    
    st.markdown("</div>", unsafe_allow_html=True)