from imdb import Cinemagoer
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def info():
    return HTMLResponse(status_code=200,
                        content="""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>IMDB Parent's Guide</title>
        <style>
            body {
                font-family: system-ui, sans-serif;
            }
            h2 {
                padding-left: 1rem;
                border-bottom: 1px solid black;
                font-size: 2rem;
            }
        </style>
    </head>
    <body>
        <div>
            <h2><code>/</code></h2>
            <p>view this page</p>
        </div>
        <div>
            <h2><code>/movies</code></h2>
            <p>search for a movie's parent data</p>
            <ul>
                <li><code>?title=title</code> - specify the movie title</li>
                <li>
                    <code>?include_descriptions=true|false</code>
                    - (optional) whether or not to include descriptions
                </li>
            </ul>
        </div>
    </body>
</html>
    """)


@app.get("/movies")
async def parent_data(title: str, include_descriptions: bool = False) -> dict:
    ia = Cinemagoer()
    movies = ia.search_movie(title)
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail="Parent's guide not found")
    movie = movies[0]
    title = movie['title']
    data = ia.get_movie_parents_guide(movie.getID())['data']
    if not include_descriptions:
        data = data['advisory votes']
    else:
        data.pop('certificates', None)

    return {
        'title': title,
        'data': data
    }
