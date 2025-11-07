"""Tiny AI helpers (placeholders).

Replace contents with real AI calls (e.g., OpenAI) when ready. Keep the same
function signatures to avoid touching views or forms.
"""

from typing import List


KEYWORDS = {
    'web': 'Web Development',
    'site': 'Web Development',
    'seo': 'SEO/Content',
    'content': 'SEO/Content',
    'logo': 'Branding/Design',
    'brand': 'Branding/Design',
    'ads': 'Advertising',
    'facebook': 'Advertising',
    'tiktok': 'Advertising',
}


def classify_job_text(text: str) -> str:
    """Return a very small rule-based category suggestion.

    This is intentionally simple. Swap this with an LLM call, e.g.:

        import openai, os
        openai.api_key = os.environ['OPENAI_API_KEY']
        # call the model with `text` and return a short label

    """
    if not text:
        return ''
    t = text.lower()
    for kw, cat in KEYWORDS.items():
        if kw in t:
            return cat
    return ''


def match_providers(job) -> List[int]:
    """Return a mock list of provider IDs.

    Replace with your own matching logic or AI ranking and fetch real users.
    """
    return []


