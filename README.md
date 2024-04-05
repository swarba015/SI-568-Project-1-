#  Project 1: Data Science: The Light of Information
### Overview
Team Lake, consisting of Nuzhat Zahan, Ibrahim Moazzam, Lizett Aguilar, Noah Attal,and Shirley Araiza Santaella, introduces a Python project allowing easy control of LED strip lights. 

Our project is designed with scalability in mind, accommodating a strip of lights that illuminate based on the International Space Station's coordinates across the globe. Leveraging object-oriented programming and a structured series of classes, our code is adaptable to accommodate any future modifications or enhancements.

This project serves as a culmination of our efforts for the "SI 568: Introduction to Applied Data Science" course, showcasing our proficiency in practical coding applications and innovative problem-solving.

### Why It's Useful
1. Real-world Integration: Connects LED lights with real-time data from the International Space Station.
2. Versatility: Can be adapted for various projects related to LED control.

### How It Works

The LED Strip Light Control project consists of a Python script that allows users to interactively control LED strip lights. Here's how it works:

> Initialization: Upon running the Python script, an LED strip object is initialized with a predefined number of LEDs.

> User Interaction: The script prompts the user with a menu displaying various options for controlling the LED strip's color and patterns.

> Options: Users can choose from the following options:

1. Set all lights to the same color.
2. Alternate between two colors.
3. Alternate back and forth between two colors.
4. Create ripple effects across the LED strip.
5. Create a chasing lights effect.
6. Synchronize LED strip colors to the beats of an audio file.

> API Communication: When a user selects an option, the corresponding method is called on the LED strip object, which communicates with an API to change the color and pattern of the LED strip.

> Looping: The script loops indefinitely until the user decides to quit by pressing "q", allowing users to experiment with different lighting effects.

> Shutdown: Upon quitting, the script turns off all the LEDs, effectively shutting down the LED strip.

### Getting Started
To get started with the project, follow these steps:

1. Clone the Repository:
Clone the repository containing the LED light show project to your local machine using Git:

   ```bash
    #Copy the following command
    git clone [https://github.com/yourrepository.git](https://github.com/umsi-class/project-1-lake-pronounced-lock-ay)

2. Install Dependencies:
Ensure you have Python 3.x installed on your system. Navigate to the project directory using the cd command and install the required Python packages using pip:

      ```bash
      #Copy the following command
      pip install requests librosa numpy

After the installation is complete, you can verify that the packages were installed successfully by running the following command:

      ```bash
      #Copy the following command
      pip list

This command will display a list of installed Python packages, and you should see requests, librosa, and numpy among them.

Now, you have successfully installed the dependencies required for the LED light show project. You can proceed with running the program and interacting with it to control the LED strip's colors and patterns.
   
4. Set Up API Key and Device Name:
Open the driver.py file in a text editor and replace the values of API_KEY and DEVICE_NAME variables with your API key and device name respectively. This ensures that the API requests are sent to the correct endpoint.

5. Run the Program:
Execute the main Python script to start the LED light show program:

   ```bash
   #Copy the following command
   python driver.py

6. Interact with the Program:
Follow the on-screen prompts to interact with the LED light show program. Choose from various options to control the LED strip colors and patterns.

7. Exit the Program:
To exit the program, select the option to quit or press 'q'. This will turn off all LEDs and terminate the program.

8. Enjoy Your Light Show:
Once the program is set up and running, enjoy the dynamic LED light show with different patterns and colors.
   
### Getting Help
If you need help with the project or encounter any issues, you can:
1. Reach out to the project maintainers by raising an issue on the GitHub repository.
2. Explore the project documentation for troubleshooting guides or additional information.
   
### Maintainers
This project is maintained and contributed to by Team LAKE (Members: Nuzhat Zahan (znuzhat@umich.edu),  Ibrahim Moazzam (imoazzam@umich.edu), Lizett Aguilar (lizett@umich.edu), Noah Attal (attnoah@umich.edu) and, Shirley Araiza Santaella (saraizas@umich.edu). We are committed to keeping the project up-to-date and welcoming contributions from the community. 

