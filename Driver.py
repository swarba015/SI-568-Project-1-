from os import wait
from turtle import back, color
import requests
import time
import math
import numpy as np
import sounddevice as sd
import pyinputplus as pyip


DEVICE_NAME = "LAKE"

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiaW1vYXp6YW1AdW1pY2guZWR1In0.PRqLyhxxaL1RCJDyfQmczzCNw14jotJ4YsFE4PfWlic"


def API(color: str) -> None:
    """
    Sends a POST request to a specific URL to change the color setting of the LED strip.

    This function constructs and sends a POST request to the "https://si568.umsi.run/change" URL.
    The request includes a JSON payload that specifies the new color values for the strip. The URL
    includes query parameters for an API key and the name of the controller, which are obtained from
    global variables `API_KEY` and `DEVICE_NAME`, respectively.

    Parameters:
    - `color` (str): The new color string to set for the strip. The exact format of this
      parameter is a series of 4 comma-separated numbers between [0-255] for each LED to represent R,G,B,W.

    Returns:
    - This function does not return any value. It only sends a POST request to the specified URL.

    Note:
    - The global variables `API_KEY` and `DEVICE_NAME` must be defined and valid for the request to
      succeed.
    - This function requires the `requests` module to be imported in order to send the HTTP request.
    """
    url = f"https://si568.umsi.run/change?key={API_KEY}&device={DEVICE_NAME}"
    try:
        requests.post(
            url,
            json={"values": color},
        )
    except:
        print("An error has occurred during the API call; try again!")


class ColorPicker:
    colors = {
        "black": "0,0,0,0",
        "blue": "0,0,255,0",
        "cyan": "0,255,255,0",
        "green": "0,255,0,0",
        "magenta": "255,0,255,0",
        "maize": "255,203,5,0",
        "red": "255,0,0,0",
        "white": "0,0,0,255",
        "yellow": "255,255,0,0",
    }

    def add_color(self, name: str, R: int, G: int, B: int, W: int) -> None:
        """
        Adds a new color to the ColorPicker's `colors` dictionary.

        This method allows for the addition of custom colors to the class's color dictionary.
        Colors are defined by their name and their RGB values, with the addition of a white
        balance component represented by 'W'. The method updates the `colors` dictionary of
        the class by adding the new color or updating the value if the color name already exists.

        Parameters:
        - name (str): The name of the color to be added or updated. This acts as the key in the
          color dictionary.
        - R (int): The red component of the color, a value between 0 and 255.
        - G (int): The green component of the color, a value between 0 and 255.
        - B (int): The blue component of the color, a value between 0 and 255.
        - W (int): The white balance component of the color, a value between 0 and 255. This is
          used to adjust the color's brightness or to add white light to the color mix.

        Returns:
        None. This method updates the class's `colors` dictionary in place.

        Example:
        >>> color_picker = ColorPicker()
        >>> color_picker.add_color("orange", 255, 255, 0, 0)
        This adds the color 'orange' with the specified RGB values and white balance to the color dictionary.
        """
        self.colors[name] = f"{R},{G},{B},{W}"


class LEDStrip(ColorPicker):
    def __init__(self):
        """
        Initializes an `LEDStrip` object with a predefined number of LEDs and a default color.

        Attributes:
        - NUMBER_OF_LEDS (int): The total number of LEDs in the strip. This is set to 300 by default.
        - color (str, optional): The current color configuration of the LED strip. It's initially set to None and will be updated when colors are applied to the strip.
        """
        self.NUMBER_OF_LEDS = 300
        self.color = None

    def array_to_color(self, array):
        """
        Converts an array of RGBW color values into a single string representation.

        This method is used to prepare the color data for sending to the LED strip. It takes an array
        of color values, each represented as a string in the format "R,G,B,W", and concatenates them into
        a single string with the values separated by commas.

        Parameters:
        - array (List[str]): An array of strings, each representing an RGBW color value for one LED in the format "R,G,B,W".

        Returns:
        - str: A string representation of the `color` array, with each LED's color value concatenated and separated by commas.

        Example:
            >>> led_strip = LEDStrip()
            >>> led_strip.array_to_color(["255,0,0,0", "0,255,0,0"])
            '255,0,0,0,0,255,0,0'
        """
        color = ",".join(array)
        return color

    def same_color_all(self, color: str) -> None:
        """
        Sets the entire LED strip to a single color.

        This method looks up the specified color in the parent class's `color` dictionary. If the color
        is found, it converted into a single string format suitable for the API. If the color is not found, it defaults
        to turning all LEDs off ("0,0,0,0"). The API is then called and the color is stored in the `color` attribute.

        Parameters:
        - color (str): The name of the color to set for the entire LED strip, as defined in the ColorPicker's
                         colors dictionary.

        Note: This method uses the `API` function to apply the color configuration to the LED strip. The `API` function should be implemented to handle the communication with the LED strip's hardware or software controller.

        Example:
            >>> led_strip = LEDStrip()
            >>> led_strip.same_color_all("red")
            This sets all LEDs in the strip to red.
        """
        # Need to try-catch for the .get()
        color_RGBW = self.colors.get(color, "0,0,0,0")
        color_array = []
        color_array = [color_RGBW] * self.NUMBER_OF_LEDS
        self.color = self.array_to_color(color_array)
        API(self.color)

    def alternate_colors(self, first_color: str, second_color: str) -> None:
        """
        Sets the LED strip to alternate between two colors along its length.

        Every other LED on the strip will be set to the first color, and the intervening LEDs will be set to
        the second color. The colors are specified by name and looked up in the ColorPicker's `color` dictionary.
        If a color name does not exist in the dictionary, it defaults to "0,0,0,0" (off).

        Parameters:
        - first_color (str): The name of the first color, as defined in the ColorPicker's `colors` dictionary.
        - second_color (str): The name of the second color, as defined in the ColorPicker's `colors` dictionary.

        Example:
            >>> led_strip = LEDStrip()
            >>> led_strip.alternate_colors("red", "blue")
            This will set alternating LEDs in the strip to red and blue, respectively.
        """
        # Need to try-catch for the .get()
        first_color_RGBW = self.colors.get(first_color, "0,0,0,0")
        second_color_RGBW = self.colors.get(second_color, "0,0,0,0")
        color_array = []
        for i in range(self.NUMBER_OF_LEDS):
            if i % 2 == 0:
                color_array.append(first_color_RGBW)
            else:
                color_array.append(second_color_RGBW)
        self.color = self.array_to_color(color_array)
        API(self.color)

    def alternate_back_forth(
        self, first_color: str, second_color: str, option: str
    ) -> None:
        """
        Alternates the LED strip between two colors, with the alternation pattern based on the specified option.

        This method allows for dynamic color patterns on the LED strip, alternating between two colors
        based on the selected option. For a duration of 5 seconds, the strip will either alternate every other LED
        between the two colors (`option` "1") or switch the entire strip between the two colors (`option` "2").

        Parameters:
        - first_color (str): The name of the first color, as defined in the ColorPicker's `colors` dictionary.
        - second_color (str): The name of the second color, as defined in the ColorPicker's `colors` dictionary.
        - option (str): Determines the alternation pattern. "1" for alternating every other LED, "2" for switching the entire strip between the two colors.

        Note:
            The transition speed and the method used to apply these changes are not adjustable within this method
            and are fixed to a duration of 5 seconds for demonstration purposes.

        Example:
            >>> led_strip = LEDStrip()
            >>> led_strip.alternate_back_forth("green", "magenta", "1")
            This will make the strip alternate every other LED between green and magenta for 5 seconds.
        """
        start_time = time.time()
        while time.time() - start_time < 5:
            if option == "1":
                self.alternate_colors(first_color, second_color)
                self.alternate_colors(second_color, first_color)
            else:
                self.same_color_all(first_color)
                self.same_color_all(second_color)

    def ripples(self, background_color: str, circles_color: str) -> None:
        """
        Creates a ripple effect on the LED strip by alternately displaying circles of a specified color against a background color.

        This method calculates the number of LEDs that should light up in each circle to simulate a ripple
        effect based on predefined radii. The ripples expand outwards for a duration of 5 seconds.

        Parameters:
        - background_color (str): The name of the color to use as the background.
        - circles_color (str): The name of the color for the circles to create the ripple effect.

        Note: The implementation assumes that the LED strip is coiled up in a spiral with varying radii. The `API` function is used to update the LED strip's color configuration.
        """

        # Distance between LEDs
        spacing = 1.65
        # Radii of the circles of the LED strip when it's wound up
        radii = [
            2.7,
            3.0,
            3.3,
            3.6,
            3.9,
            4.2,
            4.5,
            4.8,
            5.1,
            5.4,
            5.7,
            6.0,
            6.3,
            6.6,
            6.9,
            7.2,
        ]
        # Number of LEDs within every circle
        led_counts = [(2 * math.pi * r) / spacing for r in radii]
        led_counts_rounded = list(map(round, led_counts))
        led_counts_rounded[0] -= 1
        self.same_color_all(background_color)
        # Need to try-catch for the .get()
        circles_color_RGBW = self.colors.get(circles_color, "0,0,0,0")
        background_color_RGBW = self.colors.get(background_color, "0,0,0,0")
        color_array = [background_color_RGBW] * self.NUMBER_OF_LEDS

        # Code to make ripples go outwards
        start_time = time.time()
        while time.time() - start_time < 5:
            i = 0
            for number_of_leds in led_counts_rounded:
                color_array[
                    (self.NUMBER_OF_LEDS - i)
                    - number_of_leds : (self.NUMBER_OF_LEDS - i)
                ] = [circles_color_RGBW] * number_of_leds
                self.color = self.array_to_color(color_array)
                API(self.color)
                color_array[
                    (self.NUMBER_OF_LEDS - i)
                    - number_of_leds : (self.NUMBER_OF_LEDS - i)
                ] = [background_color_RGBW] * number_of_leds
                i += number_of_leds

        self.same_color_all(background_color)

    def chasing_lights(self, color: str) -> None:
        """
        Creates a chasing light effect on the LED strip where a group of LEDs of a specified color moves along the strip.

        The effect simulates lights "chasing" each other along the strip, with each light group consisting
        of four LEDs. The background color of the strip is set to maize, and the chasing lights are set
        to the specified color.

        Parameters:
        - color (str): The name of the color for the chasing lights.
        """
        # Need to try-catch for the .get()
        color_RGBW = self.colors.get(color, "0,0,0,0")
        # Turn the entire LED strip maize
        color_array = [self.colors.get("maize", "0,0,0,0")] * self.NUMBER_OF_LEDS
        for i in range(self.NUMBER_OF_LEDS):
            color_array[i : i + 4] = [color_RGBW] * 4
            self.color = self.array_to_color(color_array)
            API(self.color)
            color_array[i] = self.colors.get("maize", "0,0,0,0")

    def turn_off_all(self):
        """
        Turns off all LEDs on the strip.

        This method sets the entire LED strip to black, effectively turning off all the LEDs.
        """
        self.color = self.same_color_all("black")

    def set_led_brightness(self, brightness: int) -> None:
        """
        Sets the brightness of the LED strip.

        This method allows setting the brightness of the entire LED strip by adjusting the blue
        component of the RGBW color configuration. The rest of the components are set to 0.

        Parameters:
        - brightness (int): The brightness level to set, where the value is directly used as
                            the blue component's value in the RGBW color model.

        Note: This implementation specifically manipulates the blue component for brightness, but any color/combination of colors can be used instead.
        """
        color_RGBW = f"0,0,{brightness},0"
        color_array = []
        color_array = [color_RGBW] * self.NUMBER_OF_LEDS
        self.color = self.array_to_color(color_array)
        API(self.color)

    def audio_callback(self, indata, frames, time, status):
        """
        This callback function is called for each audio chunk captured by the microphone.
        It tries to detect volume levels by analyzing the energy of the audio signal.

        Parameters:
        - indata: Captured audio data (numpy array)
        - frames: Number of frames in the chunk
        - time: Timestamps of the block
        - status: Status flags
        """
        # Check for errors
        if status:
            print(status)

        # Calculate the energy of the current audio chunk
        energy = np.sum(indata**2) / len(indata)

        # Normalize energy to a scale of 0-255 for LED brightness
        max_energy = 0.08  # Adjust based on the maximum expected energy level
        brightness = int((energy / max_energy) * 255)
        brightness = min(max(brightness, 0), 255)  # Clamp value to range [0, 255]

        # Set LED brightness based on calculated energy
        self.set_led_brightness(brightness)

    def reactive_lights(self, duration, fs):
        """
        Starts live recording and attempts to control LED intensity based on detected volume levels in the audio input.

        Parameters:
        - duration: Recording duration in seconds
        - fs: Sampling frequency (samples per second)
        """
        print("Starting live recording...")
        with sd.InputStream(callback=self.audio_callback, samplerate=fs, channels=1):
            sd.sleep(duration * 1000)
        print("Live recording finished.")


def input_prompt(led_strip: LEDStrip) -> None:
    """
    Interactively prompts the user to select a lighting effect for an LED strip and configure it accordingly.

    This function provides an interactive prompt where the user can select from various lighting effects
    for an LED strip, such as setting all lights to the same color, making lights alternate between colors,
    creating ripple effects, or even making the lights responsive to sound. The user's selections are
    processed to configure the LED strip accordingly.

    Parameters:
    - `led_strip` (LEDStrip): An instance of an LEDStrip class. This object should have methods corresponding
      to the different lighting effects that can be chosen, such as `same_color_all`, `alternate_colors`,
      `alternate_back_forth`, `ripples`, `chasing_lights`, and `reactive_lights`. It should also have a
      `colors` attribute, which is a dictionary mapping color names to their respective values.

    The function prompts the user for their choice of lighting effect and any necessary color selections.
    The user can continue to choose and configure lighting effects until they decide to quit by entering 'q'.

    Important notes:
    - The function assumes that the `led_strip` parameter provides the necessary methods and attributes as
      described above.
    - For the sound-reactive lights option, the function currently uses fixed values for the duration and
      sampling frequency. These could be made configurable for greater flexibility.
    """

    prompt = """Please choose from one of the following options:
    * Enter 1 to make all the lights the same color
    * Enter 2 to make the lights an alternate color
    * Enter 3 to make the lights alternate back and forth between two colors
    * Enter 4 to make ripples
    * Enter 5 to make the lights chase themselves in a "maize"
    * Enter 6 to make the lights responsive to sound!
    * Enter "c" to add a new color
    - Press "q" to quit"""

    choice = ""
    while True:
        print()
        print("---")
        print(prompt)
        print("---")
        print()
        available_colors = list(led_strip.colors.keys())
        choice = pyip.inputChoice(
            ["1", "2", "3", "4", "5", "6", "c", "q"], prompt="Your choice: "
        )
        if choice == "1":
            color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose a color from the following list {available_colors}: ",
            )
            led_strip.same_color_all(color)

        elif choice == "2":
            # Need input validation
            first_color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose the first color from the following list {available_colors}: ",
            )
            second_color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose the second color from the following list {available_colors}: ",
            )
            led_strip.alternate_colors(first_color, second_color)

        elif choice == "3":
            first_color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose the first color from the following list {available_colors}: ",
            )
            second_color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose the second color from the following list {available_colors}: ",
            )
            print()
            alternating_prompt = """Please choose how you'd like to alternate the lights:
    * Enter 1 to make every other light alternate
    * Enter 2 to make all lights alternate together
            """
            print(alternating_prompt)
            alternating_option = pyip.inputChoice(["1", "2"], prompt="Your choice: ")
            led_strip.alternate_back_forth(
                first_color, second_color, alternating_option
            )

        elif choice == "4":
            background_color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose the background color from the following list {available_colors}: ",
            )
            circles_color = pyip.inputChoice(
                available_colors,
                prompt=f"Choose the circles' color from the following list {available_colors}: ",
            )
            led_strip.ripples(background_color, circles_color)

        elif choice == "5":
            color = pyip.inputChoice(
                available_colors,
                f"Choose a color from the following list {available_colors}: ",
            )
            led_strip.chasing_lights(color)

        elif choice == "6":
            print("Play a sound!")
            duration = 30  # Recording duration in seconds
            fs = 30000  # Sampling frequency in Hz
            led_strip.reactive_lights(duration, fs)

        elif choice == "c":
            name = pyip.inputStr(
                "Enter the name of the color: ", allowRegexes=["[a-zA-Z]"]
            )
            R = pyip.inputInt("Enter the R value: ", min=0, max=255)
            G = pyip.inputInt("Enter the G value: ", min=0, max=255)
            B = pyip.inputInt("Enter the B value: ", min=0, max=255)
            W = pyip.inputInt("Enter the W value: ", min=0, max=255)
            led_strip.add_color(name, R, G, B, W)

        elif choice == "q":
            print()
            break


def main():
    led_strip = LEDStrip()
    print("Welcome to Team LAKE's Light Show!")
    input_prompt(led_strip)
    print("Goodbye!")
    led_strip.turn_off_all()


if __name__ == "__main__":
    main()
