

def make_stub(raw_string):
    return ''.join(e for e in raw_string.replace(' ', '_') if (e.isalnum() or e == '_')).lower()