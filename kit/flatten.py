"""Flatten nested JSON into editable key/label/value rows, and set values back by path."""
import json, re

def _label(seg):
    s = re.sub(r'\[(\d+)\]', r' \1', seg)
    s = re.sub(r'(?<!^)(?=[A-Z])', ' ', s)
    return s.replace('_',' ').strip().capitalize()

def flatten(obj, prefix='', section=''):
    """Yield (key, section, item, value) for every editable string leaf."""
    rows = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{prefix}.{k}' if prefix else k
            sec = section or _label(k)
            if isinstance(v, str):
                rows.append((p, section or 'General', _label(k), v))
            elif isinstance(v, (dict, list)):
                rows += flatten(v, p, sec if prefix else _label(k))
            elif v is None:
                rows.append((p, section or 'General', _label(k), ''))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f'{prefix}[{i}]'
            if isinstance(v, str):
                rows.append((p, section, f'{prefix.split(".")[-1]} {i+1}', v))
            elif isinstance(v, dict):
                nm = v.get('name') or v.get('step') or v.get('stage') or v.get('title') or v.get('id') or v.get('approach') or v.get('form') or v.get('tier') or v.get('layer') or v.get('item') or v.get('objection') or v.get('stat') or f'{i+1}'
                rows += flatten(v, p, f'{section} · {nm}' if section else str(nm))
    return rows

def get_path(root, path):
    cur = root
    for seg in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        if seg.startswith('['):
            i = int(seg[1:-1])
            if not isinstance(cur, list) or i >= len(cur): return None
            cur = cur[i]
        else:
            if not isinstance(cur, dict) or seg not in cur: return None
            cur = cur[seg]
    return cur

def set_path(root, path, value):
    segs = re.findall(r'[^.\[\]]+|\[\d+\]', path)
    cur = root
    for j, seg in enumerate(segs[:-1]):
        nxt = segs[j+1]
        if seg.startswith('['):
            i = int(seg[1:-1])
            while isinstance(cur, list) and len(cur) <= i: cur.append({} if not nxt.startswith('[') else [])
            cur = cur[i]
        else:
            if seg not in cur or cur[seg] is None:
                cur[seg] = [] if nxt.startswith('[') else {}
            cur = cur[seg]
    last = segs[-1]
    if last.startswith('['):
        i = int(last[1:-1])
        while len(cur) <= i: cur.append('')
        cur[i] = value
    else:
        cur[last] = value
    return True
