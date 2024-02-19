import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import ttkbootstrap

class WeatherApp(ttkbootstrap.Window):
    def __init__(self, themename='morph') -> None:
        super().__init__(themename=themename)
        self.title("Weather App")
        self.geometry("400x400")

        self.setup_widgets()

    def setup_widgets(self) -> None:
        # Disable resizing the window
        self.resizable(width=False, height=False)
        
        # Entry widget -> to enter the city name
        self.city_entry = ttkbootstrap.Entry(self, font=("Helvetica", 18))
        self.city_entry.pack(pady=10)

        # Button widget -> to get the weather details
        self.search_button = ttkbootstrap.Button(self, text="Search", command=self.search, bootstyle="warning")
        self.search_button.pack(pady=10)

        # Label widget -> to show the city/country name
        self.location_label = tk.Label(self, font=("Helvetica", 25))
        self.location_label.pack(pady=20)

        # Label widget -> to show the weather icon
        self.icon_label = ttkbootstrap.Label(self)
        self.icon_label.pack()

        # Label widget -> to show the temperature
        self.temperature_label = tk.Label(self, font=("Helvetica", 20))
        self.temperature_label.pack()

        # Label widget -> to show the weather description
        self.description_label = tk.Label(self, font=("Helvetica", 20))
        self.description_label.pack()  # Don't forget to pack the description label

    # Function to get weather information from openweathermap.org API
    def get_weather(self, city) -> tuple:
        API_key = "API_key"  # Replace with your actual API key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"

        try:
            res = requests.get(url)
            res.raise_for_status()  # Raise HTTPError for bad responses

            weather = res.json()
            icon_id = weather["weather"][0]["icon"]
            temperature = weather["main"]["temp"] - 273.15
            description = weather["weather"][0]["description"]
            country = weather["sys"]["country"]
            city = weather["name"]

            icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
            return (icon_url, temperature, description, country, city)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve weather data: {e}")
            return None

    # Function to search weather for a city
    def search(self) -> None:
        city = self.city_entry.get()
        result = self.get_weather(city)
        if result is None:
            return

        icon_url, temperature, description, country, city = result
        self.location_label.config(text=f"{city}, {country}")

        image = Image.open(requests.get(icon_url, stream=True).raw)
        icon = ImageTk.PhotoImage(image)
        self.icon_label.configure(image=icon)
        self.icon_label.image = icon

        self.temperature_label.configure(text=f"{temperature:.2f}°C")
        self.description_label.configure(text=f"Description: {description}")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()