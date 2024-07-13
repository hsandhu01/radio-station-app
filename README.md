# World Radio App

This is a simple World Radio App built using Python and Tkinter. It allows users to select a country and genre, and play radio stations from the selected options.

## Features

- Fetch radio stations by country and genre.
- Play the selected radio station.
- Stop the currently playing station.
- Control the volume of the playing station.

## Requirements

- Python 3.x
- `requests` library
- `vlc` library
- `pyradios` library
- `tkinter` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/hsandhu01/radio-station-app.git
    cd radio-station-app
    ```

2. Install the required Python libraries:
    ```sh
    pip install requests python-vlc pyradios
    ```

3. Run the app:
    ```sh
    python3 radio_app.py
    ```

## Usage

1. Select a country from the dropdown menu.
2. Select a genre from the dropdown menu.
3. Click on the "Update Stations" button to fetch the radio stations for the selected country and genre.
4. Select a radio station from the list.
5. Click "Play" to start playing the selected radio station.
6. Use the "Stop" button to stop the currently playing station.
7. Adjust the volume using the volume slider.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
