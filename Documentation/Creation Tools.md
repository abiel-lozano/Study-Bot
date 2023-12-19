# Tools Folder

This folder contains tools that can assist in the customization of **Study-Bot**. These scripts are not required to run **Study-Bot**, but can be used for adding new topics, and testing new features.

### `ArUcoCreate.py` and `ArUcoReader.py`

These scripts are used to generate the image files of the ArUco markers from a pre-defined dictionary, and test the detection of the markers respectively.

### `ColorDetection.py`

This script is used to determine and calibrate the color ranges of the educational materials you want to detect. It will display the image from the camera, and a rectangle around the area of the image that is within the predefined color ranges.

### `PromptTesting.py`

Allows direct interaction with the chosen GPT model. This script is used to test custom instructions, source material, temperature settings, and other customizations to the GPT model. Consider that a valid **OpenAI API** key is required in a file named `credentials.py` to use this script.

### `speechGenerator.py`

This script is used to generate the audio recordings for **Study-Bot's** accessibility feature. It will convert the given text into speech, and provide the audio ID for the newly created recording, so that it can be accessed and played later. Consider that a valid **Elevenlabs API** key is required in a file named `credentials.py` to use this script to work.