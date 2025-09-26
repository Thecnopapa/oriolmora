PROJECT_ID = "oriolmora"
STATIC_FOLDER = "static"
UPLOAD_FOLDER = "uploads"
APPLICATION_ROOT = "/web"
DATABASE_URL = "https://firestore.googleapis.com/v1/projects/oriolmora/"
STORAGE_URL = "https://firebasestorage.googleapis.com/v0/b/oriolmora.firebasestorage.app/o/{}%2F{}?alt=media"
STORAGE_URL_SINGLE = "https://firebasestorage.googleapis.com/v0/b/oriolmora.firebasestorage.app/o/{}?alt=media"


SECRET_URLS = dict(
    flask = "projects/1050223961125/secrets/flask/versions/1",
    service_account = "projects/1050223961125/secrets/service_account/versions/1",
)












# DEVELOPMENT
NGROK_URL = "https://funny-constantly-peacock.ngrok-free.app"