from flask import Flask, render_template, request, jsonify
import os
from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def segment_story_into_scenes(story_text):
    """
    Segments a story into scenes based on double line breaks.
    """
    if not story_text or not story_text.strip():
        return []
    scenes = story_text.split('\n\n')
    return [scene.strip() for scene in scenes if scene.strip()]

@app.route('/process_story', methods=['POST'])
def process_story():
    data = request.get_json()
    api_key = data.get('apiKey')
    ai_provider = data.get('apiProvider')
    story = data.get('story')

    if not api_key or not ai_provider:
        return jsonify({'error': 'API key and provider are required.'}), 400
    if not story:
        return jsonify({'error': 'Story text is required.'}), 400

    scenes = segment_story_into_scenes(story)
    if not scenes:
        # This implies the story was empty or only whitespace
        return jsonify({'error': 'Failed at scene segmentation. Story might be empty or in an unexpected format.'}), 500

    prompts = generate_image_prompts(scenes, api_key, ai_provider)
    if not prompts:
        # This implies scenes was empty, which is already checked, or prompt generation failed.
        return jsonify({'error': 'Failed to generate image prompts. Ensure scenes are not empty.'}), 500

    image_urls = generate_images_for_prompts(prompts, api_key, ai_provider)
    if not image_urls:
        # This implies prompts was empty or image generation failed.
        return jsonify({'error': 'Failed to generate images (placeholder step). Ensure prompts are not empty.'}), 500

    snippet_paths = create_video_snippets_from_images(image_urls)
    if not snippet_paths:
         # This implies image_urls was empty or snippet creation failed.
        return jsonify({'error': 'Failed to create video snippets. Ensure image URLs are valid and not empty.'}), 500
    
    final_video_path = stitch_video_snippets(snippet_paths)
    if not final_video_path:
        # This implies snippet_paths was empty or stitching failed.
        return jsonify({'error': 'Failed to stitch video snippets. Ensure snippets were created.'}), 500
            
    return jsonify({
        'scenes': scenes,
        'prompts': prompts,
        'image_urls': image_urls,
        'snippet_paths': snippet_paths, 
        'final_video_path': final_video_path
    })

def generate_image_prompts(scenes: list[str], api_key: str, provider: str):
    """
    Generates image prompts for each scene.
    Placeholder logic: prepends a fixed string to each scene.
    """
    # In a real application, this function would use the api_key and provider
    # to make calls to an AI image generation model.
    # For now, we're just using placeholder logic.
    if not scenes: # Added check for empty input
        return []
    prompts = [f"A vivid image of: {scene}" for scene in scenes]
    return prompts

def generate_images_for_prompts(prompts: list[str], api_key: str, provider: str):
    """
    Generates images for each prompt.
    Placeholder logic: returns a fixed placeholder image path for each prompt.
    """
    if not prompts: # Added check for empty input
        return []
    image_urls = []
    for prompt in prompts:
        print(f"Attempting to generate image for prompt: '{prompt}' using {provider} with key {api_key}")
        # Placeholder: return a path to a static image
        image_urls.append('static/placeholder_image.png')
    return image_urls

def create_video_snippets_from_images(image_paths: list[str], output_dir: str = 'static/videos') -> list[str]:
    """
    Creates video snippets from a list of image paths.
    """
    if not image_paths: # Added check for empty input
        return []
    os.makedirs(output_dir, exist_ok=True)
    snippet_paths = []
    for i, image_path in enumerate(image_paths):
        try:
            if not os.path.exists(image_path):
                print(f"Error: Image file not found at {image_path}")
                continue

            # Ensure the image is not empty
            if os.path.getsize(image_path) == 0:
                print(f"Error: Image file at {image_path} is empty.")
                # Create a dummy valid image file for moviepy to not crash
                # This is a workaround for the placeholder image being empty.
                # In a real scenario, empty images should be handled or prevented.
                from PIL import Image as PILImage
                img = PILImage.new('RGB', (100, 100), color = 'red')
                img.save(image_path)
                print(f"Created a dummy image at {image_path} to avoid moviepy error.")


            clip = ImageClip(image_path)
            clip.duration = 3  # seconds
            clip.fps = 24      # frames per second
            
            snippet_filename = f"snippet_{i}.mp4"
            snippet_filepath = os.path.join(output_dir, snippet_filename)
            
            clip.write_videofile(snippet_filepath, codec='libx264', fps=24)
            snippet_paths.append(snippet_filepath)
            print(f"Successfully created snippet: {snippet_filepath}")
        except Exception as e:
            print(f"Error creating video snippet for {image_path}: {e}")
    return snippet_paths

def stitch_video_snippets(snippet_paths: list[str], output_path: str = 'static/final_video.mp4') -> str | None:
    """
    Stitches video snippets together into a final video.
    Deletes individual snippets after successful stitching.
    """
    if not snippet_paths:
        print("Warning: No video snippets provided to stitch.")
        return None

    valid_clips = []
    for snippet_path in snippet_paths:
        try:
            if not os.path.exists(snippet_path) or os.path.getsize(snippet_path) == 0:
                print(f"Error: Snippet file is missing or empty: {snippet_path}")
                continue
            clip = VideoFileClip(snippet_path)
            valid_clips.append(clip)
        except Exception as e:
            print(f"Error loading snippet {snippet_path}: {e}. Skipping.")

    if not valid_clips:
        print("Error: No valid video clips were loaded. Cannot create final video.")
        return None

    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir: # Handle cases where output_path might be just a filename
             os.makedirs(output_dir, exist_ok=True)

        final_clip = concatenate_videoclips(valid_clips, method="compose")
        final_clip.write_videofile(output_path, codec='libx264', fps=24)
        print(f"Successfully stitched video: {output_path}")

        # Close the clips to release file handles before deleting
        for clip in valid_clips:
            clip.close()
        
        # Delete individual snippet files
        for snippet_path in snippet_paths:
            try:
                os.remove(snippet_path)
                print(f"Deleted snippet: {snippet_path}")
            except OSError as e: # More specific exception for file operations
                print(f"Error deleting snippet {snippet_path}: {e}")
        
        return output_path
    except Exception as e:
        print(f"Error during video stitching or writing: {e}")
        # Attempt to close any clips that were opened if an error occurs mid-process
        for clip in valid_clips:
            try:
                clip.close()
            except Exception:
                pass # Ignore errors on close if already in an error state
        return None

if __name__ == '__main__':
    app.run(debug=True)
