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


# Function to wait for the mentalcommand.txt file to appear
def wait_for_emotions():
    print("Waiting for emotions.txt...")
    while not os.path.exists("Color Matching/emotions.txt"):
        time.sleep(1)  # Check every second for the file
    print("Found emotions.txt, proceeding with color matching.")

def writePromptToFile(emotion, colors):
    """Write the drawing prompt to a text file."""
    prompt = f"Please draw me an abstract image for the emotion '{emotion}' using these three dominant colors: {colors[0]}, {colors[1]}, {colors[2]}"
    with open('prompt.txt', 'w') as f:
        f.write(prompt)
    print("Prompt written to prompt.txt")


def createCSV():
    # converting csv of data to dataframe
    dataframe = pd.read_csv('Color Matching/emotions.txt', sep=",",header=None)
    dfWords = dataframe[0]
    listOfEmotions = dfWords.values.tolist()
    setOfEmotions = set(listOfEmotions)
    subsetOfEmotions = set(listOfEmotions[0:5])
    emotionsImages = dict()

    for emotion in setOfEmotions:
        emotionsImages[emotion] = []

        url = f'''https://www.google.com/search?q={emotion}&sxsrf=ALiCzsbU_4iqCOO_EV-A4KOIHte-_LSP_A:1667679491520&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjivMOd7pf7AhVKmokEHTv1DRkQ_AUoAXoECAEQAw&cshid=1667679510040315&biw=1512&bih=798&dpr=2'''

        urlRequest = requests.get(url)
        soup = BeautifulSoup(urlRequest.text, 'html.parser') 
        for item in soup.find_all('img'):
            if 'gif' not in item['src']:
                emotionsImages[emotion].append(item['src'])

    with open('Color Matching/emotionimages.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerow(['Emotion', 'URLs'])
        for emotion in emotionsImages:
            links = (emotionsImages[emotion])
            for link in links:
                wr.writerow([emotion, link])
    print('Scrapping Done.')


def dominantColor(url):
    response = requests.request('GET', url) # path is a URL!
    f = io.BytesIO(response.content)
    color_thief = ColorThief(f)
    color = color_thief.get_color(quality=1)
    return color
        

def strToInt(r):
    result = ''
    for char in r:
        if char.isdigit():
            result += char
    return int(result)

def fixRGB(r, g, b):
    return strToInt(r), strToInt(g), strToInt(b)

def createDict():
    emotionColors = dict()
    with open('Color Matching/emotions_images_colors.csv') as f:
        fileString = f.read()
    
    firstLine = True
    for line in fileString.splitlines():
        if firstLine:
            firstLine = False
            continue
        (_, emotion, _, r, g, b) = line.split(',')
        res = ''
        for chr in emotion:
            if chr.isalpha():
                res += chr
        emotion = res
        (r, g, b) = fixRGB(r, g, b)
        emotionColors[emotion] = emotionColors.get(emotion, []) + [(r, g, b)]
    return emotionColors

emotionColors = createDict()

def generateRandColors():
    wait_for_emotions()
    createCSV()
    df = pd.read_csv("Color Matching/emotionimages.csv")
    urls = df['URLs']
    colors = [dominantColor(url) for url in urls]
    df['color'] = colors
    df.to_csv("Color Matching/emotions_images_colors.csv")
    print('Dominant Color Done.')
    emotion = input('Enter an emotion --> ')
    randomEmotion = dict()
    emotion = emotion.lower()
    if emotion not in emotionColors:
        print("Sorry! We don't have that emotion. Try a different one!")
        return generateRandColors()
    else:
        (one, two, three) = (random.randint(1, 19), random.randint(1, 19), 
            random.randint(1, 19))
        while one == two:
            one = random.randint(1,19)
        while one == three:
            one = random.randint(1, 19)
            while two == three:
                two = random.randint(1, 19)
    randomEmotion[emotion] = [emotionColors[emotion][one], emotionColors[emotion][two],
        emotionColors[emotion][three]]
    print(randomEmotion)
    writePromptToFile()
    return randomEmotion

generateRandColors()