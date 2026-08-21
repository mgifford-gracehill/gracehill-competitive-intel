import json, glob, re

# ---------- hand-authored "when it comes up" for every Do-not-compete / Partner record ----------
WIC = {
"udemy-business": dict(
 why="Udemy Business is a content marketplace, not a compliance system. Nobody buys it to prove a fair housing course was completed by a named employee on a date. If a customer has it, they bought general professional development for corporate staff.",
 say="Udemy's great for the general skills stuff — Excel, leadership, whatever your corporate team wants to take. It's a different job to what we do. We're the system that proves a specific person was trained on a specific regulation, and produces the record when someone asks for it.",
 avoid="Don't compare catalog sizes. Theirs is enormous and you'll lose that exchange — and it's not the reason anyone buys either product.",
 redirect="If you had a fair housing complaint next month, what would you hand the investigator?"),
"opensesame": dict(
 why="OpenSesame aggregates courses and delivers them into whatever LMS the customer already has. It has no platform of its own, so it isn't competing for the same seat. It does carry an exclusive IREM collection that includes fair housing.",
 say="OpenSesame's a library — they license content into whatever system you already run. Worth knowing they carry the IREM collection, so if you've got that, you've got some real property management content. The question is what's delivering it and what's tracking it.",
 avoid="Never say OpenSesame has no fair housing or property management content. They carry IREM's collection and a rep who claims otherwise gets corrected on the spot.",
 redirect="Which system is actually assigning and tracking those courses today?"),
"amplifire": dict(
 why="Amplifire sells confidence-based assessment — finding where people are confidently wrong. It's a genuinely good idea and it's almost never bought by a multifamily operator for compliance.",
 say="Amplifire does something interesting — they measure not just whether someone got it right but whether they were sure. It's mostly a healthcare and enterprise thing. Not something we bump into.",
 avoid="Don't dismiss the idea itself. If a prospect is excited about it, they're telling you completion tracking isn't enough for them — that's a competency conversation, and it's a good one.",
 redirect="It sounds like knowing they finished the course isn't the bar for you. What would you actually need to see?"),
"axonify": dict(
 why="Frontline microlearning built for retail and distribution floors. When it shows up in a multifamily deal it's because a corporate parent already owns the contract, not because someone shortlisted it against us.",
 say="Axonify's a frontline enablement tool — big in retail and warehouse. If your corporate group already has it, that's fine, it's solving a different problem than multifamily compliance.",
 avoid="Don't argue against daily microlearning as a concept — the research behind it is solid and you'll sound defensive.",
 redirect="Does that cover your onsite property teams, or is it aimed at a different part of the business?"),
"coursebox": dict(
 why="An AI authoring tool with a light LMS attached. Its appearance is a signal, not a threat — someone is thinking about building compliance content themselves.",
 say="Coursebox is an authoring tool — it helps you make courses fast. The thing to think through is who owns those courses eighteen months from now when the law in three of your states has changed.",
 avoid="Don't mock AI-generated content. Say who maintains it instead — that's the real question and it's one they haven't thought about.",
 redirect="If you build it yourself, who's responsible for keeping it current, and how do they find out a rule changed?"),
"learnie": dict(
 why="User-generated microlearning video. It's bought for culture and peer knowledge sharing, not to satisfy a compliance requirement.",
 say="Learnie's a peer-to-peer video thing — teams recording tips for each other. Honestly it's a decent culture tool. It just isn't what you'd point a regulator at.",
 avoid="Don't position it as a failed LMS. It isn't trying to be one.",
 redirect="Is this about people sharing what works, or about proving what they were required to know?"),
"adobe-learning-manager": dict(
 why="An enterprise LMS sold inside a marketing-technology stack. It reaches multifamily through a corporate marketing or franchise relationship, not through an operations evaluation.",
 say="Adobe Learning Manager usually arrives through the marketing side of the house. It's a capable platform — it's just not built around multifamily regulation or property roles.",
 avoid="Don't fight Adobe on platform capability. You will lose and it's not the point.",
 redirect="Who owns that relationship internally — marketing, or the operations team who'd actually use this?"),
"learning-pool": dict(
 why="A UK-headquartered LMS/LXP with off-the-shelf compliance content, mostly reaching North America through a globally headquartered owner.",
 say="Learning Pool is strong in the UK public and enterprise space. If it's here it's usually because a parent company standardized on it globally.",
 avoid="Don't treat it as a live multifamily threat — it will read as unfamiliarity with the market.",
 redirect="Is this a global standard you have to work within, or is the US portfolio free to choose?"),
"seismic-learning": dict(
 why="Sales enablement and revenue-team coaching. If it's present, someone is trying to improve leasing conversion, not run a compliance program.",
 say="Seismic is a sales enablement platform — it's about coaching a revenue team. If leasing performance is what you're chasing, that's a real conversation, it's just a different one from compliance and policy.",
 avoid="Don't conflate leasing coaching with fair housing training. They're separate budgets and separate buyers.",
 redirect="Are we talking about making leasing better, or about making sure everyone's trained on what they're legally required to know?"),
"sana-learn": dict(
 why="Workday acquired Sana, so where a large owner-operator runs Workday it will be offered as the learning layer at a price that's hard to argue with.",
 say="If you're on Workday, Sana's going to get offered to you and the pricing will look good. That's a real consideration. What it won't come with is multifamily-specific content or anyone maintaining it as regulation changes.",
 avoid="Don't argue against the consolidation logic — it's sound. Argue about what fills the platform.",
 redirect="If you go that route, where does the multifamily content come from, and who keeps it current?"),
"escal8": dict(
 why="The company appears to have pivoted away from the multifamily talent-development LMS a prospect may be remembering. Confirm which product they actually saw before responding.",
 say="Escal8's changed direction — worth checking which product you looked at, because it isn't the multifamily LMS it used to be.",
 avoid="Don't assume you know what they saw. Guessing here makes you look uninformed.",
 redirect="When did you see it, and what were they showing you?"),
"appfolio-staffing-training": dict(
 why="AppFolio's training is product enablement — teaching customers to use AppFolio. It isn't a compliance or fair housing program, which makes AppFolio accounts effectively greenfield.",
 say="What AppFolio gives you is training on AppFolio — how to use the software. That's useful and it's not the same as fair housing, harassment or policy training for your onsite teams.",
 avoid="Don't imply AppFolio's training is poor. It's good at what it's for.",
 redirect="Where does your fair housing and compliance training come from today?"),
"realty-share": dict(
 why="A document management platform built on SharePoint. If it's already deployed, displacing it is an IT project nobody wants — but it holds documents, it doesn't author policy.",
 say="If REALTY|share is already in, keep it. It's where documents live. What we bring is the actual multifamily policy content and the attestation trail — that sits on top rather than replacing anything.",
 avoid="Don't propose ripping out a system IT chose. You'll lose the room.",
 redirect="Where do the policies themselves come from today — who writes them and who updates them?"),
"tour24": dict(
 why="Self-guided physical tour access. A Tour24 prospect still needs media of the unit — the two products sit next to each other rather than against each other.",
 say="Tour24 handles getting someone into the building on their own schedule. That's a genuinely different problem from what the prospect sees before they decide to come. They work fine together.",
 avoid="Don't manufacture a fight here. Reps who do it sound like they don't understand either product.",
 redirect="Once they've booked that self-guided tour, what are they actually looking at online beforehand?"),
"rentcast": dict(
 why="RentCast is self-serve rent estimates sold to individual investors and small landlords at $12 a month. It isn't bidding for an institutional operator's market intelligence budget.",
 say="RentCast is built for individual investors — someone with a handful of doors checking what a house should rent for. Different buyer entirely from portfolio-level comps and concession tracking.",
 avoid="Do not get into a coverage-number comparison. RentCast publishes 150M+ property records because it counts single-family across the whole country. Quoting HelloData's multifamily number against it looks like losing.",
 redirect="What decision are you trying to make with this — pricing a specific unit, or seeing what your comp set is doing on concessions week to week?"),
"rentgrata": dict(
 why="Resident referral and prospect-to-resident messaging, now owned by Opiniion. It coexists with surveys rather than replacing them.",
 say="Rentgrata connects prospects to current residents — it's a referral and social proof play. It's not a listening program and it won't tell you why people leave.",
 avoid="Never position it as a surveys competitor. It isn't one, and Opiniion owning it is the part that actually matters.",
 redirect="Separate from what prospects hear from residents, how are you finding out what residents are actually experiencing?"),
"yext": dict(
 why="Local SEO and listings infrastructure. It manages where your properties appear, not what residents are saying or what your teams do about it.",
 say="Yext is listings infrastructure — making sure your properties show up correctly everywhere. That's real work and it's upstream of us. We're about the review conversation itself and what happens after it.",
 avoid="Don't claim we do listings management better. Be precise about the boundary.",
 redirect="Once someone finds the property and reads the reviews, who's responding, and how fast?"),
"chatmeter": dict(
 why="Horizontal multi-location reputation management serving restaurants, retail and healthcare. When it appears it's usually an enterprise CX evaluation, often run by marketing.",
 say="Chatmeter's a multi-location platform — restaurants, retail, that world. It's capable. The difference is whether you want reputation benchmarked against other multifamily properties or against locations generally.",
 avoid="Don't claim they can't do multifamily. They can. The argument is benchmark relevance, not capability.",
 redirect="When you look at a property's score, what do you want to compare it to?"),
"vendasta": dict(
 why="A white-label platform sold to agencies, who then resell to operators. You only meet it behind an agency's logo, which means the real relationship is with the agency.",
 say="Vendasta's the engine behind a lot of agency offerings — you're probably seeing it branded as something else. If an agency's running your reputation work, the question is what they hand back to your onsite teams.",
 avoid="Don't attack the agency. They may be a channel, and the buyer chose them.",
 redirect="Does what the agency does reach the property teams, or does it stop at a monthly report?"),
"eliseai": dict(
 why="EliseAI is a Grace Hill partner — there's a jointly published resident survey report and an active partnership. Their SentimentAI product does create genuine scope overlap on resident feedback, which makes this a relationship question rather than a competitive one.",
 say="We work with EliseAI — we've published joint research with them. They're strong at the leasing conversation. If resident sentiment is coming up, that's worth a conversation with both of us in the room rather than either of us pitching against the other.",
 avoid="Do not use competitive language about EliseAI, and do not speculate about anything to do with the partnership arrangement. If a prospect is weighing SentimentAI against our surveys, escalate before you respond.",
 redirect="Are you looking for feedback at the leasing moment, or an ongoing benchmarked listening program across the resident lifecycle?"),
"siro": dict(
 why="Conversation intelligence for in-person selling — recording and coaching real interactions. It's a replacement-category threat to sampled mystery shopping, not a vendor we out-feature.",
 say="Siro records and coaches the conversations your team is actually having. That's more coverage than a sample of shops, and it's fair to say so. What it can't do is test the experience of someone who isn't already talking to you — the community that never picks up, the email nobody answered.",
 avoid="Do not argue shop quality or shopper training, and do not try to win on volume. You'll be comparing a sample to continuous coverage and you will lose that comparison on its own terms.",
 redirect="How would you find out about the prospect who called and nobody answered?"),
}

# ---------- stack layer mapping ----------
STACK = json.load(open('data/stack.json'))['layers']
LNAME = {l['number']: l['name'] for l in STACK}
def layer_for(r):
    tc = (r.get('toolCategory') or '').lower(); ci = r.get('ciCategory') or ''
    n = None; note = ''
    if ci == 'Status Quo':
        return {"number": None, "name": "No layer — the buyer's current habit",
                "note": "Not a vendor. This is what happens when nobody buys anything."}
    if any(k in tc for k in ['property management system','pms','erp']): n, note = 0, 'Owns the ledger. Records what happened.'
    elif any(k in tc for k in ['leasing agent','crm','tour','virtual tour','video','listing','self-guided','3d scanning','marketplace for renters']): n, note = 1, 'Sits in demand and leasing, upstream of the resolution loop.'
    elif any(k in tc for k in ['resident','referral','service','maintenance work']): n, note = 2, 'Resident living and service.'
    elif any(k in tc for k in ['access control','smart','iot']): n, note = 3, 'Physical and connected property.'
    elif any(k in tc for k in ['hcm','hris','payroll','human resource','talent','employee engagement','learning management','lms','lxp','microlearning','course','learning platform','authoring','enablement']): n, note = 4, 'Arrives through the people and workforce stack, often on an HR contract.'
    elif any(k in tc for k in ['market','rent comparable','property data','analytics']): n, note = 6, 'Feeds market context in; sits closer to asset and finance.'
    elif any(k in tc for k in ['reputation','review','survey','mystery shop','conversation intelligence','policy','document management','compliance']): n, note = 5, 'Competes for the resolution layer position, or a slice of it.'
    if n is None: return {"number": None, "name": "Outside the multifamily stack", "note": "No natural position in the operator stack."}
    return {"number": n, "name": LNAME.get(n, ''), "note": note}

# ---------- derived when-it-comes-up for the rest ----------
def derive_wic(r):
    v = r.get('verdict') or {}
    gaps = [g['text'] for g in (r.get('gaps') or [])]
    ask = r.get('askThis') or []
    dns = r.get('doNotSay') or []
    stance = v.get('stance')
    if stance == 'Compete':
        why = f"A real head-to-head. {v.get('line','')}"
        say = ("Acknowledge what they do well, then move the conversation to the ground in 'Win with' — "
               "don't open with a feature list.")
    else:
        why = f"Overlaps in part, not in whole. {v.get('line','')}"
        say = ("Concede the part they genuinely own, then be specific about the part they don't. "
               "Partial overlap is where reps over-claim and lose credibility.")
    return {"why": why, "say": say,
            "avoid": dns[0] if dns else "Don't state an absolute negative about their product. Ask instead.",
            "redirect": ask[0] if ask else "What would have to be true for this to be solved?",
            "derived": True}

# ---------- per-competitor SPICED ----------
def spiced_for(r):
    n = r.get('name'); tc = (r.get('toolCategory') or 'this tool').lower()
    gaps = [g['text'] for g in (r.get('gaps') or [])]
    ask = r.get('askThis') or []
    v = r.get('verdict') or {}
    aka = ', '.join(r.get('aka') or []) or n
    unknown = [k for k,f in (r.get('features') or {}).items() if f.get('support')=='Unknown']
    return [
      {"letter":"S","stage":"Situation",
       "listenFor": f"They name {aka}, or describe {tc} already in place.",
       "ask": ask[0] if ask else f"What are you using today, and how did {n} come into the picture?"},
      {"letter":"P","stage":"Pain",
       "listenFor": gaps[0] if gaps else f"Frustration that {n} isn't reaching the onsite team.",
       "ask": ask[1] if len(ask)>1 else f"What's not working about how that runs today?"},
      {"letter":"I","stage":"Impact",
       "listenFor": "Whether the gap costs them money, time or exposure — or is just an annoyance.",
       "ask": "If that stayed exactly as it is for another year, what does it cost you?"},
      {"letter":"CE","stage":"Critical Event",
       "listenFor": f"A renewal date on the {n} contract, an audit, an acquisition, or new leadership asking what the data shows.",
       "ask": f"When does the {n} agreement come up, and what has to be decided before then?"},
      {"letter":"D","stage":"Decision Process",
       "listenFor": f"Whether {n} sits on someone else's budget line — that changes who has to agree.",
       "ask": ask[2] if len(ask)>2 else "Who else has to be comfortable with this, and what do they need to see?"},
    ]

# ---------- apply ----------
counts = {'wic_authored':0,'wic_derived':0,'spiced':0,'layer':0}
for f in glob.glob('data/records/*.json'):
    recs = json.load(open(f)); changed=False
    for r in recs:
        r['stackLayer'] = layer_for(r); counts['layer']+=1
        if r['id'] in WIC:
            r['whenItComesUp'] = WIC[r['id']]; counts['wic_authored']+=1
        else:
            r['whenItComesUp'] = derive_wic(r); counts['wic_derived']+=1
        r['spiced'] = spiced_for(r); counts['spiced']+=1
        changed=True
    if changed: json.dump(recs, open(f,'w'), indent=2, ensure_ascii=False)
print(counts)
missing = [k for k in WIC if not any(r['id']==k for f in glob.glob('data/records/*.json') for r in json.load(open(f)))]
print('authored ids not found in data:', missing)
