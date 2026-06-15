import json
from pathlib import Path


FAILURE_FILE = Path(
    "storage/failed_youtube_urls.json"
)


def save_failed_url(
    url: str,
    video_id: str,
    reason: str
):

    failures = []

    if FAILURE_FILE.exists():

        with open(
            FAILURE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            failures = json.load(f)

    failures.append({

        "url": url,

        "video_id": video_id,

        "reason": reason
    })

    FAILURE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        FAILURE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            failures,
            f,
            indent=4,
            ensure_ascii=False
        )