import eel
from backend import export


if __name__ == "__main__":
    eel.init('frontend')
    eel.start(
        'templates/home.html',
        size=(1000, 600),
        jinja_templates='templates'
    )
