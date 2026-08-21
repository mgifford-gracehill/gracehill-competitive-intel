"""Turn Ruth's review into detectors. Every class of defect she found on one page,
counted across all 98 records. Facts are auto-fixable; claims queue."""
import json,re,sys,collections

C=json.load(open('data/competitors.json'))
C=C if isinstance(C,list) else C.get('competitors',C)
GHB=json.load(open('data/gh-baseline.json'))

# Which fields are rep-facing claims vs facts. Ruth's edits were almost all in claim fields.
CLAIM=['positioning','whyWeWin','verdict','weaknesses','play','doNotSay','sayThat']
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,f'{path}.{k}' if path else k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from walk(v,f'{path}[{i}]')
    elif isinstance(o,str): yield path,o

# Reviewed-and-correct hits. A detector fires on words, not meaning, so a line can
# contain "obligation" while correctly saying the obligation is the customer's. Once a
# human confirms a hit is fine it goes here, keyed by id + field + a hash of the text —
# so if the text is later edited the hash changes and it surfaces again for re-review.
try:
    ALLOW = set(tuple(x) for x in json.load(open('audit-allowlist.json')))
except FileNotFoundError:
    ALLOW = set()
def ok(cls, cid, path, txt):
    import hashlib
    h = hashlib.sha1(txt.encode()).hexdigest()[:10]
    return [cls, cid, path, h] and (cls, cid, path, h) in ALLOW
def key(cls, cid, path, txt):
    import hashlib
    return [cls, cid, path, hashlib.sha1(txt.encode()).hexdigest()[:10]]

D=collections.defaultdict(list)
SUPPRESSED=[]

# A. Absolute constructions — makes a nuanced thing sound settled.
ABS=[r'\bis not the problem\b',r'\bmeans nothing\b',r'\bchanges nothing\b',r'\bno one else\b',
     r'\bnobody else\b',r'\bthe only (?:vendor|platform|one|company)\b',r'\balways\b',
     r'\bnever (?:wins|works|matters)\b',r'\bcannot compete\b',r'\bhas no\b']
# C. Grace Hill assuming the customer's responsibility.
OBL=[r'\bobligation\b',r'\bresponsible for\b',r'\bguarantee',r'\bensures compliance\b',
     r'\bcontractually\b',r'\bwe own\b',r'\bassumes? (?:the )?(?:customer|client)']
# D. Confrontational / fear questions.
FEAR=[r'who is accountable',r'when a claim',r'\bif .{0,40}(?:fails|is out of date|goes wrong)',
      r'\bwho pays\b',r'\bexposed\b.*\?',r'\bliab']
# I. Jargon flagged by the Punchy skill and the brand voice skill.
JARG=['actionable insight','streamline','comprehensive platform','best-in-class','drive results',
      'seamless','robust','world-class','cutting-edge','game-chang','revolutionary','synerg',
      'unlock','next-gen','turnkey','holistic','frictionless','future-proof','paradigm']

for c in C:
    cid=c.get('id','?')
    for path,txt in walk(c):
        isclaim=any(path.startswith(f) or f'.{f}' in path for f in CLAIM)
        low=txt.lower()
        # Guardrail fields exist to PROHIBIT these patterns. A match there is the
        # control working, not a defect. Excluding them is what turns a noisy
        # regex into a usable linter.
        if any(g in path for g in ('doNotSay','.avoid','reviewNote','languageToAvoid')):
            continue
        def hit(cls):
            if ok(cls,cid,path,txt): SUPPRESSED.append(cls); return
            D[cls].append((cid,path,txt[:110]))
        if any(re.search(p,low) for p in ABS):  hit('A_absolute')
        if any(re.search(p,low) for p in OBL):  hit('C_obligation')
        if any(re.search(p,low) for p in FEAR): hit('D_fear')
        for j in JARG:
            if j in low: D['I_jargon'].append((cid,path,j))
        # B. Aphorism: short claim-field sentence built on an "X, not Y" or em-dash pivot.
        if isclaim and len(txt)<150 and re.search(r'(—|,)\s*(not|it is|that is)\b',low) and txt.count('.')<=1:
            hit('B_aphorism')

# J. Grace Hill customer or prospect named anywhere. Sourced from Salesforce
# opportunities, Jira assignment records and RFP responses. This is the one rule
# with a cost that lands outside the company, so it is a must-fix and it gets its
# own detector rather than relying on anyone remembering.
CUSTOMERS=['venterra','fogelman','ram partners','camden development','redstone residential',
 'lynd company','11residential','hackberry lane','moinian','rpm development','schaumburg towers',
 'franklin group','idi logistics','max properties','harbor group','picerne','dayrise','akara',
 'westhome','perennial properties','drucker falk','northwood ravin']
for f in ['data/gh-baseline.json','data/gh-index.json','data/products.json','data/playbook.json',
          'data/pitch.json','data/competitors.json','data/gh-context.json','data/personas.json']:
    try: blob=open(f).read()
    except FileNotFoundError: continue
    low=blob.lower()
    for name in CUSTOMERS:
        i=low.find(name)
        while i>=0:
            ctx=blob[max(0,i-260):i+len(name)+120]
            # An approved, attributed public testimonial is consented and the brand
            # voice guide requires the attribution. What this rule is for is a
            # customer named in a competitive comparison, or a prospect in the
            # pipeline. Scope the detector to that.
            # The playbook models this deliberately: customerStories carries an
            # `anonymous` flag, and 20 of 22 are named because they are approved
            # public case studies. Respect that structure rather than fighting it.
            testimonial=any(k in ctx for k in ('Success Story','Playbook','"quote"','Testimonial',
                                               'VP of','Director of','VP Property','Vice President',
                                               '"customer":','customerStories','Case_Studies','case study'))
            if not testimonial:
                D['J_customer_named'].append((f.split('/')[-1],name,ctx[190:].replace(chr(10),' ')))
            i=low.find(name,i+1)

# F. Over-indexing on one Grace Hill strength.
for c in C:
    blob=json.dumps({k:v for k,v in c.items() if k in CLAIM}).lower()
    fh=blob.count('fair housing')
    if fh>=3: D['F_fairhousing_heavy'].append((c.get('id'),'claim fields',f'{fh} mentions'))

# G. Grace Hill claims still resting on marketing pages or internal decks.
for k,v in GHB.items():
    s=(v.get('source') or '')
    sl = s.lower()
    if not any(ok in sl for ok in ('adminhq', 'rfp response', 'catalog.gracehill.com')):
        tag='no source' if not s else ('internal deck' if ('battle card' in s.lower() or 'playbook' in s.lower() or 'internal' in s.lower()) else 'marketing page / web')
        D['G_unsourced_GH'].append((k,tag,s[:80]))
# H. A four-way value carrying no note to hold the nuance.
for k,v in GHB.items():
    if not (v.get('note') or '').strip(): D['H_no_note'].append((k,v.get('support'),''))

order=['J_customer_named','C_obligation','D_fear','A_absolute','B_aphorism','I_jargon','F_fairhousing_heavy','G_unsourced_GH','H_no_note']
NAMES={'J_customer_named':'Grace Hill customer or prospect named  [MUST FIX]',
 'C_obligation':'Grace Hill implying it owns the customer\'s compliance  [MUST FIX]',
 'D_fear':'Confrontational or fear-framed question  [MUST FIX]',
 'A_absolute':'Nuance stated as absolute  [MUST FIX]',
 'B_aphorism':'Punchy aphorism in a claim field — "sounds generated"  [ITERATIVE]',
 'I_jargon':'Jargon flagged by brand voice / Punchy  [ITERATIVE]',
 'F_fairhousing_heavy':'Over-indexed on Fair Housing as the differentiator  [ITERATIVE]',
 'G_unsourced_GH':'Grace Hill claim not yet sourced to AdminHQ  [ITERATIVE]',
 'H_no_note':'Yes/Partial/No with no note to hold the nuance  [MUST FIX]'}
MUST=['J_customer_named','C_obligation','D_fear','A_absolute','H_no_note']
def summary():
    return {k:len(v) for k,v in D.items()}
def gate():
    """Classes where being wrong lands on someone outside the room. These block a build."""
    return {k:D[k] for k in MUST if D[k]}
if __name__!='__main__':
    pass
print(f'{len(C)} competitor records · {len(GHB)} Grace Hill capability claims\n')
for k in order:
    rows=D[k]
    recs=len({r[0] for r in rows})
    print(f'{NAMES[k]}\n  {len(rows)} hits across {recs} records')
    for r in rows[:4]: print(f'    · {r[0]} :: {r[1]} :: {r[2]}')
    if len(rows)>4: print(f'    … {len(rows)-4} more')
    print()
if SUPPRESSED:
    c=collections.Counter(SUPPRESSED)
    print(f'suppressed as reviewed-and-correct: {sum(c.values())}  ({", ".join(f"{k} {v}" for k,v in sorted(c.items()))})')
json.dump({k:v for k,v in D.items()},open('audit-findings.json','w'),indent=1)

# Emit an allowlist-ready block for whatever is currently open, so triage is a copy-paste.
if '--emit-allowlist' in sys.argv:
    out=[]
    for c in C:
        for path,txt in walk(c):
            if any(g in path for g in ('doNotSay','.avoid','reviewNote','languageToAvoid')): continue
            low=txt.lower()
            for cls,pats in (('A_absolute',ABS),('C_obligation',OBL),('D_fear',FEAR)):
                if any(re.search(p,low) for p in pats) and not ok(cls,c['id'],path,txt):
                    out.append(key(cls,c['id'],path,txt))
    json.dump(out,open('audit-open.json','w'),indent=1)
    print(f'wrote audit-open.json — {len(out)} open must-fix hits, ready to triage')
