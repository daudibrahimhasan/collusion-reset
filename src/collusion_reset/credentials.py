"""Local credential selection. No key rotation, provider calls or secret output."""

import os

from collusion_reset.episode_smoke import ROOT


def groq_settings(model=None):
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False, interpolate=False)
    slot = os.environ.get('GROQ_KEY_SLOT', 'GROK_1')
    if slot not in {f'GROK_{i}' for i in range(1, 6)}:
        raise ValueError('GROQ_KEY_SLOT must be GROK_1 through GROK_5')
    key = os.environ.get(slot, '').strip()
    if not key:
        raise ValueError(f'Add the selected credential to {slot} in the local .env')
    model = model or os.environ.get('GROQ_MODEL', '')
    if not model.startswith('groq/') or not model.removeprefix('groq/'):
        raise ValueError('Choose an explicit groq/<model-id> route')
    if os.environ.get('GROQ_FREE_TIER_CONFIRMED', '').lower() != 'true':
        raise ValueError('Verify no paid billing in the console, then set GROQ_FREE_TIER_CONFIRMED=true')
    try:
        limit = int(os.environ.get('GROQ_MAX_REQUESTS', '100'))
    except ValueError:
        raise ValueError('GROQ_MAX_REQUESTS must be a positive integer') from None
    if limit < 1:
        raise ValueError('GROQ_MAX_REQUESTS must be a positive integer')
    return {'model': model, 'key': key, 'slot': slot, 'max_requests': limit}


class BoundedCompletion:
    """One key and model; finite call budget; sanitized provider failures."""

    def __init__(self, completion, settings):
        self.completion = completion
        self.settings = settings
        self.attempted = 0

    def __call__(self, **kwargs):
        if kwargs.get('model') != self.settings['model']:
            raise RuntimeError('Model change forbidden within this run')
        if self.attempted >= self.settings['max_requests']:
            raise RuntimeError('Request cap reached; stopped without switching accounts')
        self.attempted += 1
        kwargs.update(api_key=self.settings['key'], num_retries=0, timeout=60)
        try:
            return self.completion(**kwargs)
        except Exception as error:
            # Do not propagate provider text that might include credentials.
            status = getattr(error, 'status_code', None)
            status = status if type(status) is int else 'unknown'
            raise RuntimeError(f'Groq request failed (HTTP {status}); stopped without account fallback') from None
