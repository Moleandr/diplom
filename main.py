if __name__ == "__main__":
    try:
        import eel
        from backend import export
        import traceback
        eel.init('frontend')

        eel.start(
            'templates/home.html',
            size=(1000, 600),
            jinja_templates='templates'
        )
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        input()
