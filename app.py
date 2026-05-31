"""
Video Hook Analyzer - Main Streamlit Application
A local tool for analyzing short videos and generating hook variations.
"""

import os
import streamlit as st
import tempfile
from pathlib import Path

# Import pipeline modules
from pipeline import video_processing, audio_transcription, ocr_processing, llm_analysis
from utils import helpers


# Configure Streamlit page
st.set_page_config(
    page_title="Video Hook Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .status-success {
        color: #2ecc71;
        font-weight: bold;
    }
    .status-error {
        color: #e74c3c;
        font-weight: bold;
    }
    .hook-card {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "results" not in st.session_state:
        st.session_state.results = None
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = helpers.get_temp_directory()


def check_dependencies():
    """Check if all required dependencies are available."""
    dependencies = {
        "FFmpeg": video_processing.check_ffmpeg_installed(),
        "Whisper": audio_transcription.check_whisper_available(),
        "EasyOCR": ocr_processing.check_easyocr_available(),
        "Ollama": llm_analysis.check_ollama_available()
    }
    return dependencies


def display_dependency_status(dependencies):
    """Display the status of dependencies."""
    st.sidebar.markdown("### 📋 Dependencies Status")
    
    all_available = True
    for dep_name, available in dependencies.items():
        status = "✅ Available" if available else "❌ Missing"
        status_color = "status-success" if available else "status-error"
        st.sidebar.markdown(f"<span class='{status_color}'>{dep_name}: {status}</span>", unsafe_allow_html=True)
        if not available:
            all_available = False
    
    if not all_available:
        st.sidebar.warning(
            "⚠️ Some dependencies are missing. Please install them before proceeding. "
            "See README.md for setup instructions."
        )
    
    return all_available


def process_video(video_file):
    """Process the uploaded video through the pipeline."""
    try:
        # Create a temporary directory for this session
        session_temp_dir = os.path.join(st.session_state.temp_dir, helpers.generate_session_id())
        helpers.ensure_directory_exists(session_temp_dir)
        
        # Save uploaded file
        video_path = os.path.join(session_temp_dir, video_file.name)
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        
        st.info(f"📁 Video saved: {video_file.name}")
        
        # Step 1: Extract audio and frames
        with st.status("🎵 Extracting audio and frames...", expanded=True) as status:
            audio_path = os.path.join(session_temp_dir, "audio.mp3")
            frames_dir = os.path.join(session_temp_dir, "frames")
            
            audio_success = video_processing.extract_audio(video_path, audio_path, duration=15)
            frames = video_processing.extract_frames(video_path, frames_dir, duration=15, fps=1)
            
            if audio_success:
                st.write("✅ Audio extracted successfully")
            else:
                st.error("❌ Failed to extract audio")
            
            if frames:
                st.write(f"✅ Extracted {len(frames)} frames")
            else:
                st.warning("⚠️ No frames extracted")
            
            status.update(label="✅ Audio and frames extracted", state="complete")
        
        # Step 2: Transcribe audio
        with st.status("🎙️ Transcribing audio...", expanded=True) as status:
            transcription_result = None
            if audio_success:
                transcription_result = audio_transcription.transcribe_audio(audio_path, model_size="base")
                if transcription_result:
                    transcript_text = transcription_result.get("text", "")
                    st.write(f"✅ Transcription complete")
                    st.write(f"📝 Text preview: {helpers.truncate_text(transcript_text, 150)}")
                else:
                    st.error("❌ Transcription failed")
            else:
                st.warning("⚠️ Skipping transcription (no audio extracted)")
            
            status.update(label="✅ Audio transcribed", state="complete")
        
        # Step 3: Perform OCR on frames
        with st.status("👁️ Extracting text from frames (OCR)...", expanded=True) as status:
            ocr_result = None
            if frames:
                ocr_result = ocr_processing.perform_ocr_on_frames(frames, languages=["en"])
                if ocr_result:
                    ocr_text = ocr_result.get("text", "")
                    st.write(f"✅ OCR complete")
                    if ocr_text.strip():
                        st.write(f"📝 Text preview: {helpers.truncate_text(ocr_text, 150)}")
                    else:
                        st.write("ℹ️ No text found in frames")
                else:
                    st.error("❌ OCR failed")
            else:
                st.warning("⚠️ Skipping OCR (no frames extracted)")
            
            status.update(label="✅ Text extracted from frames", state="complete")
        
        # Step 4: Analyze hook structure
        with st.status("🔍 Analyzing hook structure...", expanded=True) as status:
            transcript_text = audio_transcription.get_transcription_text(transcription_result)
            ocr_text = ocr_processing.get_ocr_text(ocr_result)
            
            analysis_result = llm_analysis.analyze_hook_structure(transcript_text, ocr_text, model="llama3.1")
            if analysis_result:
                st.write("✅ Hook analysis complete")
            else:
                st.error("❌ Hook analysis failed")
            
            status.update(label="✅ Hook structure analyzed", state="complete")
        
        # Step 5: Generate alternative hooks
        with st.status("✨ Generating alternative hooks...", expanded=True) as status:
            hooks_result = llm_analysis.generate_alternative_hooks(transcript_text, ocr_text, num_hooks=3, model="llama3.1")
            if hooks_result:
                st.write("✅ Alternative hooks generated")
            else:
                st.error("❌ Hook generation failed")
            
            status.update(label="✅ Alternative hooks generated", state="complete")
        
        # Compile results
        results = {
            "transcript": transcript_text,
            "ocr_text": ocr_text,
            "analysis": llm_analysis.get_analysis_text(analysis_result),
            "hooks": llm_analysis.get_generated_hooks(hooks_result),
            "session_dir": session_temp_dir
        }
        
        return results
    
    except Exception as e:
        st.error(f"❌ Error processing video: {str(e)}")
        return None


def display_results(results):
    """Display the analysis results."""
    if not results:
        return
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Display transcript
    st.markdown("### 📝 Transcript")
    transcript = results.get("transcript", "")
    if transcript:
        st.text_area("Original Transcript:", value=transcript, height=100, disabled=True)
    else:
        st.info("No transcript available")
    
    # Display OCR text
    st.markdown("### 👁️ On-Screen Text (OCR)")
    ocr_text = results.get("ocr_text", "")
    if ocr_text:
        st.text_area("Extracted Text:", value=ocr_text, height=100, disabled=True)
    else:
        st.info("No on-screen text detected")
    
    # Display hook analysis
    st.markdown("### 🔍 Hook Structure Analysis")
    analysis = results.get("analysis", {})
    if analysis:
        if isinstance(analysis, dict):
            for key, value in analysis.items():
                st.markdown(f"**{key.replace('_', ' ').title()}:**")
                st.write(value)
        else:
            st.write(analysis)
    else:
        st.info("No analysis available")
    
    # Display generated hooks
    st.markdown("### ✨ Generated Alternative Hooks")
    hooks = results.get("hooks", [])
    if hooks:
        for idx, hook in enumerate(hooks, 1):
            hook_type = hook.get("type", "Generated")
            hook_text = hook.get("hook", "")
            st.markdown(f"""
            <div class="hook-card">
                <strong>{idx}. {hook_type} Hook:</strong><br/>
                {hook_text}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No alternative hooks generated")


def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Video Hook Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("Analyze your video hooks and generate engaging alternatives using local AI.")
    
    # Check dependencies
    dependencies = check_dependencies()
    all_available = display_dependency_status(dependencies)
    
    if not all_available:
        st.error("⚠️ Please install missing dependencies before proceeding. See README.md for instructions.")
        return
    
    # Main content
    st.markdown("---")
    
    # File upload
    st.markdown("### 📤 Upload Video")
    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "mov", "avi", "mkv", "flv", "wmv", "webm", "m4v"],
        help="Supported formats: MP4, MOV, AVI, MKV, FLV, WMV, WEBM, M4V"
    )
    
    # Process button
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🚀 Analyze Video", use_container_width=True):
                st.session_state.processing = True
                st.session_state.results = process_video(uploaded_file)
                st.session_state.processing = False
        
        with col2:
            st.info("Click 'Analyze Video' to process your video and generate hook variations.")
    
    # Display results
    if st.session_state.results:
        display_results(st.session_state.results)
        
        # Cleanup button
        if st.button("🗑️ Clear Results & Cleanup", use_container_width=False):
            session_dir = st.session_state.results.get("session_dir", "")
            if session_dir and os.path.exists(session_dir):
                import shutil
                try:
                    shutil.rmtree(session_dir)
                    st.success("✅ Temporary files cleaned up")
                except Exception as e:
                    st.warning(f"⚠️ Could not clean up all files: {str(e)}")
            
            st.session_state.results = None
            st.rerun()
    
    # --- Footer ---
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888888; font-size: 14px; margin-top: 20px;'>"
        "Built with support from <b>Matzpen</b>"
        "</div>", 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
