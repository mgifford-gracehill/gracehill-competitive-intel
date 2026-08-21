import json, base64, pathlib
A=pathlib.Path('/root/.claude/skills/synced/gracehill-branding-official/assets')
L=lambda n: json.load(open(f'data/{n}.json'))
data={'competitors':L('competitors'),'features':L('features'),'news':L('news'),
      'products':L('products'),'positioning':L('positioning'),'built':'August 11, 2026'}
logo='data:image/svg+xml;base64,'+base64.b64encode((A/'GH-CorporateLogo-AllWhite.svg').read_bytes()).decode()
p=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</script>','<\\/script>')
out=pathlib.Path('template.html').read_text().replace('__DATA__',p).replace('__LOGO__',logo)
f=pathlib.Path('Grace-Hill-Competitive-Intelligence.html'); f.write_text(out,encoding='utf-8')
print(f'built {f} — {f.stat().st_size/1024/1024:.2f} MB · {len(data["competitors"])} competitors')
