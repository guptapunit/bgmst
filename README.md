# Story-to-Reel Video Generator

## Overview
This application allows users to input a story, which is then processed to generate a video suitable for social media reels. It breaks the story into scenes, prepares image prompts, (currently) uses placeholders for image generation, creates video snippets from these images, and finally stitches them into a single video.

## Features
-   Web-based interface for story input and configuration.
-   Story segmentation into scenes.
-   (Placeholder) Image prompt generation for each scene.
-   (Placeholder) Image generation for each prompt.
-   Creation of video snippets from images using `moviepy`.
-   Stitching of video snippets into a final MP4 video.
-   Configuration for AI API provider and key (stored locally in browser).

## Tech Stack
-   **Backend:** Python, Flask
-   **Video Processing:** moviepy
-   **Frontend:** HTML, CSS, JavaScript
-   **Dependencies:** Pillow (for image handling with moviepy)

## Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    flask run
    # Or: python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000`.

## Usage Instructions
1.  Open your web browser and navigate to `http://127.0.0.1:5000`.
2.  **Story Input:** Enter your story text into the large text area.
3.  **API Configuration:**
    *   **API Key:** Enter the API key for your chosen AI service.
    *   **API Provider:** Select the AI provider (e.g., OpenAI, GoogleAI) from the dropdown.
    *   *Note: API keys are stored in your browser's local storage for convenience. Do not use this application on shared or public computers if you are using real API keys.*
4.  Click the "**Generate Video**" button.
5.  The application will process the story. A loading indicator will be shown.
6.  Once complete, a video player will appear with the generated video, and a download link will be available.
7.  If errors occur, an error message will be displayed.

## Unit Testing - Areas for Improvement
The following functions in `app.py` are good candidates for unit tests:

-   **`segment_story_into_scenes(story_text)`:**
    -   Test with an empty story string.
    -   Test with a story containing a single paragraph.
    -   Test with a story containing multiple paragraphs (separated by `\n\n`).
    -   Test with leading/trailing whitespace in the story or paragraphs.
-   **`generate_image_prompts(scenes, api_key, provider)` (current placeholder logic):**
    -   Test with an empty list of scenes.
    -   Test with a list of one or more scenes to ensure the placeholder prefix is correctly added.
-   **`create_video_snippets_from_images(image_paths)`:**
    -   Test with an empty list of `image_paths`.
    -   Test with a list containing a valid path to the placeholder image.
    -   Test with a list containing an invalid or non-existent image path (should be skipped gracefully).
    -   Test if output video snippet files are created in the correct directory.
-   **`stitch_video_snippets(snippet_paths)`:**
    -   Test with an empty list of `snippet_paths`.
    -   Test with a list of paths to valid (placeholder) video snippets.
    -   Test if the final video is created at the specified output path.
    -   Test if individual snippet files are deleted after successful stitching.
    -   Test with some invalid snippet paths (should be handled gracefully).

## Current Limitations / Future Work
-   **Placeholder AI Integration:** The core AI-driven functionalities (scene understanding beyond paragraph splitting, image prompt generation from scenes, and actual image generation from prompts) currently use simple placeholders. The next major step is to integrate real AI APIs (e.g., Google Gemini, OpenAI GPT for text tasks; OpenAI DALL-E, Google Imagen for image generation).
-   **Basic Scene Segmentation:** Scene segmentation currently relies on paragraph breaks. More advanced NLP techniques or LLM calls should be used for better contextual understanding and scene division.
-   **Video Snippet Animation:** Video snippets are currently static images with a fixed duration. Future enhancements could include image animation (e.g., Ken Burns effect, parallax) within each snippet.
-   **Advanced UI/UX:** The user interface is basic. It could be improved with more interactive elements, progress updates for each step, and better styling.
-   **Background Processing:** For longer stories or many scenes, video generation can be time-consuming. Implementing background tasks (e.g., using Celery with Flask) would improve responsiveness.
```
