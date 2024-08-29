# Hand Tracking Project

This Projects is about using Mediapipe (a python library) to track the body, in my project the hands specifically.

## About The Project
I started with learning the basics of the hand tracking functionalities and how i can implement them in python, then I turned the code into a module so I can use it in further projects, the project focuses on the [hand landmarks](https://mediapipe.readthedocs.io/en/latest/solutions/hands.html) and how to take each land mark individually and make some cool stuff with them like controlling the volume of the pc, which needed some libraries like pycaw which works with the operating system for windows, and after that i added some features of my own for Example:
Voice activation for the Program so it does not irritate the user while running the program in the background,
you can do that by simply saying "activate volume" or "deactivate" 

## Installation

First install a virtual environment
```bash
python -m venv .venv

Activate it:

.venv/Scripts/activate  (windows)


```


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary libraries

```bash
pip install -r requirements.txt
```

## Usage

```bash
Simply run the file called VolumeHandControl.py:

python VolumeHandControl.py

Then Say: Activate Volume to run the program 
after that you can control the volume of your pc and to turn it of or just save the volume level raise the middle 
finger and you can either say deactivate to shutdown the program or just keep it running by not doing anything 
```


## License

With the help of a Youtube course: [link](https://www.youtube.com/watch?v=01sAkU_NvOY) 

Youtube Channel: [Murtaza's Workshp](https://www.youtube.com/channel/UCYUjYU5FveRAscQ8V21w81A)
