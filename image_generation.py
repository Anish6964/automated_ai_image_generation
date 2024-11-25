import requests
import math

#  API key
API_KEY = "31bee9d0-5c3a-45f8-bcc2-92abb354c457"


# Step 1: Read the Video Script
def read_script(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""


# Step 2: Split Script into Scenes
def split_script_into_scenes(script, num_scenes):
    # Remove extra spaces and split the script into lines
    lines = [line.strip() for line in script.split("\n") if line.strip()]

    # Calculate how many lines per scene
    lines_per_scene = math.ceil(len(lines) / num_scenes)

    # Group lines into distinct scenes
    scenes = [
        " ".join(lines[i : i + lines_per_scene])
        for i in range(0, len(lines), lines_per_scene)
    ]

    print(f"Script split into {len(scenes)} scenes.")
    return scenes


# Step 3: Split Long Scenes into Smaller Chunks
def split_large_scene(scene, max_length=1500):
    words = scene.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1  # +1 for the space
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# Step 4: Create an Image Generation for Each Scene
def create_image_for_scene(scene, model_id="6bef9f1b-29cb-40c7-b9df-32b51c1f67d3"):
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}",
    }
    payload = {"height": 512, "modelId": model_id, "prompt": scene, "width": 512}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        generation_id = data.get("sdGenerationJob", {}).get("generationId")
        if generation_id:
            print(f"Generation ID for scene '{scene[:50]}...': {generation_id}")
            return generation_id
        else:
            print(f"No generation ID returned for scene: '{scene[:50]}...'")
    else:
        print(
            f"Error for scene '{scene[:50]}...': {response.status_code} - {response.text}"
        )
    return None


# Step 5: Process the Video Script and Generate Images
def process_script(file_path):
    # Read the script
    script = read_script(file_path)
    if not script:
        print("The script is empty or could not be read.")
        return

    # Ask user for the number of images
    try:
        num_images = int(input("Enter the number of images (scenes) to generate: "))
        if num_images <= 0:
            print("Number of images must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a positive integer.")
        return

    # Split the script into scenes
    scenes = split_script_into_scenes(script, num_images)

    # Process each scene
    for i, scene in enumerate(scenes):
        print(f"Processing scene {i + 1}/{len(scenes)}: {scene[:50]}...")

        # Split long scenes into smaller chunks
        sub_scenes = split_large_scene(scene)
        for j, sub_scene in enumerate(sub_scenes):
            print(f"Processing sub-scene {j + 1}/{len(sub_scenes)} of scene {i + 1}...")
            generation_id = create_image_for_scene(sub_scene)
            if generation_id:
                print(f"Image generation successful for sub-scene {j + 1}")
            else:
                print(f"Failed to generate image for sub-scene {j + 1}")


# Main Execution
if __name__ == "__main__":
    script_file_path = (
        "Social_engineering.txt"  # Replace with your video script file
    )
    process_script(script_file_path)
