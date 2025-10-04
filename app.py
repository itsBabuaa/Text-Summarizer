import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import VideoUnavailable, TranscriptsDisabled
from langchain.docstore.document import Document
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()

# API Keys
#groq_api_key = st.secrets["GROQ_API_KEY"]  # For Streamlit Deployment
groq_api_key = os.getenv("GROQ_API_KEY")    # For LocalHost Testing

# Langsmith Tracking
#os.environ['LANGCHAIN_API_KEY'] = st.secrets["LANGCHAIN_API_KEY"]  # For Streamlit Deployment
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")    # For LocalHost Testing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Text Summarizer"

# LLM
llm = ChatGroq(
    groq_api_key = groq_api_key,
    model = "llama-3.1-8b-instant"
)

# prompt for 500 words summary
prompt_template = prompt_template = """
Summarize the following content in approximately 500 words. 
Structure the summary with the following sections:

Title: <A brief, catchy title for the summary>

Summary:
<Write the full summary in paragraphs, around 500 words>

Key Points:
- <Key point 1>
- <Key point 2>
- <Key point 3>
...

Content: {text}
"""

prompt_1 = PromptTemplate(
    template=prompt_template,
    input_variables= ['text']
)

# prompt for 3-Sentence summary
prompt_template_3_sentences = prompt_template_3_sentences = """
Summarize the following content in 3 concise sentences.
Structure the summary as follows:

Summary:
<Write 3 concise and informative sentences>

Content: {text}
"""


prompt_2 = PromptTemplate(
    template=prompt_template_3_sentences,
    input_variables= ['text']
)

# extract yt video ID form url
def extract_video_id(yt_url):
    parsed_url = urlparse(yt_url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    return None

# get transcript from YouTube
def transcriber(yt_url):
    video_id = extract_video_id(yt_url)
    if not video_id:
        return None, "❌Invalid YouTube URL."

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Converting the List into str
        transcript_text = " ".join([i["text"] for i in transcript_list])
        return [Document(
            page_content=transcript_text,
            metadata={"source": input_url, "video_id": video_id}
            )], None, video_id
    
    except VideoUnavailable:
        return None, "❌ Video is unavailable or private.", video_id
    except TranscriptsDisabled:
        return None, "❌ Transcripts are disabled for this video.", video_id
    except Exception as e:
        return None, f"⚠️ Unexpected error: {e}", video_id


# Streamlit UI Setup
st.set_page_config(page_icon="📝", page_title="TastyText: The Text Summarizer")
st.title("📝 TastyText: The Text Summarizer")
st.subheader("Summarize Any URL")

# Get URL from the user
input_url = st.text_input("Paste Your URL", label_visibility="collapsed")

# select summary type
summary_type = st.selectbox(
    "Select the type of summary you'd like:",
    ("✨ 3-Sentence Summary", "📄 Paragraph Summary"),
    index=0,  # 3-Sentence as default selection 
    help="Choose how detailed you want the summary to be."
)

if summary_type == "✨ 3-Sentence Summary":
    prompt = prompt_2
else:
    prompt = prompt_1


# Main
if st.button("🚀 Generate Summary", type="primary"):
    if not input_url.strip():
        st.error("⚠️ Please enter a URL!")
    elif not validators.url(input_url):
        st.error("⚠️ Please enter a Valid URL! It can be a YT URL or Website URL.")

    else:
        try:
            with st.spinner("In Progress..."):
                # Loading the YT or the web page data
                if "youtube.com" in input_url or "youtu.be" in input_url:
                    docs, yt_error, video_id = transcriber(input_url)
                    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width =True)
                    if yt_error:
                        st.error(yt_error)
                else:
                    loader=UnstructuredURLLoader(
                        urls=[input_url],
                        ssl_verify=False,
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Language": "en-US,en;q=0.9",
                        }
                    )
                    docs=loader.load()
                
                # Chain for summarization
                chain = load_summarize_chain(
                    llm= llm,
                    chain_type= "stuff",
                    prompt= prompt
                )

                output_summary= chain.run(docs)
                # Display summary
                st.markdown("## 📋 Summary")
                st.markdown(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")

# Sidebar Tips
st.sidebar.header("💡 Tips for Using TastyText")
st.sidebar.info(
    """
    📝 TastyText can summarize:

    - Any **news article**  
    - Any **blog post**  
    - Any **YouTube video** 
    - Any **WebPage URL**

    ⚡ Choose whether you want a **quick 3-sentence summary** or a **detailed paragraph summary**.  

    🚀 Simply paste the URL above and click "Generate Summary" to get a concise, structured overview!
    """
)