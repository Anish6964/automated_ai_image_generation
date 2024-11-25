"""
# AI Script-to-Image Generator

This project processes a video script, splits it into distinct scenes, and generates images for each scene using the Leonardo AI API. It dynamically handles long scripts, balances scene lengths, and ensures no scene exceeds the prompt limit of 1500 characters.

---

## Features
- **Script Upload**: Accepts a `.txt` file containing the video script.
- **Dynamic Scene Splitting**: Allows the user to specify the number of scenes (images) to generate.
- **Character Limit Handling**: Automatically splits scenes exceeding 1500 characters into sub-scenes.
- **AI Image Generation**: Generates unique images for each scene using Leonardo AI API.
- **Logs Generation IDs**: Provides a unique `generationId` for tracking each image in the Leonardo AI dashboard.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Anish6964/automated_ai_image_generation.git
   cd SocialEngineering
