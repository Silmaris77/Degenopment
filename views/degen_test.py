import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
from data.test_questions import DEGEN_TYPES, TEST_QUESTIONS
from data.users import load_user_data, save_user_data
from data.degen_details import degen_details
from utils.components import zen_header, zen_button, progress_bar, notification, content_section, tip_block

def calculate_test_results(scores):
    """Calculate the dominant degen type based on test scores"""
    return max(scores.items(), key=lambda x: x[1])[0]

def plot_radar_chart(scores):
    """Generate a radar chart for test results"""
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]  # Close the polygon
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # Ensure we have a valid limit
    max_val = max(values) if max(values) > 0 else 1
    ax.set_ylim(0, max_val)
    
    ax.set_title("Twój profil inwestycyjny", size=20, pad=20)
    ax.grid(True)
    
    for i, (angle, value) in enumerate(zip(angles[:-1], values[:-1])):
        color = DEGEN_TYPES[labels[i]]["color"]
        ax.text(angle, value + max_val*0.1, f"{labels[i]}\n({value})", 
                horizontalalignment='center', verticalalignment='center',
                fontsize=9, color=color, fontweight='bold')
    
    return fig

def show_degen_test():
    zen_header("Test Typu Degena")
    
    # Informacja o teście
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    if st.session_state.show_test_info:
        st.markdown("""
        ### 👉 Jak działa ten test?

        Ten test pomoże Ci sprawdzić, **jakim typem inwestora (degena)** jesteś.

        - Każde pytanie ma **8 odpowiedzi** – każda reprezentuje inny styl inwestycyjny.
        - **Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.**
        - Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego.        🧩 Gotowy? 
        """)
        if zen_button("Rozpocznij test"):
            st.session_state.show_test_info = False
            if 'test_step' not in st.session_state:
                st.session_state.test_step = 0
                st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
            st.rerun()
          # Opcja przeglądania typów degenów
        st.markdown("---")
        st.markdown("### 📚 Chcesz dowiedzieć się więcej o typach degenów?")
        selected_type = st.selectbox("Wybierz typ degena:", list(DEGEN_TYPES.keys()))
        if selected_type:
            st.markdown(f"### {selected_type}")
            
            col1, col2 = st.columns(2)
            with col1:
                content_section("Mocne strony:", 
                               "\n".join([f"- ✅ {strength}" for strength in DEGEN_TYPES[selected_type]["strengths"]]), 
                               icon="💪", 
                               collapsed=False)
            
            with col2:
                content_section("Wyzwania:", 
                               "\n".join([f"- ⚠️ {challenge}" for challenge in DEGEN_TYPES[selected_type]["challenges"]]), 
                               icon="🚧", 
                               collapsed=False)
            
            tip_block(DEGEN_TYPES[selected_type]["strategy"], "Rekomendowana strategia")
            
            # Dodajemy szczegółowy opis typu degena
            if st.checkbox("Pokaż szczegółowy opis typu"):
                if selected_type in degen_details:
                    st.markdown(degen_details[selected_type])
                else:
                    st.warning("Szczegółowy opis dla tego typu degena nie jest jeszcze dostępny.")
    # Tryb testu    
    elif 'test_step' not in st.session_state:
        st.session_state.test_step = 0
        st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
        st.rerun()
    
    elif st.session_state.test_step < len(TEST_QUESTIONS):
        # Display current question
        question = TEST_QUESTIONS[st.session_state.test_step]
        
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        st.subheader(f"Pytanie {st.session_state.test_step + 1} z {len(TEST_QUESTIONS)}")
        st.markdown(f"### {question['question']}")
        
        # Render options in two columns
        options = question['options']
        col1, col2 = st.columns(2)
        for i in range(len(options)):
            if i < len(options) // 2:
                with col1:
                    if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                        # Add scores for the answer
                        for degen_type, score in options[i]['scores'].items():
                            st.session_state.test_scores[degen_type] += score
                        
                        st.session_state.test_step += 1
                        st.rerun()
            else:
                with col2:
                    if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                        # Add scores for the answer
                        for degen_type, score in options[i]['scores'].items():
                            st.session_state.test_scores[degen_type] += score
                        
                        st.session_state.test_step += 1
                        st.rerun()
        
        # Progress bar
        progress_value = st.session_state.test_step / len(TEST_QUESTIONS)
        progress_bar(value=st.session_state.test_step, max_value=len(TEST_QUESTIONS), 
                    label=f"Postęp testu: {int(progress_value * 100)}%")
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # Show test results
        dominant_type = calculate_test_results(st.session_state.test_scores)
          # Update user data
        users_data = load_user_data()
        users_data[st.session_state.username]["degen_type"] = dominant_type
        users_data[st.session_state.username]["test_taken"] = True
        users_data[st.session_state.username]["test_scores"] = st.session_state.test_scores  # Save test scores
        users_data[st.session_state.username]["xp"] += 50  # Bonus XP for completing the test
        save_user_data(users_data)
        
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        st.subheader("Wyniki testu")
        
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2>Twój dominujący typ Degena to:</h2>
            <h1 style='color: {DEGEN_TYPES[dominant_type]["color"]};'>{dominant_type}</h1>
            <p>{DEGEN_TYPES[dominant_type]["description"]}</p>
        </div>
        """, unsafe_allow_html=True)
          # Radar chart
        radar_fig = plot_radar_chart(st.session_state.test_scores)
        st.pyplot(radar_fig)
        
        # Display strengths and challenges
        col1, col2 = st.columns(2)
        with col1:
            content_section(
                "Twoje mocne strony:", 
                "\n".join([f"- ✅ {strength}" for strength in DEGEN_TYPES[dominant_type]["strengths"]]),
                icon="💪",
                collapsed=False
            )
        with col2:
            content_section(
                "Twoje wyzwania:", 
                "\n".join([f"- ⚠️ {challenge}" for challenge in DEGEN_TYPES[dominant_type]["challenges"]]),
                icon="🚧",
                collapsed=False
            )
        
        tip_block(DEGEN_TYPES[dominant_type]["strategy"], title="Rekomendowana strategia", icon="🎯")
        
        # Dodanie szczegółowych informacji o typie degena
        content_section(
            "Szczegółowy opis twojego typu degena", 
            degen_details.get(dominant_type, "Szczegółowy opis dla tego typu degena nie jest jeszcze dostępny."),
            icon="🔍",
            collapsed=True
        )
          # Additional options
        if zen_button("Wykonaj test ponownie"):
            st.session_state.test_step = 0
            st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
            st.session_state.show_test_info = True
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        if zen_button("Przejdź do dashboardu"):
            st.session_state.test_step = 0
            st.session_state.page = 'dashboard'
            st.rerun()