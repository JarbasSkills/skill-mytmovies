import json
import shutil
from os.path import dirname, isfile

from youtube_archivist import YoutubeMonitor

archive = YoutubeMonitor(db_name="MytMovies",
                         min_duration=30 * 60,
                         blacklisted_kwords=["trailer", "teaser", "movie scene",
                                             "movie clip", "behind the scenes",
                                             "Movie Preview", "Documentary", "Episode",
                                             "soundtrack", " OST", "opening theme"])

# load previous cache
cache_file = f"{dirname(dirname(__file__))}/bootstrap.json"
if isfile(cache_file):
    try:
        with open(cache_file) as f:
            data = json.load(f)
            archive.db.update(data)
            archive.db.store()
    except:
        pass  # corrupted for some reason

    shutil.rmtree(cache_file, ignore_errors=True)

for url in [
    "https://www.youtube.com/c/SuperheroMovieClip"
]:
    # parse new vids
    archive.parse_videos(url)

# save bootstrap cache
shutil.copy(archive.db.path, cache_file)
