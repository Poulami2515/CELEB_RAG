import instaloader

from src.media.instagram_media_ingestor import create_instaloader

loader = create_instaloader()

print("Logged in as:", loader.test_login())

profile = instaloader.Profile.from_username(
    loader.context,
    "iamsrk"
)

print(profile.username)