# LobotonApp

LobotonApp is a Python application for managing Loboton games, supporting both a Streamlit web interface and a Tkinter desktop version. It allows users to upload court files, view player information, and record game results.

## Features

- **Streamlit Web App**: Interactive web interface for managing games, viewing players, and uploading court files.
- **Tkinter Desktop App**: Local GUI for managing games and teams.
- **Court Templates**: Example CSV files for courts with 6, 7, or 8 players.
- **Player Ratings**: Integration with Google Sheets for player ratings.
- **Image Support**: Displays player images in the UI.

## Installation

1. Clone the repository:
	```powershell
	git clone https://github.com/josejlopezperez/LobotonApp.git
	```
2. Install dependencies:
	```powershell
	pip install streamlit customtkinter pillow pandas
	```

## Usage

### Streamlit Web App

Run the web app with:
```powershell
streamlit run Home.py
```
- Upload a court CSV file when prompted.
- View and manage players and teams.

### Tkinter Desktop App

Run the desktop app with:
```powershell
python LobotonSheetAppTkinterVersion.py
```

## File Structure

- `Home.py`: Entry point for the Streamlit web app.
- `LobotonSheetAppTkinterVersion.py`: Tkinter desktop app.
- `Src/`: Core modules (`CourtInfo.py`, `Player.py`, `LobotonSheetWepApp.py`).
- `Resources/`: Example court and player CSV files, player image.
- `pages/`: Streamlit pages for ratings and court templates.

## Example Court Files

- `Resources/court_6_players.csv`
- `Resources/court_7_players.csv`
- `Resources/court_8_players.csv`

## Contributing

Feel free to submit issues or pull requests!