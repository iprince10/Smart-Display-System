# Smart Display System Using Python and Raspberry Pi

A smart display system built with Python and Raspberry Pi that shows time, date, weather updates, top news headlines, motivational quotes, and a customizable to-do list.

## Features

* Live time and date display
* Weather information for your city using OpenWeatherMap API
* News headlines using NewsAPI
* Motivational quotes
* Editable to-do list

## Installation

1. Clone the repository:
   `git clone <https://github.com/iprince10/Smart-Display-System>`
2. Make sure you have Python 3 installed
3. Install required packages:
   `pip install -r requirements.txt`
4. Copy `smart_display_config_example.json` to `smart_display_config.json`
5. Fill in your own API keys in `smart_display_config.json`

## How to Run

1. Open a terminal
2. Navigate to the folder containing `SmartDisplay.py`
3. Run:
   `python SmartDisplay.py`

## Configuration

* `smart_display_config.json` contains user-specific settings like API keys, location, name, greeting emoji, and initial to-do list
* **Keep this file private** and do **not** upload it to GitHub
* Users can rename `smart_display_config_example.json` to `smart_display_config.json` and fill in their own API keys

## Usage & Screenshot

Once you run the program:

* The top-left section shows **time, date, and a greeting**
* The top-right section shows **current weather**
* The middle-left section shows **top news headlines**
* The middle-right section shows **your to-do list**, which can be edited using the small ✎ button
* The bottom section shows **motivational quotes** that update periodically
* Screenshot file(smartdisplayimage.jpg) should stay in the repo folder for proper display.

![Smart Display System Screenshot](https://github.com/iprince10/Smart-Display-System/blob/main/smartdisplayimage.jpg?raw=true)

## Contributing

* Fork the repo, make improvements, and submit pull requests
* Do **not** commit real API keys

---

