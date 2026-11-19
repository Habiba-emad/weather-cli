git clone <repo-link>
cd weather-cli
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# copy .env.example to .env and add your API key
python weather.py