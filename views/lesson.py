import streamlit as st
from data.lessons import load_lessons
from data.users import load_user_data, save_user_data
from utils.components import zen_header, zen_button, notification, content_section, tip_block, quote_block, progress_bar, embed_content

def show_lesson():
    zen_header("Kurs Zen Degen Academy")

    lessons = load_lessons()
    lesson_id = st.session_state.get('current_lesson')

    if not lesson_id or lesson_id not in lessons:
        st.error("Nie znaleziono wybranej lekcji.")
        return

    lesson = lessons[lesson_id]

    if 'lesson_step' not in st.session_state:
        st.session_state.lesson_step = 'intro'
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    # Lesson navigation in sidebar
    with st.sidebar:
        st.markdown("<h3>Nawigacja lekcji</h3>", unsafe_allow_html=True)

        # Define all lesson steps
        lesson_steps = {
            'intro': 'Wprowadzenie',
            'content': 'Merytoryka',
            'reflection': 'Refleksja i Praktyka',
            'application': 'Implementacja',
            'summary': 'Podsumowanie'        }        
        # Create navigation buttons
        for step, name in lesson_steps.items():
            if zen_button(
                name, 
                key=f"nav_{step}",
                disabled=st.session_state.lesson_step == step,
                use_container_width=True
            ):
                st.session_state.lesson_step = step
                st.rerun()

        if zen_button("Powrót do dashboard", use_container_width=True):
            st.session_state.lesson_step = 'intro'
            st.session_state.page = 'dashboard'
            st.rerun()
            
    # Main content
    st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
    
    # Main content logic for each step
    if st.session_state.lesson_step == 'intro':
        content_section("Wprowadzenie", lesson["intro"], collapsed=False)

    elif st.session_state.lesson_step == 'content':
        for section in lesson["sections"]["learning"]["sections"]:
            content_section(
                section["title"], 
                section["content"], 
                collapsed=True  # Zmiana z False na True, aby sekcje były domyślnie zwinięte
            )
            
    elif st.session_state.lesson_step == 'reflection':
        for section in lesson["sections"]["reflection"]["sections"]:
            # Use the new embed_content component
            embed_content(
                url="https://www.canva.com/design/DAGElemhrt0/-yw2s6fJnKLvyKvz1NDuTA/view?embed",
                width="1200",
                height="800",
                title=section["title"]
            )
            
    elif st.session_state.lesson_step == 'summary':
        total_xp = st.session_state.quiz_score + lesson["xp_reward"]

        users_data = load_user_data()
        user_data = users_data[st.session_state.username]

        if lesson_id not in user_data.get('completed_lessons', []):
            user_data['xp'] = user_data.get('xp', 0) + total_xp
            if 'completed_lessons' not in user_data:
                user_data['completed_lessons'] = []            
                user_data['completed_lessons'].append(lesson_id)
            users_data[st.session_state.username] = user_data
            save_user_data(users_data)

            notification(f"""
            🎉 Gratulacje! Ukończyłeś lekcję!

            Zdobyte punkty:
            - Quiz: {st.session_state.quiz_score} XP
            - Ukończenie lekcji: {lesson["xp_reward"]} XP
            - Łącznie: {total_xp} XP
            """, type="success")

        if zen_button("Powrót do dashboardu"):
            st.session_state.lesson_step = 'intro'
            st.session_state.current_quiz_step = 0
            st.session_state.closing_quiz_step = 0
            st.session_state.quiz_score = 0
            st.session_state.page = 'dashboard'
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)