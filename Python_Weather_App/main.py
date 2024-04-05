import tkinter as tk
from tkinter import ttk, messagebox
import requests

def get_weather(api_key, city):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()
    return data

def get_weather_and_display():
    city = city_entry.get()
    if city == "":
        messagebox.showerror("Error", "Please enter a city name.")
        return
    
    try:
        weather_data = get_weather(api_key, city)
        if 'error' in weather_data:
            messagebox.showerror("Error", f"Error: {weather_data['error']['message']}")
        else:
            location = weather_data['location']['name']
            country = weather_data['location']['country']
            condition = weather_data['current']['condition']['text']
            temperature_c = weather_data['current']['temp_c']
            temperature_f = weather_data['current']['temp_f']
            humidity = weather_data['current']['humidity']
            icon_url = weather_data['current']['condition']['icon']
            
            result_label.config(text=f"Weather in {location}, {country}:\nCondition: {condition}\nTemperature: {temperature_c}°C ({temperature_f}°F)\nHumidity: {humidity}%")
            
            # Display weather icon
            icon_response = requests.get("http:" + icon_url)
            icon_data = icon_response.content
            photo = tk.PhotoImage(data=icon_data)
            icon_label.config(image=photo)
            icon_label.image = photo
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI Setup
api_key = "#" #ENTER YOUR WEATHERAPI API KEY HERE

root = tk.Tk()
root.title("Weather App")

style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0")

main_frame = ttk.Frame(root)
main_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

city_label = ttk.Label(main_frame, text="Enter city name:")
city_label.grid(column=0, row=0, pady=(0, 5))

city_entry = ttk.Entry(main_frame, width=30)
city_entry.grid(column=0, row=1, padx=5)

get_weather_button = ttk.Button(main_frame, text="Get Weather", command=get_weather_and_display)
get_weather_button.grid(column=1, row=1, padx=5)

result_label = ttk.Label(main_frame, text="", wraplength=300)
result_label.grid(column=0, row=2, columnspan=2, pady=10)

icon_label = ttk.Label(main_frame)
icon_label.grid(column=0, row=3, columnspan=2, pady=(0, 10))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
