# PDF QuizMaster

PDF QuizMaster is a Streamlit application that turns uploaded documents into interactive multiple-choice quizzes. It extracts text from PDFs, TXT, and MD files, sends the content through a LangGraph workflow powered by Groq, and presents the generated questions in a timed quiz interface with scoring, explanations, progress tracking, and lifelines.

## Features

- Upload PDF, TXT, or MD documents and extract their text automatically.
- Generate MCQs from the uploaded document using Groq and LangGraph.
- Choose the quiz topic, difficulty, number of questions, and time per question.
- Answer questions in a clean dark-themed Streamlit interface.
- Use lifelines such as 50:50, Audience Poll, and Phone Friend.
- View instant explanations after each answer.
- Review a final results screen with score summary, timing stats, and performance feedback.
- Read document statistics such as character count, word count, and estimated pages.

## How It Works

1. The app reads the uploaded file and extracts text with `PyPDF2` for PDFs or direct decoding for text-based files.
2. The extracted content is validated to make sure it is long and meaningful enough for quiz generation.
3. A LangGraph workflow chunks the text, prompts Groq’s `llama-3.1-8b-instant` model, validates the returned questions, and prepares the final quiz set.
4. The Streamlit UI presents the quiz one question at a time with a countdown timer and answer tracking.
5. After completion, the app shows score breakdowns, time statistics, and a summary of quiz performance.

## Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Groq API
- PyPDF2
- Plotly
- Pandas

## Project Structure

- `app.py` - Main Streamlit entry point and quiz flow.
- `agents.py` - LangGraph workflow and MCQ generation agents.
- `document_processor.py` - File upload handling and text extraction.
- `ui_components.py` - Custom UI styling, quiz widgets, timers, lifelines, and results views.
- `requirements.txt` - Runtime dependencies.
- `setup.py` - Packaging metadata.

## Prerequisites

- Python 3.10 or newer is recommended.
- A valid Groq API key.

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.

```bash
python -m pip install -r requirements.txt
```

4. Set your Groq API key as an environment variable.

On PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

On macOS/Linux:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

## Run the App

```bash
streamlit run app.py
```

After launching, open the local Streamlit URL shown in the terminal, upload a document, configure the quiz settings, and click **Generate MCQs**.

## Usage Notes

- The app requires `GROQ_API_KEY` to be set before startup.
- Documents must contain enough text for quality quiz generation.
- Supported input files are PDF, TXT, and MD.
- If a generated question set is incomplete, the app falls back to safer default handling inside the workflow.

## Example Workflow

1. Upload a study document.
2. Set the topic and difficulty.
3. Choose the number of questions and time per question.
4. Generate the quiz.
5. Answer each question and use lifelines if needed.
6. Review the final score and performance summary.

## Troubleshooting

- If the app stops with an AI service error, verify that `GROQ_API_KEY` is set correctly.
- If no quiz is generated, make sure the uploaded document contains enough readable text.
- If a PDF is image-only or encrypted, text extraction may fail.

## License

No explicit license is included in this repository.
