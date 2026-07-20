import streamlit as st
import os
from document_processor import DocumentProcessor, display_document_stats
from agents import create_mcq_workflow, MCQState
from ui_components import KBCStyleUI
import time
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="PDF QuizMaster - Interactive Learning",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
KBCStyleUI.apply_custom_css()

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'document_processed' not in st.session_state:
        st.session_state.document_processed = False
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = None
    if 'time_per_question' not in st.session_state:
        st.session_state.time_per_question = 30
    if 'lifelines_used' not in st.session_state:
        st.session_state.lifelines_used = {'fifty_fifty': False, 'audience_poll': False, 'phone_friend': False}
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = []
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False
    if 'current_explanation' not in st.session_state:
        st.session_state.current_explanation = {}
    if 'waiting_for_next' not in st.session_state:
        st.session_state.waiting_for_next = False
    if 'last_update' not in st.session_state:
        st.session_state.last_update = 0
    if 'last_timer_update' not in st.session_state:
        st.session_state.last_timer_update = 0

def reset_quiz():
    """Reset all quiz-related session state"""
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.user_answers = {}
    st.session_state.quiz_completed = False
    st.session_state.quiz_started = False
    st.session_state.score = 0
    st.session_state.timer_start = None
    st.session_state.lifelines_used = {'fifty_fifty': False, 'audience_poll': False, 'phone_friend': False}
    st.session_state.quiz_results = []
    st.session_state.show_explanation = False
    st.session_state.current_explanation = {}
    st.session_state.waiting_for_next = False
    if hasattr(st.session_state, 'quiz_topic'):
        delattr(st.session_state, 'quiz_topic')
    if hasattr(st.session_state, 'quiz_difficulty'):
        delattr(st.session_state, 'quiz_difficulty')
    st.session_state.last_update = 0
    st.session_state.last_timer_update = 0

    # Clean up lifeline data for all questions
    keys_to_remove = []
    for key in st.session_state.keys():
        if ('fifty_fifty_options_' in key or
            'audience_poll_' in key or
            'phone_hint_' in key):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del st.session_state[key]

def process_document_and_generate_mcqs(uploaded_file, topic, difficulty, num_questions, groq_api_key):
    """Process document and generate MCQs using LangGraph agents"""
    
    # Extract text from document
    success, result = DocumentProcessor.process_document(uploaded_file)
    
    if not success:
        st.error(f"❌ {result}")
        return False
    
    # Validate text
    is_valid, message = DocumentProcessor.validate_text_for_mcq(result)
    if not is_valid:
        st.error(f"❌ {message}")
        return False
    
    st.success(f"✅ {message}")
    st.session_state.extracted_text = result
    
    # Display document stats
    st.subheader("📊 Document Analysis")
    display_document_stats(result)
    
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Create workflow
        status_text.text("🔄 Setting up AI agents...")
        progress_bar.progress(20)
        workflow = create_mcq_workflow(groq_api_key)
        
        # Prepare initial state
        status_text.text("📝 Processing document...")
        progress_bar.progress(40)
        
        initial_state: MCQState = {
            "document_text": result,
            "topic": topic,
            "difficulty": difficulty,
            "num_questions": num_questions,
            "processed_chunks": [],
            "raw_questions": "",
            "structured_questions": [],
            "final_mcqs": [],
            "current_question_index": 0,
            "user_answers": {},
            "score": 0,
            "feedback": []
        }
        
        # Run the workflow
        status_text.text("🤖 Generating MCQs...")
        progress_bar.progress(60)
        
        final_state = workflow.invoke(initial_state)
        
        status_text.text("✅ MCQs generated successfully!")
        progress_bar.progress(100)
        
        # Store questions and quiz configuration in session state
        st.session_state.questions = final_state["final_mcqs"]
        st.session_state.quiz_topic = topic
        st.session_state.quiz_difficulty = difficulty
        st.session_state.document_processed = True
        
        # Clear progress indicators
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error generating MCQs: {str(e)}")
        progress_bar.empty()
        status_text.empty()
        return False

def display_quiz_interface():
    """Display the main quiz interface with timer and lifelines"""
    questions = st.session_state.questions
    current_q_idx = st.session_state.current_question

    if current_q_idx >= len(questions):
        st.session_state.quiz_completed = True
        st.rerun()

    question = questions[current_q_idx]

    # Start timer for this question if not started
    if st.session_state.timer_start is None:
        st.session_state.timer_start = time.time()
        st.session_state.last_update = time.time()

    # Calculate remaining time
    current_time = time.time()
    elapsed_time = current_time - st.session_state.timer_start
    remaining_time = max(0, st.session_state.time_per_question - elapsed_time)

    # Check if we need to update (every second)
    time_since_update = current_time - st.session_state.get('last_update', 0)
    should_update = time_since_update >= 1.0

    # Auto-submit if time runs out
    if remaining_time <= 0:
        st.session_state.user_answers[current_q_idx] = "No Answer (Time Up)"
        st.session_state.quiz_results.append({
            'question': question['question'],
            'user_answer': "No Answer (Time Up)",
            'correct_answer': question['correct_answer'],
            'is_correct': False,
            'explanation': question['explanation'],
            'time_taken': st.session_state.time_per_question
        })

        # Store explanation data for time up display
        st.session_state.current_explanation = {
            'explanation': question["explanation"],
            'is_correct': False,
            'correct_answer': question["correct_answer"],
            'user_answer': "No Answer (Time Up)",
            'time_up': True
        }
        st.session_state.show_explanation = True
        st.session_state.waiting_for_next = True
        st.session_state.timer_start = None
        st.rerun()

    # Display quiz info in right column
    main_col, sidebar_col = st.columns([3, 1])

    with sidebar_col:
        st.subheader("📊 Quiz Progress")

        # Timer display
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        percentage = (remaining_time / st.session_state.time_per_question) * 100

        # Enhanced timer display
        KBCStyleUI.display_enhanced_timer(remaining_time, st.session_state.time_per_question)

        # Optimized timer refresh - update every 2 seconds to avoid button interference
        if remaining_time > 0 and not st.session_state.show_explanation:
            timer_update_interval = 2.0  # Update every 2 seconds
            if current_time - st.session_state.last_timer_update >= timer_update_interval:
                st.session_state.last_timer_update = current_time
                st.rerun()

        # Quiz statistics
        accuracy = (st.session_state.score / max(1, current_q_idx + 1)) * 100 if current_q_idx >= 0 else 0

        st.metric("Score", f"{st.session_state.score}/{len(questions)}")
        st.metric("Question", f"{current_q_idx + 1}/{len(questions)}")
        st.metric("Accuracy", f"{accuracy:.1f}%")

    with main_col:
        # Show explanation overlay if needed (this takes priority)
        if st.session_state.show_explanation:
            explanation_data = st.session_state.current_explanation

            # Display question reference
            st.markdown(f"### Question {current_q_idx + 1} of {len(questions)}")
            st.markdown(f"**{question['question']}**")

            # Show user's answer with special handling for time up
            if explanation_data.get('time_up', False):
                st.error(f"⏰ **Time's Up!** No answer submitted")
                st.warning(f"🎯 **Correct Answer:** {explanation_data['correct_answer']}")
            else:
                st.markdown(f"**Your Answer:** {explanation_data['user_answer']}")

            # Show explanation with improved styling
            KBCStyleUI.show_explanation(
                explanation_data['explanation'],
                explanation_data['is_correct']
            )

            # Show correct answer if user was wrong (but not for time up, as we already showed it)
            if not explanation_data['is_correct'] and not explanation_data.get('time_up', False):
                st.error(f"🎯 **Correct Answer:** {explanation_data['correct_answer']}")

            # Next button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                # Simple, stable key for next button
                next_key = f"next_{current_q_idx}"

                if st.button(
                    "➡️ Next Question",
                    key=next_key,
                    use_container_width=True,
                    type="primary"
                ):
                    # Execute immediately without flags
                    st.session_state.show_explanation = False
                    st.session_state.waiting_for_next = False
                    st.session_state.current_question += 1
                    st.rerun()

        else:
            # Normal quiz interface (only show when not showing explanation)
            # Display lifelines
            KBCStyleUI.display_lifelines(st.session_state.lifelines_used, question, current_q_idx)

            # Display question card
            KBCStyleUI.display_question_card(
                current_q_idx + 1,
                len(questions),
                question["question"]
            )

            # Display options (may be modified by lifelines)
            options_to_show = question["options"][:]
            if st.session_state.lifelines_used.get('fifty_fifty', False) and f'fifty_fifty_options_{current_q_idx}' in st.session_state:
                options_to_show = st.session_state[f'fifty_fifty_options_{current_q_idx}']

            user_answer = KBCStyleUI.display_options(
                options_to_show,
                str(current_q_idx)
            )

            # Show audience poll if used
            if st.session_state.lifelines_used.get('audience_poll', False) and f'audience_poll_{current_q_idx}' in st.session_state:
                st.markdown("### 👥 Audience Poll Results")
                poll_data = st.session_state[f'audience_poll_{current_q_idx}']
                cols = st.columns(4)
                option_labels = ['A', 'B', 'C', 'D']

                for i, (col, label) in enumerate(zip(cols, option_labels)):
                    percentage = poll_data.get(label, 0)
                    with col:
                        st.metric(f"Option {label}", f"{percentage}%")
                        st.progress(percentage / 100)

            # Show phone friend hint if used
            if st.session_state.lifelines_used.get('phone_friend', False) and f'phone_hint_{current_q_idx}' in st.session_state:
                st.info(f"💡 Your friend's hint: {st.session_state[f'phone_hint_{current_q_idx}']}")

            # Navigation buttons
            _, col2, _ = st.columns([1, 2, 1])

            with col2:
                # Check if already answered to prevent multiple submissions
                already_answered = current_q_idx in st.session_state.user_answers
                submit_disabled = already_answered or st.session_state.show_explanation

                button_text = "Submit Answer"
                if already_answered:
                    button_text = "✓ Already Answered"

                # Simple, stable key for submit button
                submit_key = f"submit_{current_q_idx}"

                if st.button(
                    button_text,
                    key=submit_key,
                    use_container_width=True,
                    disabled=submit_disabled,
                    type="primary"
                ):
                    if user_answer and not already_answered:
                        # Store answer
                        st.session_state.user_answers[current_q_idx] = user_answer

                        # Check if correct
                        is_correct = user_answer == question["correct_answer"]
                        if is_correct:
                            st.session_state.score += 1

                        # Store result
                        st.session_state.quiz_results.append({
                            'question': question['question'],
                            'user_answer': user_answer,
                            'correct_answer': question['correct_answer'],
                            'is_correct': is_correct,
                            'explanation': question['explanation'],
                            'time_taken': st.session_state.time_per_question - remaining_time
                        })

                        # Store explanation data for display
                        st.session_state.current_explanation = {
                            'explanation': question["explanation"],
                            'is_correct': is_correct,
                            'correct_answer': question["correct_answer"],
                            'user_answer': user_answer
                        }
                        st.session_state.show_explanation = True
                        st.session_state.waiting_for_next = True

                        # Reset timer for next question
                        st.session_state.timer_start = None
                        st.rerun()
                    elif not user_answer:
                        st.error("⚠️ Please select an answer before submitting!")

def display_final_results():
    """Display comprehensive quiz summary and thank you message"""
    st.title("🎉 Quiz Completed!")

    total_questions = len(st.session_state.questions)
    score = st.session_state.score
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0

    # Show final score prominently
    if percentage >= 80:
        st.balloons()
        st.success(f"🏆 Excellent! You scored {score}/{total_questions} ({percentage:.1f}%)")
    elif percentage >= 60:
        st.success(f"🎯 Great job! You scored {score}/{total_questions} ({percentage:.1f}%)")
    elif percentage >= 40:
        st.warning(f"👍 Good effort! You scored {score}/{total_questions} ({percentage:.1f}%)")
    else:
        st.info(f"💪 Keep practicing! You scored {score}/{total_questions} ({percentage:.1f}%)")

    st.write("")  # Add spacing

    # Detailed Quiz Summary Section
    st.subheader("📋 Detailed Quiz Summary")

    # Calculate comprehensive statistics
    total_time = sum([result.get('time_taken', 0) for result in st.session_state.quiz_results])
    avg_time_per_question = total_time / total_questions if total_questions > 0 else 0
    lifelines_count = sum([1 for k, v in st.session_state.lifelines_used.items() if v])

    # Get quiz configuration details
    topic = getattr(st.session_state, 'quiz_topic', 'General Knowledge')
    difficulty = getattr(st.session_state, 'quiz_difficulty', 'Medium')

    # Display comprehensive summary in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Final Score", f"{score}/{total_questions}")
        st.metric("🎯 Accuracy", f"{percentage:.1f}%")

    with col2:
        st.metric("✅ Correct", score)
        st.metric("❌ Incorrect", total_questions - score)

    with col3:
        st.metric("⏱️ Total Time", f"{total_time:.1f}s")
        st.metric("📈 Avg Time/Q", f"{avg_time_per_question:.1f}s")

    with col4:
        st.metric("🎮 Lifelines Used", f"{lifelines_count}/3")
        st.metric("📚 Difficulty", difficulty)

    st.write("")  # Add spacing

    # Quiz Configuration Details
    st.subheader("📖 Quiz Details")

    config_col1, config_col2 = st.columns(2)

    with config_col1:
        st.info(f"**📝 Topic:** {topic}")
        st.info(f"**🎚️ Difficulty Level:** {difficulty}")

    with config_col2:
        st.info(f"**🔢 Total Questions:** {total_questions}")
        st.info(f"**⏰ Time per Question:** {st.session_state.time_per_question}s")

    # Performance Analysis
    if total_questions > 0:
        st.subheader("📊 Performance Analysis")

        performance_msg = ""
        if percentage >= 90:
            performance_msg = "🌟 Outstanding performance! You have excellent understanding of the material."
        elif percentage >= 80:
            performance_msg = "🏆 Excellent work! You demonstrated strong knowledge in this area."
        elif percentage >= 70:
            performance_msg = "🎯 Good performance! You have a solid grasp of the concepts."
        elif percentage >= 60:
            performance_msg = "👍 Fair performance! Consider reviewing the material for better understanding."
        else:
            performance_msg = "💪 Keep studying! Practice more to improve your understanding."

        st.info(performance_msg)

    st.write("")  # Add spacing

    # Lifelines Usage Breakdown
    if lifelines_count > 0:
        st.subheader("🎮 Lifelines Used")
        lifeline_cols = st.columns(3)

        with lifeline_cols[0]:
            if st.session_state.lifelines_used.get('fifty_fifty', False):
                st.success("✅ 50:50 - Used")
            else:
                st.info("❌ 50:50 - Not used")

        with lifeline_cols[1]:
            if st.session_state.lifelines_used.get('audience_poll', False):
                st.success("✅ Audience Poll - Used")
            else:
                st.info("❌ Audience Poll - Not used")

        with lifeline_cols[2]:
            if st.session_state.lifelines_used.get('phone_friend', False):
                st.success("✅ Phone Friend - Used")
            else:
                st.info("❌ Phone Friend - Not used")

    st.write("")  # Add more spacing

    # Enhanced Thank you section
    st.markdown("""
    <div style='background-color: #2d2d2d; padding: 25px; border-radius: 15px; border: 3px solid #4CAF50; margin: 25px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
        <h1 style='color: #4CAF50; text-align: center; margin: 0; font-size: 2.5em;'>🎉 Congratulations!</h1>
        <h2 style='color: white; text-align: center; margin: 10px 0; font-size: 1.8em;'>Thank you for using PDF QuizMaster!</h2>
        <p style='color: #cccccc; text-align: center; margin: 15px 0; font-size: 1.1em;'>You've successfully completed the quiz and demonstrated your knowledge.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color: #1e3a8a; padding: 20px; border-radius: 12px; border: 2px solid #3b82f6; margin: 15px 0;'>
        <h3 style='color: white; text-align: center; margin: 0 0 10px 0; font-size: 1.3em;'>🚀 Continue Your Learning Journey</h3>
        <p style='color: #e0e7ff; text-align: center; margin: 0; font-size: 1.1em;'>📄 Upload another document to generate new quizzes and expand your knowledge!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # Add spacing

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📄 Try Another File", use_container_width=True, type="primary"):
            reset_quiz()
            st.rerun()

    st.write("")  # Add final spacing

def main():
    """Main application function"""
    initialize_session_state()
    
    # Display title
    KBCStyleUI.display_title()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Quiz Settings")

        # Get Groq API Key from environment
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            st.error("⚠️ AI service configuration missing.")
            st.info("💡 Please check your configuration settings.")
            st.stop()
        
        # Document upload
        st.subheader("📄 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or text file",
            type=['pdf', 'txt', 'md'],
            help="Upload a document to generate MCQs from"
        )
        
        # Quiz configuration
        st.subheader("🎯 Quiz Configuration")
        topic = st.text_input(
            "📖 Topic/Subject",
            value="General Knowledge",
            help="Enter the main topic or subject"
        )

        difficulty = st.selectbox(
            "🎚️ Difficulty Level",
            ["Easy", "Medium", "Hard"],
            index=1
        )

        num_questions = st.slider(
            "🔢 Number of Questions",
            min_value=3,
            max_value=15,
            value=5,
            help="Select number of MCQs to generate"
        )

        # Timer configuration
        st.subheader("⏱️ Timer Settings")
        st.session_state.time_per_question = st.slider(
            "⏰ Time per Question (seconds)",
            min_value=10,
            max_value=120,
            value=30,
            help="Set time limit for each question"
        )
        
        # Generate button
        if st.button("🚀 Generate MCQs", use_container_width=True):
            if not uploaded_file:
                st.error("❌ Please upload a document!")
            else:
                reset_quiz()
                with st.spinner("Generating MCQs..."):
                    success = process_document_and_generate_mcqs(
                        uploaded_file, topic, difficulty, num_questions, groq_api_key
                    )
                    if success:
                        st.success("✅ MCQs generated successfully!")
                        st.session_state.quiz_started = True
    
    # Main content area
    if st.session_state.quiz_completed:
        display_final_results()
    elif st.session_state.quiz_started and st.session_state.questions:
        # Display quiz with sidebar
        display_quiz_interface()
    elif st.session_state.document_processed:
        st.info("📋 Document processed successfully! Click 'Generate MCQs' to start the quiz.")
        KBCStyleUI.display_quiz_stats(st.session_state.questions)
    else:
        # Enhanced Welcome screen with better styling
        KBCStyleUI.display_enhanced_welcome_page()



if __name__ == "__main__":
    main()