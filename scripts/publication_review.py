"""Reviewed public copy; archived source data remains unchanged."""
from pathlib import Path
from html import escape,unescape
import json,re
ROOT=Path(__file__).resolve().parents[1]
OVERRIDES=json.loads((ROOT/'content/publication-overrides.json').read_text())
EDITS=json.loads((ROOT/'content/publication-copy-edits.json').read_text())
def edited_text(text):
 for rule in EDITS:text=text.replace(rule['old'],rule['new'])
 return text

def public_html(html):
 # Exact reviewed source blocks, not a blanket keyword filter.
 for item in OVERRIDES:html=html.replace(item['original_html'],item['html'])
 # Edit only text between tags; never modify scripts, styles, attributes or IDs.
 def replace(match):
  raw=match.group(1);text=unescape(raw);new=edited_text(text)
  return '>'+ (escape(new,quote=False) if new!=text else raw)+'<'
 return re.sub(r'>([^<>]*)<',replace,html)
