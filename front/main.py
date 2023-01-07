import eel

# eel.init('web')


if __name__ == "__main__":
    eel.init('web')
    eel.start(
        'templates/base.html',
        size=(1000, 1000),
        jinja_templates='templates'
    )
