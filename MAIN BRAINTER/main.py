from ImageSketcher.Imagesketchermodule import *
from GCodeGenerator.TopG import *
import time


def main():
    start = time.time()
    # generates an image after receiving a text file from node red
    print("Waiting for the necessary information")
    # while True:
    #     status, file_path = check_for_files()
    #     if status == "command":
    #         print("Start mental command process.")
    #         process_mental_command(file_path)
    #         print("Finished mental command process.")
    #         break
    #     elif status == "emotion":
    #         print("Start emotion color matching process.")
    #         process_emotion(file_path)
    #         print("Finished emotion color matching  process.")
    #         break
    TopG()
    end = time.time()
    print("Total time taken = " + str(end - start) + " seconds")


if __name__ == "__main__":
    main()
