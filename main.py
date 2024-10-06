from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from youtube_playlist_analyzer import playlist_length, video_length

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_details(request: Request):
    print(request.method)
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/playlist")
def get_details(request: Request, search_playlist: str = Form(...), custom_playlist_speed: str | None = Form(...)):
    print("Inside playlist flow")
    if custom_playlist_speed:
        custom_playlist_speed = float(custom_playlist_speed)
    else:
        custom_playlist_speed = 0
    display_playlist_text = playlist_length(search_playlist, custom_playlist_speed)
    print(display_playlist_text)
    return templates.TemplateResponse("home.html", {"request": request, "display_playlist_text": display_playlist_text})


@app.post("/video")
def get_details(request: Request, search_video: str = Form(...), custom_video_speed: str | None = Form(...)):
    print("Inside video flow")
    if custom_video_speed:
        custom_speed = float(custom_video_speed)
    else:
        custom_speed = 0
    display_video_text = video_length(search_video, custom_speed)
    print(display_video_text)
    return templates.TemplateResponse("home.html", {"request": request, "display_video_text": display_video_text})
