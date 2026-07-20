import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import time
import random
import pandas as pd

class KBCStyleUI:
    """ChatGPT-style clean UI components"""

    @staticmethod
    def apply_custom_css():
        """Apply custom CSS for ChatGPT-like clean theme"""
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        .main {
            background: #212121;
            color: #ececf1;
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: #212121;
        }

        /* Sidebar styling like ChatGPT */
        .css-1d391kg {
            background: #171717;
        }

        .css-17lntkn {
            background: #171717;
            color: #ececf1;
        }

        /* Sidebar text color */
        .css-17lntkn .stMarkdown,
        .css-17lntkn .stText,
        .css-17lntkn label {
            color: #ececf1 !important;
        }

        /* Sidebar headers */
        .css-17lntkn h1,
        .css-17lntkn h2,
        .css-17lntkn h3 {
            color: #ffffff !important;
        }

        /* Sidebar input styling */
        .css-17lntkn .stTextInput input,
        .css-17lntkn .stSelectbox select,
        .css-17lntkn .stSlider {
            background: #2d2d30 !important;
            color: #ececf1 !important;
            border: 1px solid #3e3e42 !important;
        }

        /* Sidebar file uploader */
        .css-17lntkn .stFileUploader {
            background: #2d2d30 !important;
            border: 1px solid #3e3e42 !important;
        }

        /* Main content text colors */
        .stMarkdown p {
            color: #ffffff !important;
        }

        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3 {
            color: #ffffff !important;
        }

        /* Radio button options styling */
        .stRadio > div > label {
            color: #ffffff !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
        }

        .stRadio > div > label > div {
            color: #ffffff !important;
        }

        /* Radio button text */
        .stRadio label span {
            color: #ffffff !important;
        }

        /* Top bar styling like ChatGPT */
        .stApp > header {
            background: #0d1117 !important;
            color: #ffffff !important;
        }

        /* Streamlit header/toolbar */
        .css-18e3th9 {
            background: #0d1117 !important;
        }

        .css-1dp5vir {
            background: #0d1117 !important;
        }

        /* Right sidebar for timer/score */
        .quiz-sidebar {
            position: fixed;
            top: 80px;
            right: 20px;
            width: 280px;
            background: #171717;
            border: 1px solid #3e3e42;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            z-index: 1000;
        }

        .quiz-sidebar h3 {
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            text-align: center;
        }

        .sidebar-section {
            background: #2d2d30;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.75rem;
            border: 1px solid #3e3e42;
        }

        .sidebar-label {
            color: #c5c5d2;
            font-size: 0.8rem;
            font-weight: 500;
            margin-bottom: 0.25rem;
        }

        .sidebar-value {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .timer-display {
            background: #1a472a;
            border: 1px solid #10a37f;
            border-radius: 8px;
            padding: 0.75rem;
            text-align: center;
            margin-bottom: 0.75rem;
        }

        .timer-display.warning {
            background: #7c2d12;
            border-color: #ea580c;
        }

        .timer-display.critical {
            background: #7f1d1d;
            border-color: #dc2626;
        }

        .timer-text {
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.2rem;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        .title-container {
            text-align: center;
            padding: 2rem 0;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }

        .welcome-card {
            background: #2d2d30;
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
            border: 1px solid #3e3e42;
        }

        .question-card {
            background: #2d2d30;
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
            border: 1px solid #3e3e42;
        }

        .question-text {
            font-family: 'Inter', sans-serif;
            font-size: 1.25rem;
            font-weight: 500;
            color: #ececf1;
            text-align: left;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }

        .interactive-card {
            background: #2d2d30;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #3e3e42;
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .interactive-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            border-color: #10a37f;
        }

        .metric-container {
            background: #2d2d30;
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid #3e3e42;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        }

        .timer-container {
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            color: #92400e;
            margin: 1rem 0;
        }

        .timer-warning {
            background: #fed7aa;
            border-color: #ea580c;
            color: #c2410c;
        }

        .timer-critical {
            background: #fecaca;
            border-color: #dc2626;
            color: #dc2626;
        }

        .stButton > button {
            background: #10a37f;
            border: none;
            border-radius: 8px;
            color: white;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: #0d8c6c;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(16, 163, 127, 0.3);
        }

        .score-display {
            background: #ecfdf5;
            border: 1px solid #10b981;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            color: #047857;
            margin: 1rem 0;
        }

        .section-header {
            color: #ececf1;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.25rem;
            margin-bottom: 1rem;
        }

        .feature-text {
            color: #c5c5d2;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .highlight-box {
            background: #2d2d30;
            border: 1px solid #3e3e42;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }

        .demo-box {
            background: #2d2d30;
            border: 1px solid #3e3e42;
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
        }

        /* Enhanced timer styling */
        .timer-countdown {
            background: #2d2d30;
            border: 2px solid #10a37f;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            font-family: 'Inter', monospace;
            font-weight: 700;
            font-size: 1.3rem;
            color: #ffffff;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }

        .timer-warning {
            border-color: #f59e0b;
            background: #451a03;
        }

        .timer-critical {
            border-color: #dc2626;
            background: #7f1d1d;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
            100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_title():
        """Display clean title"""
        st.markdown("""
        <div class="title-container">
            📚 PDF QuizMaster
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_question_card(question_num: int, total_questions: int, question_text: str):
        """Display question in clean card"""
        progress_percentage = (question_num / total_questions) * 100

        st.markdown(f"""
        <div class="question-card">
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 1rem;">
                Question {question_num} of {total_questions}
            </div>
            <div style="background: #e5e7eb; border-radius: 8px; height: 4px; margin-bottom: 1.5rem;">
                <div style="background: #10b981; height: 100%; border-radius: 8px; width: {progress_percentage}%; transition: width 0.5s ease;"></div>
            </div>
            <div class="question-text">
                {question_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_options(options: List[str], question_id: str) -> str:
        """Display options with clean styling and no default selection"""
        option_labels = ['A', 'B', 'C', 'D']

        # Create formatted options, handling removed options
        formatted_options = []
        for label, option in zip(option_labels, options):
            if option == "[Removed]":
                formatted_options.append(f"{label}: [Removed by 50:50]")
            else:
                formatted_options.append(f"{label}: {option}")

        # Filter out removed options for selection
        selectable_options = [opt for opt in formatted_options if "[Removed]" not in opt]

        if not selectable_options:
            st.error("No options available!")
            return ""

        # Add a placeholder option to force user choice
        options_with_placeholder = ["Please select an answer..."] + selectable_options

        selected = st.radio(
            "Select your answer:",
            options_with_placeholder,
            index=0,  # Start with placeholder selected
            key=f"question_{question_id}",
            help="Choose the option you think is correct"
        )

        # Return empty string if placeholder is selected, otherwise return the letter
        if selected and selected != "Please select an answer...":
            return selected[0]  # Return A, B, C, or D
        return ""

    @staticmethod
    def display_score_card(current_score: int, total_questions: int, percentage: float):
        """Display current score in clean style"""
        st.markdown(f"""
        <div class="score-display">
            Score: {current_score}/{total_questions} ({percentage:.1f}%)
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_timer(remaining_time: float, total_time: int):
        """Display countdown timer"""
        percentage = (remaining_time / total_time) * 100

        # Determine timer style based on remaining time
        if percentage > 50:
            timer_class = "timer-container"
        elif percentage > 20:
            timer_class = "timer-container timer-warning"
        else:
            timer_class = "timer-container timer-critical"

        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        st.markdown(f"""
        <div class="{timer_class}">
            ⏱️ Time Remaining: {minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)

        # Progress bar for timer
        st.progress(remaining_time / total_time)

    @staticmethod
    def display_quiz_sidebar(remaining_time: float, total_time: int, current_score: int, total_questions: int, current_question: int):
        """Display quiz info using native Streamlit components"""
        # Create a container for the sidebar content
        with st.container():
            # Timer display
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            percentage = (remaining_time / total_time) * 100

            # Color-coded timer based on remaining time
            if percentage > 50:
                st.success(f"⏱️ Time: {minutes:02d}:{seconds:02d}")
            elif percentage > 20:
                st.warning(f"⏱️ Time: {minutes:02d}:{seconds:02d}")
            else:
                st.error(f"⏱️ Time: {minutes:02d}:{seconds:02d}")

            # Progress bar for time
            st.progress(percentage / 100)

            # Quiz statistics
            accuracy = (current_score / max(1, current_question)) * 100 if current_question > 0 else 0

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Score", f"{current_score}/{total_questions}")
                st.metric("Accuracy", f"{accuracy:.1f}%")

            with col2:
                st.metric("Question", f"{current_question}/{total_questions}")
                st.metric("Remaining", f"{total_questions - current_question}")

    @staticmethod
    def display_lifelines(lifelines_used: Dict[str, bool], question: Dict[str, Any], question_idx: int):
        """Display clean lifelines with instant responsiveness"""
        st.markdown("### Lifelines")

        col1, col2, col3 = st.columns(3)

        with col1:
            fifty_fifty_disabled = lifelines_used.get('fifty_fifty', False)

            if st.button(
                "🎲 50:50" if not fifty_fifty_disabled else "✓ 50:50 Used",
                disabled=fifty_fifty_disabled,
                key=f"lifeline_50_50_{question_idx}",
                help="Remove 2 incorrect options"
            ):
                # Execute immediately without any flags or delays
                KBCStyleUI._use_fifty_fifty(question, question_idx)
                st.session_state.lifelines_used['fifty_fifty'] = True
                st.rerun()

        with col2:
            audience_disabled = lifelines_used.get('audience_poll', False)

            if st.button(
                "👥 Audience Poll" if not audience_disabled else "✓ Audience Used",
                disabled=audience_disabled,
                key=f"lifeline_audience_{question_idx}",
                help="See what the audience thinks"
            ):
                # Execute immediately without any flags or delays
                KBCStyleUI._use_audience_poll(question, question_idx)
                st.session_state.lifelines_used['audience_poll'] = True
                st.rerun()

        with col3:
            phone_disabled = lifelines_used.get('phone_friend', False)

            if st.button(
                "📞 Phone Friend" if not phone_disabled else "✓ Phone Used",
                disabled=phone_disabled,
                key=f"lifeline_phone_{question_idx}",
                help="Get a helpful hint"
            ):
                # Execute immediately without any flags or delays
                KBCStyleUI._use_phone_friend(question, question_idx)
                st.session_state.lifelines_used['phone_friend'] = True
                st.rerun()

    @staticmethod
    def _use_fifty_fifty(question: Dict[str, Any], question_idx: int):
        """Implement 50:50 lifeline"""
        key = f'fifty_fifty_options_{question_idx}'
        if key not in st.session_state:
            options = question['options'][:]
            correct_answer = question['correct_answer']
            correct_idx = ['A', 'B', 'C', 'D'].index(correct_answer)
            incorrect_indices = [i for i in range(len(options)) if i != correct_idx]

            if len(incorrect_indices) >= 2:
                to_remove = random.sample(incorrect_indices, 2)
            else:
                to_remove = incorrect_indices

            fifty_fifty_options = []
            for i, option in enumerate(options):
                if i in to_remove:
                    fifty_fifty_options.append("[Removed]")
                else:
                    fifty_fifty_options.append(option)

            st.session_state[key] = fifty_fifty_options

    @staticmethod
    def _use_audience_poll(question: Dict[str, Any], question_idx: int):
        """Implement audience poll lifeline"""
        key = f'audience_poll_{question_idx}'
        if key not in st.session_state:
            options = ['A', 'B', 'C', 'D']
            correct_answer = question['correct_answer']
            base_votes = [random.randint(5, 25) for _ in range(4)]
            correct_idx = options.index(correct_answer)

            if random.random() < 0.7:
                base_votes[correct_idx] += random.randint(15, 35)

            total = sum(base_votes)
            percentages = {}
            for i, option in enumerate(options):
                percentages[option] = round((base_votes[i] / total) * 100)

            total_percent = sum(percentages.values())
            if total_percent != 100:
                percentages[correct_answer] += (100 - total_percent)

            st.session_state[key] = percentages

    @staticmethod
    def _use_phone_friend(question: Dict[str, Any], question_idx: int):
        """Implement phone friend lifeline"""
        key = f'phone_hint_{question_idx}'
        if key not in st.session_state:
            hints = [
                "Look for keywords in the question that might guide you to the answer.",
                "Try to eliminate options that seem obviously incorrect first.",
                "Think about the main topic and what you know about it.",
                "Consider which option fits best with the context provided.",
                "Sometimes the longest or most detailed option is correct.",
                "Look for options that directly relate to the question's subject."
            ]
            hint = random.choice(hints)
            st.session_state[key] = hint

    @staticmethod
    def display_final_results_enhanced(score: int, total: int, percentage: float, results: List[Dict]):
        """Display clean final results"""
        if percentage >= 80:
            st.balloons()
            emoji = "🏆"
            message = "Excellent! Outstanding performance!"
            color = "#10b981"
        elif percentage >= 60:
            emoji = "🎉"
            message = "Great job! Well done!"
            color = "#3b82f6"
        elif percentage >= 40:
            emoji = "👏"
            message = "Good effort! Keep learning!"
            color = "#f59e0b"
        else:
            emoji = "💪"
            message = "Keep practicing! You'll improve!"
            color = "#ef4444"

        st.markdown(f"""
        <div style="
            background: #2d2d30;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
            border: 1px solid {color};
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{emoji}</div>
            <div style="font-family: 'Inter', sans-serif; font-size: 1.5rem; font-weight: 600; color: {color}; margin-bottom: 1rem;">
                {message}
            </div>
            <div style="font-family: 'Inter', sans-serif; font-size: 1.25rem; color: #ececf1;">
                Final Score: {score}/{total} ({percentage:.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_performance_charts(results: List[Dict]):
        """Display performance charts"""
        if not results:
            return

        df = pd.DataFrame(results)
        df['question_num'] = range(1, len(df) + 1)
        df['time_taken'] = df['time_taken'].fillna(0)

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.line(
                df, x='question_num', y='time_taken',
                title='Time Taken per Question', markers=True
            )
            fig1.update_layout(
                paper_bgcolor="#2d2d30",
                plot_bgcolor="#2d2d30",
                font={'color': "#ececf1"}
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            correct_count = df['is_correct'].sum()
            incorrect_count = len(df) - correct_count

            fig2 = go.Figure(data=[go.Pie(
                labels=['Correct', 'Incorrect'],
                values=[correct_count, incorrect_count],
                marker_colors=['#10b981', '#ef4444']
            )])
            fig2.update_layout(
                title='Answer Distribution',
                paper_bgcolor="#2d2d30",
                plot_bgcolor="#2d2d30",
                font={'color': "#ececf1"}
            )
            st.plotly_chart(fig2, use_container_width=True)

    @staticmethod
    def show_detailed_statistics(results: List[Dict], total_questions: int):
        """Show detailed statistics"""
        if not results:
            st.error("No results to display")
            return

        st.subheader("📊 Performance Analysis")

        df = pd.DataFrame(results)
        correct_answers = df['is_correct'].sum()
        accuracy = (correct_answers / total_questions) * 100
        avg_time = df['time_taken'].mean()
        fastest_time = df['time_taken'].min()
        slowest_time = df['time_taken'].max()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        with col2:
            st.metric("Avg Time", f"{avg_time:.1f}s")
        with col3:
            st.metric("Fastest", f"{fastest_time:.1f}s")
        with col4:
            st.metric("Slowest", f"{slowest_time:.1f}s")

    @staticmethod
    def show_explanation(explanation: str, is_correct: bool):
        """Show explanation with improved dark styling and overlay effect"""
        if is_correct:
            color = "#10a37f"
            bg_color = "#0d2818"
            border_color = "#10a37f"
            icon = "✅"
            status = "Correct!"
        else:
            color = "#ff6b6b"
            bg_color = "#2d1b1b"
            border_color = "#ff6b6b"
            icon = "❌"
            status = "Incorrect"

        st.markdown(f"""
        <div style="
            background: {bg_color};
            border: 2px solid {border_color};
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
            position: relative;
            z-index: 100;
        ">
            <div style="
                font-weight: 700;
                color: {color};
                margin-bottom: 1rem;
                font-size: 1.3rem;
                text-align: center;
            ">
                {icon} {status}
            </div>
            <div style="
                color: #ffffff;
                line-height: 1.8;
                font-size: 1.1rem;
                font-weight: 500;
                text-align: left;
                background: #1a1a1a;
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 4px solid {color};
            ">
                {explanation}
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_quiz_stats(questions: List[Dict[str, Any]]):
        """Display quiz statistics"""
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Questions", len(questions))

        with col2:
            st.metric("Difficulty", "Medium")

        with col3:
            time_limit = st.session_state.get('time_per_question', 30)
            st.metric("Time per Question", f"{time_limit}s")


    @staticmethod
    def display_enhanced_timer(remaining_time: float, total_time: int):
        """Display enhanced timer with better visual feedback"""
        percentage = (remaining_time / total_time) * 100
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        # Determine timer style
        if percentage > 50:
            timer_class = "timer-countdown"
        elif percentage > 20:
            timer_class = "timer-countdown timer-warning"
        else:
            timer_class = "timer-countdown timer-critical"

        # Display timer without JavaScript interference
        st.markdown(f"""
        <div class="{timer_class}" id="timer-display">
            ⏱️ Time: {minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.progress(percentage / 100)

    @staticmethod
    def display_enhanced_welcome_page():
        """Display enhanced welcome page with better styling and interactivity"""

        # Enhanced title section using native Streamlit
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
            <h1 style="color: #ffffff; font-size: 3rem; margin: 0;">📚 PDF QuizMaster</h1>
            <p style="color: #e8e8e8; font-size: 1.2rem; margin: 1rem 0 0 0;">Transform Documents into Interactive Learning</p>
        </div>
        """, unsafe_allow_html=True)

        # Description using Streamlit components with better colors
        st.markdown("""
        <div style="background: #2d2d30; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border: 1px solid #10a37f;">
            <p style="color: #ffffff; font-size: 1.1rem; text-align: center; margin: 0; line-height: 1.6;">
                🎯 Transform your documents into interactive learning experiences with AI-powered MCQs<br>
                ⚡ Practice with timer challenges, lifelines, and detailed analytics
            </p>
        </div>
        """, unsafe_allow_html=True)

        # How to Get Started - using native Streamlit for better compatibility
        st.markdown("## 🚀 How to Get Started")

        # Using Streamlit's native info boxes with white text
        st.markdown("""
        <div style="background: #1a472a; padding: 1.5rem; border-radius: 10px; border: 2px solid #10a37f; margin: 1rem 0;">
            <div style="color: #ffffff; font-size: 1rem; line-height: 1.8;">
                <p style="margin: 0.5rem 0;"><strong>📄 Step 1:</strong> Upload your PDF, TXT, or MD document using the sidebar</p>
                <p style="margin: 0.5rem 0;"><strong>⚙️ Step 2:</strong> Configure quiz settings (difficulty, timer, number of questions)</p>
                <p style="margin: 0.5rem 0;"><strong>🎮 Step 3:</strong> Take the quiz using interactive lifelines when needed</p>
                <p style="margin: 0.5rem 0;"><strong>📊 Step 4:</strong> Review your performance with detailed analytics</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Key Features using Streamlit columns
        st.markdown("## ✨ Key Features")

        col1, col2 = st.columns(2)

        with col1:
            st.info("**⏱️ Smart Timer**\nConfigurable countdowns add challenge and excitement to your learning experience")
            st.info("**👥 Audience Poll**\nSee how others might vote to help guide your decision making")

        with col2:
            st.info("**🎲 50:50 Lifeline**\nRemove two incorrect options to improve your chances of success")
            st.info("**📞 Phone Friend**\nGet strategic hints when you're stuck on difficult questions")

        # Call to action
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
            <h2 style="color: #ffffff; margin: 0 0 1rem 0;">🚀 Ready to Get Started?</h2>
            <p style="color: #fecaca; margin: 0 0 1rem 0;">Upload your document and begin your interactive learning journey!</p>
            <div style="background: #ffffff; color: #dc2626; padding: 0.75rem 1.5rem; border-radius: 8px; display: inline-block; font-weight: bold;">
                📚 Supported formats: PDF, TXT, MD files
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_animated_spinner():
    """Create a simple loading spinner"""
    return st.spinner("Loading...")