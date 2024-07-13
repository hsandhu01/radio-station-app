import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QSlider, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import vlc
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

class RadioApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("World Radio App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.player = None
        self.station_urls = {}
        self.favorites = {}

        self.init_ui()

    def init_ui(self):
        # Country selection
        self.country_label = QLabel("Country:")
        self.layout.addWidget(self.country_label)

        self.country_combobox = QComboBox()
        countries = [
            "United States", "United Kingdom", "Canada", "Australia", "Germany", "France",
            "Italy", "Spain", "Netherlands", "Russia", "India", "China", "Japan", "South Korea",
            "Brazil", "Mexico", "South Africa", "Argentina", "Sweden", "Norway", "Denmark"
        ]
        self.country_combobox.addItems(countries)
        self.country_combobox.currentIndexChanged.connect(self.update_genres)
        self.layout.addWidget(self.country_combobox)

        # Genre selection
        self.genre_label = QLabel("Genre:")
        self.layout.addWidget(self.genre_label)

        self.genre_combobox = QComboBox()
        self.genre_combobox.addItems(COMMON_GENRES)
        self.genre_combobox.currentIndexChanged.connect(self.update_stations)
        self.layout.addWidget(self.genre_combobox)

        # Station selection
        self.station_label = QLabel("Station:")
        self.layout.addWidget(self.station_label)

        self.station_combobox = QComboBox()
        self.layout.addWidget(self.station_combobox)

        # Play button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_station)
        self.layout.addWidget(self.play_button)

        # Stop button
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_station)
        self.layout.addWidget(self.stop_button)

        # Volume control
        self.volume_label = QLabel("Volume:")
        self.layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.layout.addWidget(self.volume_slider)

        # Update button
        self.update_button = QPushButton("Update Stations")
        self.update_button.clicked.connect(self.update_stations)
        self.layout.addWidget(self.update_button)

        # Add to favorites button
        self.favorites_button = QPushButton("Add to Favorites")
        self.favorites_button.clicked.connect(self.add_to_favorites)
        self.layout.addWidget(self.favorites_button)

        # Favorites selection
        self.favorites_label = QLabel("Favorites:")
        self.layout.addWidget(self.favorites_label)

        self.favorites_combobox = QComboBox()
        self.favorites_combobox.activated[str].connect(self.play_favorite)
        self.layout.addWidget(self.favorites_combobox)

        self.update_genres()

    def fetch_radio_stations(self, country, genre):
        for server in SERVERS:
            try:
                rb = pyradios.RadioBrowser(base_url=f"https://{server}")
                stations = rb.search(country=country, tag=genre, limit=10)
                if stations:
                    return stations
            except Exception as e:
                print(f"Error fetching stations from {server}: {e}")
        QMessageBox.critical(self, "Error", "Failed to fetch radio stations from all servers.")
        return []

    def play_station(self):
        selected_station = self.station_combobox.currentText()
        if selected_station:
            station_info = self.station_urls[selected_station]
            url = station_info['url_resolved']

            if self.player and self.player.is_playing():
                self.player.stop()

            instance = vlc.Instance('--quiet', '--no-xlib')
            self.player = instance.media_player_new()
            media = instance.media_new(url)
            self.player.set_media(media)
            self.player.audio_set_volume(self.volume_slider.value())
            self.player.play()
            QMessageBox.information(self, "Play Station", f"Playing: {selected_station}\nURL: {url}")
        else:
            QMessageBox.warning(self, "No Station Selected", "Please select a radio station to play.")

    def stop_station(self):
        if self.player and self.player.is_playing():
            self.player.stop()

    def update_stations(self):
        country = self.country_combobox.currentText()
        genre = self.genre_combobox.currentText()
        stations = self.fetch_radio_stations(country, genre)
        station_names = [station['name'] for station in stations]
        self.station_urls = {station['name']: station for station in stations}
        self.station_combobox.clear()
        self.station_combobox.addItems(station_names)
        if station_names:
            self.station_combobox.setCurrentIndex(0)

    def update_genres(self):
        self.genre_combobox.clear()
        self.genre_combobox.addItems(COMMON_GENRES)
        self.update_stations()

    def set_volume(self, value):
        if self.player:
            self.player.audio_set_volume(value)

    def add_to_favorites(self):
        selected_station = self.station_combobox.currentText()
        if selected_station and selected_station not in self.favorites:
            self.favorites[selected_station] = self.station_urls[selected_station]
            self.favorites_combobox.addItem(selected_station)
            QMessageBox.information(self, "Favorites", f"Added {selected_station} to favorites.")

    def play_favorite(self, station_name):
        if station_name in self.favorites:
            station_info = self.favorites[station_name]
            url = station_info['url_resolved']

            if self.player and self.player.is_playing():
                self.player.stop()

            instance = vlc.Instance('--quiet', '--no-xlib')
            self.player = instance.media_player_new()
            media = instance.media_new(url)
            self.player.set_media(media)
            self.player.audio_set_volume(self.volume_slider.value())
            self.player.play()
            QMessageBox.information(self, "Play Favorite", f"Playing: {station_name}\nURL: {url}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load QSS style sheet
    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())
    
    window = RadioApp()
    
    # Set the icon
    icon_path = os.path.join('assets', 'images', 'icons8-radio-64.png')
    window.setWindowIcon(QIcon(icon_path))
    
    window.show()
    sys.exit(app.exec_())

