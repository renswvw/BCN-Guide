import gettext

language_from_code = {"ca": "Català", "es": "Castellano", "en": "English", "nl": "Nederlands"}

def init_translator(language):
    try:
        localizator = gettext.translation(
            "base", localedir="locales", languages=[language]
        )
        localizator.install()
        tranlator_fn = localizator.gettext
    except Exception:
        tranlator_fn = gettext.gettext
    return tranlator_fn