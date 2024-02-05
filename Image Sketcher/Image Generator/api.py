import os
import requests
import datetime
import time
from openai import OpenAI

# Function to initialize OpenAI client
def initialize_openai_client(api_key_file):
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
            if api_key:
                return OpenAI(api_key=api_key)
    return None

# Function to generate and save an image
def generate_and_save_image(client, prompt_text, size_value, model="dall-e-2", quality_value="standard"):
    save_dir = "Image Generator/generated_images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        response = client.images.generate(
            model=model,
            prompt=prompt_text,
            size=size_value,
            quality=quality_value,
        )

        if response.data and isinstance(response.data, list):
            image_url = response.data[0].url
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                save_path = f"{save_dir}/brainter.png"

                with open(save_path, 'wb') as image_file:
                    image_file.write(image_response.content)
                print(f"Image successfully generated and saved at {save_path}")
                # Remove the file after processing to avoid reprocessing
                os.remove("Image Generator/mentalcommand.txt")
            else:
                raise ValueError("Failed to download the image.")
    except Exception as e:
        print(f"Error generating image: {e}")

# Function to wait for the mentalcommand.txt file to appear
def wait_for_mental_command():
    print("Waiting for mentalcommand.txt...")
    while not os.path.exists("Image Generator/mentalcommand.txt"):
        time.sleep(1)  # Check every second for the file
    print("Found mentalcommand.txt, proceeding with image generation.")

    with open("Image Generator/mentalcommand.txt", "r") as file:
        prompt_text = file.read().strip()
    return prompt_text

# Main execution function
def main():
    api_key_file = "Image Generator/openai_api_key.txt"
    client = initialize_openai_client(api_key_file)

    if client is None:
        print("Failed to initialize OpenAI client. Please check your API key.")
        return

    # Wait for the mental command file and read the prompt
    prompt_text = wait_for_mental_command()
    size_value = "256x256"
    generate_and_save_image(client, prompt_text, size_value)

if __name__ == "__main__":
    main()
