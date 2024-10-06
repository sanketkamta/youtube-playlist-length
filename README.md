# YouTube Playlist & Video Duration Calculator

This project is a FastAPI-based application that fetches the total duration of a YouTube playlist or video and calculates the duration at various playback speeds, including custom speeds. The app uses the YouTube Data API to retrieve video details and provides results in a user-friendly format.

## Features

- **Calculate Playlist Duration**: Fetches all video durations in a given playlist and calculates the total playlist length.
- **Video Length Calculation**: Fetches the length of a single YouTube video.
- **Custom Playback Speed**: Calculates the video/playlist length at different playback speeds, including a user-defined speed.
- **FastAPI**: Built using the FastAPI web framework for high-performance APIs.

### Virtual environment: [Windows]
1. pip install virtualenv 
2. python -m venv myenv
3. myenv\Scripts\activate

### Run this project in local
uvicorn main:app --reload

### Requirements

- Python 3.7+
- FastAPI
- Uvicorn (for running the FastAPI app)
- Requests
- isodate



