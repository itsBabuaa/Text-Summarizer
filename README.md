# 📝 TastyText: The Text Summarizer

TastyText is a **Streamlit-based web app** that can summarize content from **news articles, blog posts, YouTube videos, or any webpage**. Using powerful LLMs via Groq and LangChain, it provides either a **quick 3-sentence summary** or a **detailed paragraph summary with key points**.

---

## 🚀 Features

- Summarize any **news article** or **blog post**.
- Summarize **YouTube videos** by automatically extracting transcripts.
- Two summary modes:
  - **✨ 3-Sentence Summary**: Quick, concise overview.
  - **📄 Paragraph Summary**: Detailed summary (~500 words) with key points.
- Clean, structured output with **titles, paragraphs, and bullet points**.
- User-friendly **Streamlit interface** with sidebar tips.

---

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/itsBabuaa/Text-Summarizer.git
cd Text-Summarizer
````

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
   Create a `.env` file in the project root and add:

```
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
```

---

## 🖥️ Usage

1. Run the Streamlit app:

```bash
streamlit run app.py
```

2. Paste a **URL** of a webpage, blog, news article, or YouTube video.
3. Select the type of summary:

   * **3-Sentence Summary**
   * **Paragraph Summary**
4. Click **"Generate Summary"** to view the output.

The app also displays a **YouTube thumbnail** for video URLs.

---

## 💡 Tips

* Works best with **publicly accessible URLs**.
* Supports **any language supported by YouTube transcripts** or web pages.
* Use the **sidebar tips** in the app for quick guidance.

---

## 🔧 Dependencies

* `streamlit`
* `validators`
* `python-dotenv`
* `youtube-transcript-api`
* `langchain`
* `langchain-groq`
* `langchain-community`
* `unstructured`
