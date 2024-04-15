import locale
import gettext
import os
LOCAL = True
# _podir = os.path.join(os.path.dirname(__file__), "po")
translation = gettext.translation("main", "po", fallback=True)
_, ngettext = translation.gettext, translation.ngettext

LOCALES = {
    ("ru_RU"): gettext.translation("main", "po", fallback=True),
    ("en_US"): gettext.NullTranslations(),
}

def ngettext(*args):
    if not LOCAL:
        return LOCALES['en_US'].ngettext(*args)
    return LOCALES['ru_RU'].ngettext(*args)



while s:= input():
    if s == 'change':
        LOCAL = not LOCAL
    n = len(s.split())
    
    print(ngettext("Entered {} word", "Entered {} words", n).format(n))
