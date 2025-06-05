# Autonomous Hypothesis Generator

An AI-powered system that continuously generates and verifies scientific hypotheses using Gemini AI.

## Features

- 🔄 Continuous hypothesis generation
- 🤖 AI-powered verification using Gemini
- 📊 Real-time visualization and statistics
- 🔍 Search functionality by hypothesis ID
- 💾 Automatic saving of hypotheses
- ⏯️ Pause/Resume system control

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
   - Get your API key from Google AI Studio
   - The key is already configured in the code

3. Run the application:
```bash
streamlit run frontend/app.py
```

## Usage

1. The system starts automatically and begins generating hypotheses
2. Use the sidebar to:
   - Pause/Resume the system
   - Search for specific hypotheses by ID
3. View real-time statistics and visualizations in the main interface
4. All hypotheses are automatically saved to `backend/hypotheses.txt`

## System Architecture

- Frontend: Streamlit web interface
- Backend: Python-based hypothesis generator
- Storage: Local file system
- AI: Google's Gemini API

## Error Handling

The system includes robust error handling for:
- API failures
- Network issues
- Invalid responses
- File system errors

## Contributing

Feel free to submit issues and enhancement requests!

## Project Structure

```
├── frontend/
│   └── app.py
├── backend/
│   └── hypothesis_generator.py
├── requirements.txt
└── README.md
```

## Note

The application uses the Gemini API for hypothesis generation. Make sure you have a valid API key configured. 
