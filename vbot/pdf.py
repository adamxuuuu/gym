from unstructured.cleaners.core import clean, clean_ordered_bullets, clean_non_ascii_chars
import re

def clean_text(text: str):
    text = clean(text, bullets=True, extra_whitespace=True, dashes=True)
    text = clean_non_ascii_chars(text)
    text = clean_ordered_bullets(text)
    re.sub(r'.{2,}', '', text)
    re.sub(r'-{2,}', '', text)
    re.sub(r'_{2,}', '', text)

if __name__ == "__main__":
    print()