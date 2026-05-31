# Local Video Hook Analyzer (Ollama MVP)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24%2B-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)
![License](https://img.shields.io/badge/License-MIT-green)

[Hebrew Version / גרסה בעברית](README.he.md)

---

A local tool for analyzing short videos and generating hook variations. This MVP focuses on **structural analysis** of video hooks using local processing, not virality prediction.

### Features

-   **Local Processing**: All processing happens locally—no external APIs or cloud services.
-   **Video Analysis**: Extracts audio and frames from video files using FFmpeg.
-   **Audio Transcription**: Uses Whisper to transcribe audio locally.
-   **Text Extraction**: Performs OCR on video frames using EasyOCR.
-   **AI-Powered Analysis**: Uses Ollama with local LLMs (e.g., `llama3.1` or `mistral`) to analyze hook structure and generate alternative hook suggestions.
-   **Hook Generation**: Generates alternative hook suggestions (e.g., Curiosity, Negative, Question).
-   **User-Friendly Interface**: Streamlit-based UI for easy interaction.

### Prerequisites

Before running this project, ensure you have the following installed:

1.  **Python 3.8+**
2.  **FFmpeg**: Required for video/audio processing.
    *   On Ubuntu: `sudo apt-get install ffmpeg`
    *   On macOS: `brew install ffmpeg`
    *   On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
3.  **Ollama**: Required for local LLM inference.
    *   Download from [ollama.ai](https://ollama.ai)
    *   After installation, pull a model: `ollama pull llama3.1` or `ollama pull mistral`

### Installation

1.  Clone or download this repository.
2.  Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  Ensure Ollama is running with a model loaded:

    ```bash
    ollama serve
    ```

    (In another terminal, you can verify with: `ollama list`)

2.  Run the Streamlit application:

    ```bash
    streamlit run app.py
    ```

3.  Open your browser and navigate to the URL provided by Streamlit (typically `http://localhost:8501`).

4.  Upload a video file (`.mp4`, `.mov`, etc.) and click "Analyze".

5.  The app will process the video and display:
    *   Original transcript
    *   Extracted on-screen text
    *   Hook structure analysis
    *   Generated alternative hooks

### Project Structure

```
video_hook_analyzer/
├── app.py                      # Main Streamlit application
├── pipeline/
│   ├── __init__.py
│   ├── video_processing.py     # FFmpeg operations
│   ├── audio_transcription.py  # Whisper transcription
│   ├── ocr_processing.py       # EasyOCR operations
│   └── llm_analysis.py         # Ollama integration
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Utility functions
├── assets/
│   └── temp/                   # Temporary processing files
├── requirements.txt            # Python dependencies
├── setup_windows.bat           # Windows setup script
└── README.md                   # This file
```

### Limitations

-   **No Virality Prediction**: This tool analyzes structure, not predicted virality.
-   **No Real Audience Data**: Analysis is based on pattern-based reasoning only.
-   **Local Resources**: Performance depends on your machine's capabilities.

### Troubleshooting

#### Ollama Connection Error

-   Ensure Ollama is running: `ollama serve`
-   Check that the model is pulled: `ollama list`

#### FFmpeg Not Found

-   Ensure FFmpeg is installed and in your system PATH.
-   Test with: `ffmpeg -version`

#### Memory Issues

-   If processing large videos, consider using shorter clips.
-   Reduce the number of frames extracted in `pipeline/video_processing.py`.

## Acknowledgments

This project was conceptualized and built with support from **Matzpen**.

### License

This project is provided as-is for educational and development purposes.
