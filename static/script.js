document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const storyTextarea = document.getElementById('story');
    const apiKeyInput = document.getElementById('apiKey');
    const apiProviderSelect = document.getElementById('apiProvider');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorDisplay = document.getElementById('errorDisplay');
    const finalVideo = document.getElementById('finalVideo');
    const videoPlaceholder = document.getElementById('videoPlaceholder'); // To hide it when video loads
    const downloadLink = document.getElementById('downloadLink');

    // Load API config from LocalStorage
    apiKeyInput.value = localStorage.getItem('apiKey') || '';
    apiProviderSelect.value = localStorage.getItem('apiProvider') || 'OpenAI'; // Default to OpenAI

    generateBtn.addEventListener('click', async () => {
        const story = storyTextarea.value.trim();
        const apiKey = apiKeyInput.value.trim();
        const apiProvider = apiProviderSelect.value;

        // Store API config in LocalStorage
        localStorage.setItem('apiKey', apiKey);
        localStorage.setItem('apiProvider', apiProvider);

        if (!story) {
            errorDisplay.textContent = 'Please enter a story.';
            return;
        }
        if (!apiKey) {
            errorDisplay.textContent = 'Please enter your API key.';
            return;
        }
        if (!apiProvider) {
            errorDisplay.textContent = 'Please select an API provider.';
            return;
        }

        loadingIndicator.style.display = 'block';
        errorDisplay.textContent = '';
        finalVideo.style.display = 'none';
        downloadLink.style.display = 'none';
        videoPlaceholder.style.display = 'flex'; // Reset placeholder

        try {
            const response = await fetch('/process_story', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    story: story,
                    apiKey: apiKey,
                    apiProvider: apiProvider,
                }),
            });

            if (!response.ok) {
                let errorMsg = `HTTP error! status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.error || errorMsg;
                } catch (e) {
                    // If parsing JSON fails, use the statusText or the generic message
                    errorMsg = response.statusText || errorMsg;
                }
                errorDisplay.textContent = errorMsg; // Display error in #errorDisplay
                throw new Error(errorMsg); // Still throw to stop further processing in try block
            }

            const data = await response.json();

            if (data.error) {
                errorDisplay.textContent = `Error: ${data.error}`;
            } else if (data.final_video_path) {
                finalVideo.src = data.final_video_path + `?t=${new Date().getTime()}`; // Cache busting
                finalVideo.style.display = 'block';
                videoPlaceholder.style.display = 'none'; // Hide placeholder

                downloadLink.href = data.final_video_path;
                downloadLink.download = 'story_video.mp4';
                downloadLink.style.display = 'inline-block';
            } else {
                errorDisplay.textContent = 'An unexpected error occurred: No video path received, and no error reported.';
            }
        } catch (error) {
            console.error('Fetch processing error:', error);
            // If errorDisplay is not already set by a !response.ok block, set it.
            if (!errorDisplay.textContent) {
                 errorDisplay.textContent = `Failed to generate video. ${error.message || 'Please check console for details.'}`;
            }
        } finally {
            loadingIndicator.style.display = 'none';
        }
    });
});
