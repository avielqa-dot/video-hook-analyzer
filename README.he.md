# Local Video Hook Analyzer (Ollama MVP) - עברית

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24%2B-red)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)
![License](https://img.shields.io/badge/License-MIT-green)

[English Version](README.md)

---

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

## Acknowledgments

This project was conceptualized and built with support from **Matzpen**.

### רישיון

פרויקט זה מסופק כפי שהוא למטרות חינוכיות ופיתוח.
