import tkinter as tk
import tkinter.font as font
from datetime import datetime
import requests
from newsapi import NewsApiClient
import random
import threading
import json
import os

# === Configuration ===
CONFIG_FILE = "smart_display_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "api_keys": {
        "openweather": "Your_OPENWEATHER_API_KEY",
        "newsapi": "YOUR_NEWSAPI_KEY"
    },
    "location": "Guwahati",
    "user": {
        "name": "Master Prince",
        "greeting_emoji": "😊"
    },
    "todo_items": [
        "Complete IoT Internship Assignments",
        "Revise Microprocessors",
        "Work on Smart Mirror Project",
        "Upload progress to LinkedIn"
    ]
}

# Load or create config file
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
else:
    config = DEFAULT_CONFIG
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# === Main Application ===
class SmartDisplay:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Smart Mirror")
        self.window.configure(bg="white")
        self.window.state('zoomed')
        self.fullscreen = True
        
        # Key bindings
        self.window.bind("<F11>", self.toggle_fullscreen)
        self.window.bind("<Escape>", lambda e: self.window.destroy())
        self.window.bind("<Control-n>", self.edit_todo_list)
        
        self.setup_ui()
        self.start_updates()
        
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)
        
    def setup_ui(self):
        # Screen dimensions
        screen_height = self.window.winfo_screenheight()
        screen_width = self.window.winfo_screenwidth()
        
        # Font configurations
        self.largeFont = font.Font(family='Helvetica', size=int(screen_height * 0.06))
        self.mediumFont = font.Font(family='Helvetica', size=int(screen_height * 0.035))
        self.smallFont = font.Font(family='Helvetica', size=int(screen_height * 0.022))
        
        # Layout configuration - 3 columns now
        self.window.rowconfigure(0, weight=1)  # Top section
        self.window.rowconfigure(1, weight=3)  # Middle section
        self.window.rowconfigure(2, weight=1)  # Bottom section
        
        # Three columns: 40% for news, 40% for todo/weather, 20% reserved for future
        self.window.columnconfigure(0, weight=4)
        self.window.columnconfigure(1, weight=4)
        self.window.columnconfigure(2, weight=2)
        
        # Create all UI components
        self.create_top_section()
        self.create_news_section()
        self.create_todo_section()  # Now in column 1 (middle)
        self.create_quotes_section()
        
    def create_top_section(self):
        # Top Left: Time, Date, Greeting
        top_left = tk.Frame(self.window, bg="white")
        top_left.grid(row=0, column=0, sticky="nw", padx=40, pady=20)
        
        self.time_label = tk.Label(top_left, font=self.largeFont, fg='black', bg='white', anchor='w')
        self.time_label.pack(anchor="w")
        
        self.date_label = tk.Label(top_left, font=self.largeFont, fg='black', bg='white', anchor='w')
        self.date_label.pack(anchor="w")
        
        greeting = f"Hi {config['user']['name']} {config['user']['greeting_emoji']}"
        self.greeting_label = tk.Label(top_left, text=greeting, font=self.mediumFont, 
                                     fg='black', bg='white', anchor='w')
        self.greeting_label.pack(anchor="w", pady=(10, 0))
        
        # Top Right: Weather (now in column 1)
        top_right = tk.Frame(self.window, bg="white")
        top_right.grid(row=0, column=1, sticky="ne", padx=40, pady=20)
        
        self.weather_label = tk.Label(top_right, font=self.mediumFont, fg='black', 
                                    bg='white', justify="right", anchor='e')
        self.weather_label.pack(anchor="e")
        
    def create_news_section(self):
        # Middle Left: News Headlines (column 0)
        mid_left = tk.Frame(self.window, bg="white")
        mid_left.grid(row=1, column=0, sticky="nsew", padx=40, pady=10)
        
        # Scrollable news area
        self.news_canvas = tk.Canvas(mid_left, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(mid_left, orient="vertical", command=self.news_canvas.yview)
        self.scrollable_news_frame = tk.Frame(self.news_canvas, bg="white")
        
        self.scrollable_news_frame.bind(
            "<Configure>",
            lambda e: self.news_canvas.configure(
                scrollregion=self.news_canvas.bbox("all")
            )
        )
        
        self.news_canvas.create_window((0, 0), window=self.scrollable_news_frame, anchor="nw")
        self.news_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.news_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(self.scrollable_news_frame, text="Top Headlines (India):", 
                font=self.mediumFont, fg='black', bg='white', anchor="w").pack(anchor="w", pady=(0, 10))
        
        self.news_labels = [
            tk.Label(self.scrollable_news_frame, font=self.smallFont, fg='black', 
                    bg='white', anchor="w", justify='left', wraplength=self.window.winfo_screenwidth()*0.35)
            for _ in range(4)
        ]
        for lbl in self.news_labels:
            lbl.pack(anchor="w", pady=2)
            
    def create_todo_section(self):
        # Middle Right: To-Do List (column 1, below weather)
        mid_right = tk.Frame(self.window, bg="white")
        mid_right.grid(row=1, column=1, sticky="nsew", padx=40, pady=10)
        
        # Header with edit button
        header_frame = tk.Frame(mid_right, bg="white")
        header_frame.pack(anchor="w", pady=(0, 10))
        
        tk.Label(header_frame, text="Today's Tasks:", font=self.mediumFont, 
                fg='black', bg='white', anchor="w").pack(side="left")
        
        # Small edit button
        edit_btn = tk.Button(header_frame, text="✎", font=self.smallFont, 
                           command=self.edit_todo_list, bd=0, bg="white", fg="gray")
        edit_btn.pack(side="left", padx=10)
        
        # Todo items
        self.todo_frame = tk.Frame(mid_right, bg="white")
        self.todo_frame.pack(anchor="w", fill="both", expand=True)
        
        self.load_todo_items()
            
    def load_todo_items(self):
        # Clear existing items
        for widget in self.todo_frame.winfo_children():
            widget.destroy()
        
        # Load from config and create new labels
        self.todo_labels = [
            tk.Label(self.todo_frame, text=f"• {task}", font=self.smallFont, 
                     fg='black', bg='white', anchor='w', wraplength=self.window.winfo_screenwidth()*0.35)
            for task in config['todo_items']
        ]
        for lbl in self.todo_labels:
            lbl.pack(anchor="w", pady=2)
            
    def edit_todo_list(self, event=None):
        # Create edit window
        edit_win = tk.Toplevel(self.window)
        edit_win.title("Edit To-Do List")
        edit_win.geometry("400x400")
        
        # Text area for editing
        text_area = tk.Text(edit_win, font=self.smallFont, wrap=tk.WORD)
        text_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load current items
        current_items = "\n".join(config['todo_items'])
        text_area.insert("1.0", current_items)
        
        # Save button
        def save_changes():
            new_items = text_area.get("1.0", tk.END).strip().split("\n")
            config['todo_items'] = [item.strip() for item in new_items if item.strip()]
            
            # Save to config file
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            
            # Update display
            self.load_todo_items()
            edit_win.destroy()
            
        save_btn = tk.Button(edit_win, text="Save", command=save_changes)
        save_btn.pack(pady=10)
            
    def create_quotes_section(self):
        # Bottom: Motivational Quotes
        bottom = tk.Frame(self.window, bg="white")
        bottom.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=40, pady=20)
        
        tk.Label(bottom, text="Motivational Quotes:", font=self.mediumFont, 
                fg='black', bg='white', anchor="w").pack(anchor="w")
        
        self.quote_label1 = tk.Label(bottom, font=self.smallFont, fg='black', 
                                   bg='white', wraplength=self.window.winfo_screenwidth()*0.8, justify="left")
        self.quote_label1.pack(anchor="w", pady=(5, 0))
        
        self.quote_label2 = tk.Label(bottom, font=self.smallFont, fg='black', 
                                    bg='white', wraplength=self.window.winfo_screenwidth()*0.8, justify="left")
        self.quote_label2.pack(anchor="w", pady=(5, 0))
        
        self.quotes = [
            "Believe in yourself and all that you are.",
            "Push yourself, because no one else is going to do it for you.",
            "Success doesn't just find you. You have to go out and get it.",
            "Great things never come from comfort zones.",
            "Dream it. Wish it. Do it.",
            "Your limitation—it's only your imagination.",
            "Hard work beats talent when talent doesn't work hard.",
            "Don't watch the clock; do what it does. Keep going."
        ]
        
    def start_updates(self):
        self.update_time()
        threading.Thread(target=self.update_weather, daemon=True).start()
        threading.Thread(target=self.update_news, daemon=True).start()
        self.update_quotes()
        
    def update_time(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%I:%M %p"))
        self.date_label.config(text=now.strftime("%A, %B %d"))
        self.window.after(1000, self.update_time)
        
    def update_weather(self):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={config['location']}&appid={config['api_keys']['openweather']}&units=metric"
            response = requests.get(url, timeout=10).json()
            if response.get("main"):
                temp = response['main']['temp']
                desc = response['weather'][0]['description'].capitalize()
                humidity = response['main']['humidity']
                wind = response['wind']['speed']
                weather_text = f"{config['location']}: {temp}°C | {desc}\nHumidity: {humidity}% | Wind: {wind} m/s"
                self.weather_label.config(text=weather_text)
        except Exception as e:
            print(f"Weather error: {e}")
            self.weather_label.config(text="Weather data unavailable")
        self.window.after(600000, lambda: threading.Thread(target=self.update_weather, daemon=True).start())
        
    def update_news(self):
        try:
            newsapi = NewsApiClient(api_key=config['api_keys']['newsapi'])
            top_headlines = newsapi.get_everything(q='India', language='en', sort_by='publishedAt', page_size=4)
            headlines = [article['title'] for article in top_headlines['articles'][:4]]
            for i, title in enumerate(headlines):
                clean_title = ' '.join(title.split())
                formatted = clean_title[:120] + "..." if len(clean_title) > 120 else clean_title
                self.news_labels[i].config(text=f"• {formatted}")
        except Exception as e:
            print(f"News error: {e}")
            for lbl in self.news_labels:
                lbl.config(text="Could not load headlines.")
        self.window.after(900000, lambda: threading.Thread(target=self.update_news, daemon=True).start())
        
    def update_quotes(self):
        selected = random.sample(self.quotes, 2)
        self.quote_label1.config(text=f"\"{selected[0]}\"")
        self.quote_label2.config(text=f"\"{selected[1]}\"")
        self.window.after(600000, self.update_quotes)
        
    def run(self):
        self.window.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = SmartDisplay()

    app.run()

