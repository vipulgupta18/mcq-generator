from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import json
import os
from dotenv import load_dotenv

load_dotenv()

class MCQState(TypedDict):
    document_text: str
    topic: str
    difficulty: str
    num_questions: int
    processed_chunks: List[str]
    raw_questions: str
    structured_questions: List[Dict[str, Any]]
    final_mcqs: List[Dict[str, Any]]
    current_question_index: int
    user_answers: Dict[int, str]
    score: int
    feedback: List[Dict[str, Any]]

class MCQAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.3
        )
    
    def text_processor_agent(self, state: MCQState) -> MCQState:
        """Process and chunk the document text for better MCQ generation"""
        text = state["document_text"]
        
        # Simple chunking strategy - split by paragraphs and limit chunk size
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < 2000:  # Keep chunks under 2000 chars
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        state["processed_chunks"] = chunks
        return state
    
    def mcq_generator_agent(self, state: MCQState) -> MCQState:
        """Generate MCQs from the processed text chunks"""
        chunks = state["processed_chunks"]
        topic = state["topic"]
        difficulty = state["difficulty"]
        num_questions = state["num_questions"]
        
        # Combine chunks for context
        context = "\n\n".join(chunks[:3])  # Use first 3 chunks to avoid token limits
        
        prompt = f"""
        Based on the following text about {topic}, create {num_questions} multiple choice questions at {difficulty} difficulty level.
        
        Text: {context}
        
        For each question, provide:
        1. A clear question
        2. Four options (A, B, C, D)
        3. The correct answer
        4. A brief explanation
        
        Format your response as a JSON array where each question is an object with keys: 
        "question", "options", "correct_answer", "explanation"
        
        Example format:
        [
            {{
                "question": "What is the main topic discussed?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "A",
                "explanation": "Brief explanation of why A is correct"
            }}
        ]
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            state["raw_questions"] = response.content
            return state
        except Exception as e:
            # If there's an error, set empty questions and let the validator handle fallback
            state["raw_questions"] = ""
            return state
    
    def question_validator_agent(self, state: MCQState) -> MCQState:
        """Validate and structure the generated questions"""
        raw_questions = state["raw_questions"]

        try:
            # Try to parse JSON from the response
            # Sometimes the LLM adds extra text, so we need to extract JSON
            start_idx = raw_questions.find('[')
            end_idx = raw_questions.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = raw_questions[start_idx:end_idx]
                questions = json.loads(json_str)
            else:
                # Fallback: create questions from text
                questions = self._parse_text_to_questions(raw_questions, state["num_questions"])
            
            # Validate each question has required fields
            validated_questions = []
            for i, q in enumerate(questions):
                if all(key in q for key in ["question", "options", "correct_answer", "explanation"]):
                    # Ensure options is a list of 4 items
                    if isinstance(q["options"], list) and len(q["options"]) == 4:
                        validated_questions.append({
                            "id": i + 1,
                            "question": q["question"],
                            "options": q["options"],
                            "correct_answer": q["correct_answer"].upper(),
                            "explanation": q["explanation"]
                        })
            
            state["structured_questions"] = validated_questions

        except Exception as e:
            # Fallback: create simple questions
            state["structured_questions"] = self._create_fallback_questions(state["num_questions"])

        return state
    
    def _parse_text_to_questions(self, text: str, num_questions: int) -> List[Dict]:
        """Fallback method to parse questions from text"""
        questions = []
        lines = text.split('\n')
        
        current_question = {}
        options = []
        
        for line in lines:
            line = line.strip()
            if line.startswith(('Q:', 'Question:', '1.', '2.', '3.', '4.', '5.')):
                if current_question and options:
                    current_question["options"] = options
                    questions.append(current_question)
                    options = []
                current_question = {"question": line}
            elif line.startswith(('A)', 'B)', 'C)', 'D)', 'A.', 'B.', 'C.', 'D.')):
                options.append(line[2:].strip())
            elif line.startswith(('Answer:', 'Correct:')):
                current_question["correct_answer"] = line.split(':')[1].strip()
            elif line.startswith(('Explanation:', 'Explanation')):
                current_question["explanation"] = line.split(':', 1)[1].strip() if ':' in line else "No explanation provided"
        
        if current_question and options:
            current_question["options"] = options
            questions.append(current_question)
        
        return questions[:num_questions]
    
    def _create_fallback_questions(self, num_questions: int) -> List[Dict]:
        """Create fallback questions if parsing fails"""
        fallback_questions = []
        for i in range(num_questions):
            fallback_questions.append({
                "id": i + 1,
                "question": f"Sample Question {i + 1}: What is the main concept discussed in this section?",
                "options": [
                    "Concept A",
                    "Concept B", 
                    "Concept C",
                    "Concept D"
                ],
                "correct_answer": "A",
                "explanation": "This is a sample question. Please check the document processing."
            })
        return fallback_questions
    
    def quiz_conductor_agent(self, state: MCQState) -> MCQState:
        """Prepare the final MCQ set for the quiz"""
        state["final_mcqs"] = state["structured_questions"]
        state["current_question_index"] = 0
        state["user_answers"] = {}
        state["score"] = 0
        state["feedback"] = []
        return state

def create_mcq_workflow(groq_api_key: str) -> StateGraph:
    """Create the LangGraph workflow for MCQ generation"""
    
    agent = MCQAgent(groq_api_key)
    
    # Create the graph
    workflow = StateGraph(MCQState)
    
    # Add nodes
    workflow.add_node("text_processor", agent.text_processor_agent)
    workflow.add_node("mcq_generator", agent.mcq_generator_agent)
    workflow.add_node("question_validator", agent.question_validator_agent)
    workflow.add_node("quiz_conductor", agent.quiz_conductor_agent)
    
    # Add edges
    workflow.add_edge("text_processor", "mcq_generator")
    workflow.add_edge("mcq_generator", "question_validator")
    workflow.add_edge("question_validator", "quiz_conductor")
    workflow.add_edge("quiz_conductor", END)
    
    # Set entry point
    workflow.add_edge(START, "text_processor")

    return workflow.compile()