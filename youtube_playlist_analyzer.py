
import os
import re
import isodate
import requests
import logging
from datetime import timedelta

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API URLs
URL_PLAYLIST = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&fields=items/contentDetails/videoId,nextPageToken&key={}&playlistId={}&pageToken='
URL_VIDEO = 'https://www.googleapis.com/youtube/v3/videos?&part=contentDetails&id={}&key={}&fields=items/contentDetails/duration'

# API Key (to be filled in)
API_KEY = os.environ['APIS']


def get_playlist_id(playlist_link):
    """
    Extract the playlist ID from the YouTube playlist URL.
    """
    try:
        # Regex to extract playlist ID
        pattern = re.compile(r'^(\S+list=)?([\w_-]+)\S*$')
        match = pattern.match(playlist_link)
        if match:
            return match.group(2)
        logging.error("Invalid playlist link format.")
        return None
    except Exception as e:
        logging.exception("Error extracting playlist ID: %s", str(e))
        return None


def format_duration(duration):
    """
    Converts a timedelta duration into a human-readable format.
    """
    ts, td = duration.seconds, duration.days
    th, rem = divmod(ts, 3600)  # Get hours and remainder
    tm, ts = divmod(rem, 60)  # Get minutes and seconds

    formatted_duration = []
    if td: formatted_duration.append(f"{td} day{'s' if td != 1 else ''}")
    if th: formatted_duration.append(f"{th} hour{'s' if th != 1 else ''}")
    if tm: formatted_duration.append(f"{tm} minute{'s' if tm != 1 else ''}")
    if ts: formatted_duration.append(f"{ts} second{'s' if ts != 1 else ''}")

    return ', '.join(formatted_duration) if formatted_duration else '0 seconds'


def playlist_length(playlist_link: str, custom_speed: float) -> list:
    """
    Fetches and calculates the total length of a YouTube playlist, adjusting for different playback speeds.
    """
    if custom_speed < 0:
        logging.error("Custom speed must be a positive number.")
        return ["Invalid custom speed. Please enter a value greater than 0."]
    playlist_id = get_playlist_id(playlist_link)
    if not playlist_id:
        return ["Invalid playlist link."]

    next_page = ''
    total_duration = timedelta(0)  # Initialize total playlist duration
    total_videos = 0
    valid_videos = 0
    output = []

    while True:
        try:
            # Fetch playlist items
            response = requests.get(URL_PLAYLIST.format(API_KEY, playlist_id) + next_page)
            results = response.json()

            video_ids = [item['contentDetails']['videoId'] for item in results['items']]
            total_videos += len(video_ids)

            # Fetch video details
            video_id_list = ','.join(video_ids)
            video_details_response = requests.get(URL_VIDEO.format(video_id_list, API_KEY))
            video_details = video_details_response.json()

            # Calculate total playlist duration
            for item in video_details['items']:
                duration_str = item["contentDetails"]["duration"]
                if duration_str != "P0D":  # Skip empty duration
                    valid_videos += 1
                    total_duration += isodate.parse_duration(duration_str)

        except KeyError as e:
            logging.error("Error fetching video details: %s", str(e))
            return [results.get('error', {}).get('message', 'Unknown error')]

        # Check if more pages of the playlist exist
        next_page = results.get('nextPageToken')
        if not next_page or total_videos >= 500:  # Limiting to 500 videos
            if total_videos >= 500:
                output.append('Number of videos limited to 500.')
            break

    if valid_videos > 0:
        # Display statistics
        output += [
            f'Total videos: {total_videos}',
            f'Private/Unavailable videos: {total_videos - valid_videos}',
            f'Average video length: {format_duration(total_duration / valid_videos)}',
            f'Total playlist length: {format_duration(total_duration)}',
            f'At 1.25x: {format_duration(total_duration / 1.25)}',
            f'At 1.5x: {format_duration(total_duration / 1.5)}',
            f'At 1.75x: {format_duration(total_duration / 1.75)}',
            f'At 2x: {format_duration(total_duration / 2)}'
        ]
        if custom_speed != 0:
            output += [f'At {custom_speed}x: {format_duration(total_duration / custom_speed)}']
    return output


def video_length(video_link: str, custom_speed: float) -> list:
    """
    Fetches and calculates the length of a single YouTube video, adjusting for different playback speeds.
    """
    if custom_speed < 0:
        logging.error("Custom speed must be a positive number.")
        return ["Invalid custom speed. Please enter a value greater than 0."]
    video_id = video_link.split("=")[-1]  # Extract video ID from link
    total_duration = timedelta(0)
    output = []

    try:
        # Fetch video details
        response = requests.get(URL_VIDEO.format(video_id, API_KEY))
        video_details = response.json()

        if not video_details['items']:
            print("from 135")
            return ["No video found"]

        duration_str = video_details['items'][0]["contentDetails"]["duration"]
        if duration_str == "P0D":
            return ["Video not yet uploaded"]

        total_duration += isodate.parse_duration(duration_str)

    except KeyError as e:
        logging.error("Error fetching video details: %s", str(e))
        print("from 146")
        return ["No video found"]

    # Display video length statistics
    output += [
        f'Total length of video: {format_duration(total_duration)}',
        f'At 1.25x: {format_duration(total_duration / 1.25)}',
        f'At 1.5x: {format_duration(total_duration / 1.5)}',
        f'At 1.75x: {format_duration(total_duration / 1.75)}',
        f'At 2x: {format_duration(total_duration / 2)}'
    ]
    if custom_speed != 0:
        output += [f'At {custom_speed}x: {format_duration(total_duration / custom_speed)}']
    return output
