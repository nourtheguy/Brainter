import random
import pandas as pd
import requests
import os
import time
from bs4 import BeautifulSoup
import csv
from colorthief import ColorThief
import io
import pandas as pd
import requests
import datetime
from openai import OpenAI
from pathlib import Path

mode = None


def check_for_files():
    emotion_file = Path(
        "MAIN BRAINTER/ImageSketcher/node-red Files/node-red-emotion.txt"
    )
    command_file = Path(
        "MAIN BRAINTER/ImageSketcher/node-red Files/node-red-mentalcommand.txt"
    )
    if command_file.is_file():
        return "command", command_file
    elif emotion_file.is_file():
        return "emotion", emotion_file
    else:
        return "none", None


def createCSV():
    start_time = time.time()
    # converting csv of data to dataframe
    dataframe = pd.read_csv(
        "MAIN BRAINTER/ImageSketcher/emotions.txt", sep=",", header=None
    )
    dfWords = dataframe[0]
    listOfEmotions = dfWords.values.tolist()
    setOfEmotions = set(listOfEmotions)
    emotionsImages = dict()

    for emotion in setOfEmotions:
        emotionsImages[emotion] = []

        url = f"""https://www.google.com/search?q={emotion}&sxsrf=ALiCzsbU_4iqCOO_EV-A4KOIHte-_LSP_A:1667679491520&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjivMOd7pf7AhVKmokEHTv1DRkQ_AUoAXoECAEQAw&cshid=1667679510040315&biw=1512&bih=798&dpr=2"""

        urlRequest = requests.get(url)
        soup = BeautifulSoup(urlRequest.text, "html.parser")
        for item in soup.find_all("img"):
            if "gif" not in item["src"]:
                emotionsImages[emotion].append(item["src"])

    with open("MAIN BRAINTER/ImageSketcher/emotionimages.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(["Emotion", "URLs"])
        for emotion in emotionsImages:
            links = emotionsImages[emotion]
            for link in links:
                wr.writerow([emotion, link])

    print(
        f"Process scraping took {time.time() - start_time} seconds."
    )  # End measuring time


def dominantColor(url):

    response = requests.request("GET", url)  # path is a URL!
    f = io.BytesIO(response.content)
    color_thief = ColorThief(f)
    color = color_thief.get_color(quality=1)

    return color


def strToInt(r):
    result = ""
    for char in r:
        if char.isdigit():
            result += char
    return int(result)


def fixRGB(r, g, b):
    return strToInt(r), strToInt(g), strToInt(b)


def createDict():
    emotionColors = dict()
    with open("MAIN BRAINTER/ImageSketcher/emotions_images_colors.csv") as f:
        fileString = f.read()

    firstLine = True
    for line in fileString.splitlines():
        if firstLine:
            firstLine = False
            continue
        (_, emotion, _, r, g, b) = line.split(",")
        res = ""
        for chr in emotion:
            if chr.isalpha():
                res += chr
        emotion = res
        (r, g, b) = fixRGB(r, g, b)
        emotionColors[emotion] = emotionColors.get(emotion, []) + [(r, g, b)]
    return emotionColors


emotionColors = createDict()


def generateRandColors():
    createCSV()
    df = pd.read_csv("MAIN BRAINTER/ImageSketcher/emotionimages.csv")
    emotion_file = Path(
        "MAIN BRAINTER/ImageSketcher/node-red Files/node-red-emotion.txt"
    )
    randomEmotion = dict()
    emotion = emotion_file.read_text().strip()

    if emotion not in emotionColors:
        print("Sorry! We don't have that emotion. Try a different one!")
        return None  # Indicate that no valid colors were found
    else:
        # Selecting three unique indices
        indices = random.sample(range(len(emotionColors[emotion])), 3)
        selected_colors = [emotionColors[emotion][i] for i in indices]
        print(f"Selected colors for {emotion}: {selected_colors}")
        return emotion, selected_colors


# Function to initialize OpenAI client
def initialize_openai_client(api_key_file):
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as f:
            api_key = f.read().strip()
            if api_key:
                return OpenAI(api_key=api_key)
    return None


# Function to generate and save an image
def generate_and_save_image(
    client, prompt_text, size_value, model="dall-e-2", quality_value="standard"
):
    start_time = time.time()
    print(f"Generating the following prompt: {prompt_text}")
    save_dir = "MAIN BRAINTER/GCodeGenerator/Assets/Images"
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

                with open(save_path, "wb") as image_file:
                    image_file.write(image_response.content)
                print(
                    f"Process of image generation took {time.time() - start_time} seconds."
                )  # End measuring time

                print(f"Image successfully generated and saved at {save_path}")
                # Remove the file after processing to avoid reprocessing
                if mode == 2:
                    os.remove(
                        "MAIN BRAINTER/ImageSketcher/node-red Files/node-red-mentalcommand.txt"
                    )
                elif mode == 1:
                    os.remove(
                        "MAIN BRAINTER/ImageSketcher/node-red Files/node-red-emotion.txt"
                    )
            else:
                raise ValueError("Failed to download the image.")
    except Exception as e:
        print(f"Error generating image: {e}")


def process_mental_command(command_file):
    global mode
    api_key_file = "MAIN BRAINTER/ImageSketcher/openai_api_key.txt"
    client = initialize_openai_client(api_key_file)

    if client is None:
        print("Failed to initialize OpenAI client. Please check your API key.")
        return

    with open(
        "MAIN BRAINTER/ImageSketcher/node-red Files/node-red-mentalcommand.txt", "r"
    ) as file:
        prompt_text = file.read().strip()

    size_value = "256x256"
    mode = 2
    generate_and_save_image(client, prompt_text, size_value)


def process_emotion(emotion_file):
    global mode
    api_key_file = "MAIN BRAINTER/ImageSketcher/openai_api_key.txt"
    client = initialize_openai_client(api_key_file)

    if client is None:
        print("Failed to initialize OpenAI client. Please check your API key.")
        return
    # Directly use generateRandColors() to get both emotion and colors
    result = generateRandColors()  # Assuming it reads the emotion inside the function
    if result is None:
        print("Error: generateRandColors() did not return valid data.")
        return

    emotion, selected_colors = (
        result  # Unpack the result into emotion and selected_colors
    )

    if len(selected_colors) < 3:
        print("Error: Not enough colors generated.")
        return

    # Use unpacked emotion and selected_colors in the prompt
    prompt = f"Please draw me an abstract image for the emotion '{emotion}' using these three dominant colors: {selected_colors[0]}, {selected_colors[1]}, {selected_colors[2]}"
    size_value = "256x256"
    mode = 1
    generate_and_save_image(client, prompt, size_value)


if __name__ == "__main__":
    main()
