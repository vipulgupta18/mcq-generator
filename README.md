# PDF QuizMaster

PDF QuizMaster is a Streamlit app that generates interactive multiple-choice quizzes from uploaded documents. It extracts text from PDFs and text files, processes the content through a LangGraph workflow powered by Groq, and presents the result in a timed quiz interface with scoring, explanations, lifelines, and performance feedback.

## Features

- Upload PDF, TXT, or MD files and extract text automatically.
- Generate MCQs with Groq through a LangGraph-based workflow.
- Configure the topic, difficulty, number of questions, and time per question.
- Answer questions in a dark-themed, responsive Streamlit UI.
- Use quiz lifelines: 50:50, Audience Poll, and Phone Friend.
- Review instant explanations after each submission.
- See a final score summary with timing and accuracy statistics.
- View document metrics such as character count, word count, and estimated pages.

## How It Works

1. The uploaded file is processed by `document_processor.py`.
2. PDFs are read with `PyPDF2`; text files are decoded with common encodings.
3. The extracted text is validated to ensure it is suitable for quiz generation.
4. `agents.py` chunks the text, prompts Groq’s `llama-3.1-8b-instant` model, and validates the returned questions.
5. `app.py` renders the quiz, tracks answers, handles the timer, and shows final results.

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
- `agents.py` - LangGraph workflow and MCQ generation logic.
- `document_processor.py` - File handling and text extraction.
- `ui_components.py` - Custom UI styling, quiz controls, timers, lifelines, and results views.
- `requirements.txt` - Runtime dependencies.
- `setup.py` - Packaging metadata.
- `.env.example` - Example environment file for local configuration.

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.

```bash
python -m pip install -r requirements.txt
```

4. Create a `.env` file in the project root.

You can copy `.env.example` and replace the placeholder value:

```env
GROQ_API_KEY=your_api_key_here
```

If you prefer setting the variable directly in PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

## Run the App

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, upload a document, choose your quiz settings, and click **Generate MCQs**.

## Usage Notes

- The app will stop if `GROQ_API_KEY` is missing.
- Documents must contain enough meaningful text for good quiz generation.
- Supported file types are PDF, TXT, and MD.
- If the model output is incomplete, the workflow falls back to safer structured handling.

## Example Workflow

1. Upload a study document.
2. Enter a topic and choose a difficulty level.
3. Pick the number of questions and the timer length.
4. Generate the quiz.
5. Answer each question and use lifelines if needed.
6. Review the final results screen.

## Troubleshooting

- If the app reports a missing AI configuration, confirm that `GROQ_API_KEY` is set.
- If MCQs are not generated, make sure the uploaded document has enough readable text.
- If a PDF is encrypted or image-only, extraction may fail.

## License

No license file is included in this repository.
