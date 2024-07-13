import tkinter as tk
from tkinter import ttk, messagebox
import os
import vlc  # You need to install python-vlc using pip
import pyradios

# List of available Radio Browser servers
SERVERS = [
    "de1.api.radio-browser.info",
    "de2.api.radio-browser.info",
    "nl1.api.radio-browser.info",
    "at1.api.radio-browser.info",
    "fr1.api.radio-browser.info",
]

# Predefined common genres
COMMON_GENRES = [
    "pop", "rock", "jazz", "classical", "electronic", "hiphop", "country", "reggae", "blues", "metal",
    "disco", "folk", "funk", "gospel", "latin", "soul", "techno", "trance", "world"
]

# Function to fetch radio stations by country and genre using pyradios
def fetch_radio_stations(country, genre):
    for server in SERVERS:
        try:
            rb = pyradios.RadioBrowser(base_url=f"https://{server}")
            stations = rb.search(country=country, tag=genre, limit=10)  # Adjust limit as needed
            return stations
        except Exception as e:
            print(f"Error fetching stations from {server}: {e}")
    messagebox.showerror("Error", "Failed to fetch radio stations from all servers.")
    return []

# Function to play the selected radio station
def play_station():
    global player

    selected_station = station_combobox.get()
    if selected_station:
        station_info = station_urls[selected_station]
        url = station_info['url_resolved']

        # Stop the current player if it's already playing
        if player and player.is_playing():
            player.stop()

        # Configure VLC instance with logging redirection
        instance = vlc.Instance('--quiet', '--no-xlib')  # Suppress VLC output
        player = instance.media_player_new()
        media = instance.media_new(url)
        player.set_media(media)
        player.audio_set_volume(volume_scale.get())  # Set initial volume
        player.play()
        messagebox.showinfo("Play Station", f"Playing: {selected_station}\nURL: {url}")
    else:
        messagebox.showwarning("No Station Selected", "Please select a radio station to play.")

# Function to stop the current radio station
def stop_station():
    global player
    if player and player.is_playing():
        player.stop()

# Function to update the station list based on selected country and genre
def update_stations():
    country = country_combobox.get()
    genre = genre_combobox.get()
    stations = fetch_radio_stations(country, genre)
    station_names = [station['name'] for station in stations]
    global station_urls
    station_urls = {station['name']: station for station in stations}
    station_combobox['values'] = station_names
    if station_names:
        station_combobox.current(0)

# Function to update the genre list based on the selected country
def update_genres():
    genre_combobox['values'] = COMMON_GENRES
    if COMMON_GENRES:
        genre_combobox.current(0)
    update_stations()

# Function to set the volume
def set_volume(val):
    global player
    volume = int(val)
    if player:
        player.audio_set_volume(volume)

# Initialize the media player globally
player = None

# Create the main window
root = tk.Tk()
root.title("World Radio App")

# Set the icon
icon_path = os.path.join('assets', 'images', 'icons8-radio-64.png')
root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Create and place the country label and combobox
country_label = tk.Label(root, text="Country:")
country_label.grid(row=0, column=0, padx=10, pady=10)
countries = [
    "United States", "United Kingdom", "Canada", "Australia", "Germany", "France",
    "Italy", "Spain", "Netherlands", "Russia", "India", "China", "Japan", "South Korea",
    "Brazil", "Mexico", "South Africa", "Argentina", "Sweden", "Norway", "Denmark"
]
country_combobox = ttk.Combobox(root, values=countries)
country_combobox.grid(row=0, column=1, padx=10, pady=10)
country_combobox.current(0)
country_combobox.bind("<<ComboboxSelected>>", lambda e: update_genres())

# Create and place the genre label and combobox
genre_label = tk.Label(root, text="Genre:")
genre_label.grid(row=1, column=0, padx=10, pady=10)
genre_combobox = ttk.Combobox(root, values=COMMON_GENRES)
genre_combobox.grid(row=1, column=1, padx=10, pady=10)
genre_combobox.current(0)
genre_combobox.bind("<<ComboboxSelected>>", lambda e: update_stations())

# Create and place the station label and combobox
station_label = tk.Label(root, text="Station:")
station_label.grid(row=2, column=0, padx=10, pady=10)
station_combobox = ttk.Combobox(root)
station_combobox.grid(row=2, column=1, padx=10, pady=10)

# Create and place the play button
play_button = tk.Button(root, text="Play", command=play_station)
play_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Create and place the stop button
stop_button = tk.Button(root, text="Stop", command=stop_station)
stop_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Create and place the volume scale
volume_label = tk.Label(root, text="Volume:")
volume_label.grid(row=5, column=0, padx=10, pady=10)
volume_scale = tk.Scale(root, from_=0, to=100, orient='horizontal', command=set_volume)
volume_scale.set(50)  # Set default volume to 50
volume_scale.grid(row=5, column=1, padx=10, pady=10)

# Create and place the update button
update_button = tk.Button(root, text="Update Stations", command=update_stations)
update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Initial update of genres and stations
update_genres()

# Run the main event loop
root.mainloop()

