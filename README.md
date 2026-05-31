# Local Video Hook Analyzer (Ollama MVP)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24%2B-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)
![License](https://img.shields.io/badge/License-MIT-green)


[English](#english) | [עברית](#hebrew)

---

<a name="english"></a>

## English

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

### License

This project is provided as-is for educational and development purposes.

---

<a name="hebrew"></a>

## עברית

כלי מקומי לניתוח סרטונים קצרים ויצירת וריאציות של הוקים (Hooks). פרויקט MVP זה מתמקד ב**ניתוח מבני** של הוקים לסרטונים באמצעות עיבוד מקומי, ולא בחיזוי ויראליות.

### תכונות

-   **עיבוד מקומי**: כל העיבוד מתבצע באופן מקומי – ללא ממשקי API חיצוניים או שירותי ענן.
-   **ניתוח וידאו**: מחלץ אודיו ופריימים מקבצי וידאו באמצעות FFmpeg.
-   **תמלול אודיו**: משתמש ב-Whisper לתמלול אודיו באופן מקומי.
-   **חילוץ טקסט**: מבצע זיהוי תווים אופטי (OCR) על פריימים של וידאו באמצעות EasyOCR.
-   **ניתוח מבוסס AI**: משתמש ב-Ollama עם מודלי LLM מקומיים (לדוגמה, `llama3.1` או `mistral`) לניתוח מבנה ההוק ויצירת הצעות חלופיות להוקים.
-   **יצירת הוקים**: מייצר הצעות חלופיות להוקים (לדוגמה, סקרנות, שלילי, שאלה).
-   **ממשק משתמש ידידותי**: ממשק מבוסס Streamlit לאינטראקציה קלה.

### דרישות קדם

לפני הפעלת פרויקט זה, ודא שהרכיבים הבאים מותקנים:

1.  **Python 3.8+**
2.  **FFmpeg**: נדרש לעיבוד וידאו/אודיו.
    *   באובונטו: `sudo apt-get install ffmpeg`
    *   ב-macOS: `brew install ffmpeg`
    *   ב-Windows: הורד מ-[ffmpeg.org](https://ffmpeg.org/download.html)
3.  **Ollama**: נדרש להסקת LLM מקומית.
    *   הורד מ-[ollama.ai](https://ollama.ai)
    *   לאחר ההתקנה, משוך מודל: `ollama pull llama3.1` או `ollama pull mistral`

### התקנה

1.  שכפל או הורד את המאגר.
2.  צור סביבה וירטואלית:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # ב-Windows: venv\Scripts\activate
    ```

3.  התקן תלויות:

    ```bash
    pip install -r requirements.txt
    ```

### שימוש

1.  ודא ש-Ollama פועל עם מודל טעון:

    ```bash
    ollama serve
    ```

    (בטרמינל אחר, תוכל לוודא זאת באמצעות: `ollama list`)

2.  הפעל את יישום Streamlit:

    ```bash
    streamlit run app.py
    ```

3.  פתח את הדפדפן שלך ונווט לכתובת ה-URL המסופקת על ידי Streamlit (בדרך כלל `http://localhost:8501`).

4.  העלה קובץ וידאו (`.mp4`, `.mov` וכו') ולחץ על "Analyze".

5.  היישום יעבד את הווידאו ויציג:
    *   תמלול מקורי
    *   טקסט שחולץ מהמסך
    *   ניתוח מבנה ההוק
    *   הוקים חלופיים שנוצרו

### מבנה הפרויקט

```
video_hook_analyzer/
├── app.py                      # יישום Streamlit ראשי
├── pipeline/
│   ├── __init__.py
│   ├── video_processing.py     # פעולות FFmpeg
│   ├── audio_transcription.py  # תמלול Whisper
│   ├── ocr_processing.py       # פעולות EasyOCR
│   └── llm_analysis.py         # אינטגרציית Ollama
├── utils/
│   ├── __init__.py
│   └── helpers.py              # פונקציות עזר
├── assets/
│   └── temp/                   # קבצי עיבוד זמניים
├── requirements.txt            # תלויות Python
├── setup_windows.bat           # סקריפט התקנה ל-Windows
└── README.md                   # קובץ זה
```

### מגבלות

-   **אין חיזוי ויראליות**: כלי זה מנתח מבנה, לא ויראליות צפויה.
-   **אין נתוני קהל אמיתיים**: הניתוח מבוסס על היגיון מבוסס תבניות בלבד.
-   **משאבים מקומיים**: הביצועים תלויים ביכולות המחשב שלך.

### פתרון בעיות

#### שגיאת חיבור ל-Ollama

-   ודא ש-Ollama פועל: `ollama serve`
-   ודא שהמודל נמשך: `ollama list`

#### FFmpeg לא נמצא

-   ודא ש-FFmpeg מותקן ונמצא בנתיב המערכת שלך (PATH).
-   בדוק עם: `ffmpeg -version`

#### בעיות זיכרון

-   אם מעבדים סרטונים גדולים, שקול להשתמש בקליפים קצרים יותר.
-   הפחת את מספר הפריימים הנחלצים ב-`pipeline/video_processing.py`.

### רישיון

פרויקט זה מסופק כפי שהוא למטרות חינוכיות ופיתוח.

## Acknowledgments

This project was conceptualized and built with support from **Matzpen**.
