
# DesiEnviroMetrics

Are you curious about the state of the environment in your community? Do you need help in finding out about the environment of the destination of your next trip? Do you want to calculate your carbon footprint? Find out how EnviroMetrics can provide real-time data and analysis, raising awareness and analyzing data to improve the environmental conditions in your area.



## Installation

1. Install python from [the official website](https://www.python.org/downloads/) and make sure [python path is set](https://realpython.com/add-python-to-path/).
2. Make sure [pip](https://pip.pypa.io/en/stable/installation/) is installed and then upgrade it.
```
pip --version
python -m pip install --upgrade pip
```
3. Clone the repository or download the code files.
4. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```
5. Obtain you API key from OpenWeatherMap API Key: 
Create a free account on [the site](https://home.openweathermap.org/api_keys) then go to your profile -> My API Keys. Enter a name in API key name under Create key and press generate. The corresponding key in the "Key" column is your API key. Copy it.

6. For setting environment variables : 
- Create a .env file in the main directory.
- Replace the placeholders(<>) in the following code with your values. Leave default values of "LAT" and "LONG".
```
API_KEY = <YOUR_API_KEY>
ROOT = "<PATH-TO-FOLDER>/WeatherAnalyser-GGH/"
LAT = 20.5937
LONG = 78.9629
```
7. Run the following to start your server
```
cd frontend/
streamlit run Welcome.py
```
## Features

- Interactive Maps (Open in fullscreen)
- Modifiable Parameters for each Graph
- Real-Time Weather Data
- Data based on region
- Downloadable dataframe
- Interpretable Graphs
- Light/Dark Mode
- Carbon Footprint Calculator


## Demo

[Link to Demo Video](https://drive.google.com/file/d/1bPM-8vCYAYiKawCEGfLvJ9qQD8_sAzJs/view?usp=drive_link)
(PS - some changes were made after this video)

## Authors

- [@khushiparikh](https://github.com/khushi-parikh)

