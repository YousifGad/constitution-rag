import re
import unicodedata

DIACRITICS = re.compile("[\u064b-\u0652\u0670]")
DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)  # split diacritics from letters
    text = text.replace("\u0640", "")  # remove tatweel
    text = DIACRITICS.sub("", text)  # remove diacritics
    
    # normalize alef variants
    for variant in ['أ', 'إ', 'آ', 'ٱ']:
        text = text.replace(variant, 'ا')
        
    # normalize Yeh
    text = text.replace('ى', 'ي')
    
    text = text.translate(DIGITS)
    return " ".join(text.split())