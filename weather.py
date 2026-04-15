from tkinter import *
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io


def fade_in(label, text, i=0):
    if i <= len(text):
        label.config(text=text[:i])
        win.after(30, lambda: fade_in(label, text, i+1))


def get_location():
    try:
        res = requests.get("http://ip-api.com/json/").json()
        city = res["city"]
        city_name.set(city)
        data_get()
    except:
        weather_label1.config(text="Location Error")



def data_get():
    city = city_name.get()

    try:
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid=aa8e0bd8daca376b44d2160ab9d24bcc"
        ).json()

        if data.get("cod") != 200:
            weather_label1.config(text="City not found")
            return

        weather = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        temp = int(data["main"]["temp"] - 273.15)
        pressure = data["main"]["pressure"]

       
        fade_in(weather_label1, weather)
        fade_in(weatherb_label1, description)
        fade_in(temp_lavel1, f"{temp} °C")
        fade_in(pressure_lavel1, f"{pressure} hPa")

        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_data = requests.get(icon_url).content
        image = Image.open(io.BytesIO(icon_data)).resize((50, 50))

        def grow(size):
            if size <= 100:
                img = Image.open(io.BytesIO(icon_data)).resize((size, size))
                icon = ImageTk.PhotoImage(img)
                icon_label.config(image=icon)
                icon_label.image = icon
                win.after(20, lambda: grow(size + 5))

        grow(50)

    except:
        weather_label1.config(text="Error")



def on_enter(e):
    e.widget.config(bg="#45a049")

def on_leave(e):
    e.widget.config(bg="#4CAF50")


win = Tk()
win.title("Weather App")
win.geometry("600x750")
win.config(bg="sky blue")

Label(win, text="Weather App", font=("Helvetica", 30, "bold"),
      bg="blue", fg="white").pack(pady=20)

city_name = StringVar()

entry = ttk.Combobox(win, textvariable=city_name, font=("Arial", 18))
entry['values'] = ["Kolkata", "Bhubaneswar", "Delhi", "Mumbai", "Chennai"]
entry.pack(pady=10)


btn1 = Button(win, text="Get Weather", font=("Arial", 14, "bold"),
              bg="#4CAF50", fg="white", command=data_get)
btn1.pack(pady=10)

btn1.bind("<Enter>", on_enter)
btn1.bind("<Leave>", on_leave)

Button(win, text="📍 Use My Location", font=("Arial", 14, "bold"),
       bg="#2196F3", fg="white", command=get_location).pack(pady=10)


icon_label = Label(win, bg="#1e1e2f")
icon_label.pack()


frame = Frame(win, bg="#2c2c3e", bd=10, relief=RIDGE)
frame.pack(pady=20, padx=20, fill="both", expand=True)

def create_row(text, y):
    Label(frame, text=text, font=("Arial", 16),
          bg="#2c2c3e", fg="white").place(x=50, y=y)
    value = Label(frame, text="", font=("Arial", 16, "bold"),
                  bg="#2c2c3e", fg="#00ffcc")
    value.place(x=250, y=y)
    return value

weather_label1 = create_row("Weather:", 50)
weatherb_label1 = create_row("Description:", 120)
temp_lavel1 = create_row("Temperature:", 190)
pressure_lavel1 = create_row("Pressure:", 260)

win.mainloop()
