import streamlit as st
import json
import os
from pipeline.interpreter import generate_scene_breakdown
from pipeline.generator import generate_manim_code
from pipeline.renderer import render_scene

st.set_page_config(page_title="Text-Driven Educational Animation", layout="wide")

st.title("Text-Driven Educational Animation Video Generator")
st.markdown("### Convert Natural Language to Manim Animations")

# Sidebar for configuration
st.sidebar.header("Pipeline Status")
step1_status = st.sidebar.empty()
step2_status = st.sidebar.empty()
step3_status = st.sidebar.empty()

# Input
prompt = st.text_area("Enter your animation request:", "Show a blue circle growing from the center and then transforming into a square.")

if st.button("Generate Animation"):
    if not prompt:
        st.error("Please enter a prompt.")
    else:
        # Phase 1: Interpretation
        step1_status.info("Phase 1: Interpreting...")
        with st.spinner("Interpreting request with Gemini..."):
            scene_data = generate_scene_breakdown(prompt)
        
        if not scene_data:
            step1_status.error("Phase 1 Failed")
            st.error("Failed to interpret prompt.")
        else:
            step1_status.success("Phase 1 Complete")
            st.subheader("Phase 1: Scene Breakdown (JSON)")
            st.json(scene_data)
            
            # Phase 2: Code Generation
            step2_status.info("Phase 2: Generating Code...")
            with st.spinner("Generating Manim code with Local SLM..."):
                manim_code = generate_manim_code(scene_data)
            
            if not manim_code:
                step2_status.error("Phase 2 Failed")
                st.error("Failed to generate code.")
            else:
                step2_status.success("Phase 2 Complete")
                st.subheader("Phase 2: Generated Manim Code")
                st.code(manim_code, language='python')
                
                # Phase 3: Rendering
                step3_status.info("Phase 3: Rendering...")
                
                # Self-Correction Loop
                max_retries = 3
                attempt = 0
                success = False
                current_code = manim_code
                
                while attempt < max_retries and not success:
                    with st.spinner(f"Rendering video (Attempt {attempt + 1}/{max_retries})..."):
                        video_path, error_msg = render_scene(current_code, "generated_video.mp4")
                    
                    if video_path and os.path.exists(video_path):
                        success = True
                        step3_status.success("Phase 3 Complete")
                        st.subheader("Phase 3: Final Video")
                        st.video(video_path)
                        st.success("Animation generated successfully!")
                    else:
                        attempt += 1
                        if attempt < max_retries:
                            st.warning(f"Rendering failed (Attempt {attempt}). Auto-fixing code...")
                            from pipeline.generator import fix_manim_code
                            with st.spinner("Auto-debugging code..."):
                                current_code = fix_manim_code(current_code, error_msg)
                            st.subheader(f"Fixed Code (Attempt {attempt + 1})")
                            st.code(current_code, language='python')
                        else:
                            step3_status.error("Phase 3 Failed")
                            st.error("Failed to render video after multiple attempts.")
                            st.error(f"Last Error: {error_msg}")
