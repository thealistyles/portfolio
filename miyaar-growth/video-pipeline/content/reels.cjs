// Miyaar Developers reels + posts. Every claim comes from miyaardevelopers.com (prices, materials, timelines, cities, portfolio).
// Scene types: photo (img + Ken Burns), clip (segment of a video in assets/), card (price | list | compare), cta.
// clip: { src: 'plot-to-keys.mp4', from: seconds }  -> render.js extracts the frames.
const P = 'plot-to-keys.mp4';
const C = (from) => ({ src: P, from });
const CTA = (h, sub) => ({ type: 'cta', dur: 3, img: 'hero-dha-residence.jpg', h, sub });
const T = { // the shots in the plot-to-keys film (seconds)
  plot: 1, dig: 7.5, paper: 13.5, steel: 19.5, pour: 25.5, brick: 31.5, grey: 37.5, phone: 43.5, grey2: 49.5,
  plaster: 55.5, tap: 61.5, done: 67.5, keys: 73.5, done2: 79.5 };
const TAGS = '#MiyaarDevelopers #LahoreConstruction #HouseConstruction #GreyStructure #Turnkey #DHALahore #BahriaTownLahore #LakeCityLahore';

const reels = [
 { id: 1, title: 'Plot to keys', hook: 'Transformation (watch time)', scenes: [
   { type: 'clip', dur: 1.8, clip: C(T.plot), text: { at: 'top', h: ['Empty plot.'] } },
   { type: 'clip', dur: 1.5, clip: C(T.steel), text: { at: 'top', h: ['Grade-60 steel.'] } },
   { type: 'clip', dur: 1.5, clip: C(T.pour), text: { at: 'top', h: ['Every pour checked.'] } },
   { type: 'clip', dur: 1.5, clip: C(T.brick), text: { at: 'top', h: ['Brick by brick.'] } },
   { type: 'clip', dur: 1.8, clip: C(T.grey), text: { at: 'top', h: ['Grey structure:', '==4 to 5 months.=='] } },
   { type: 'clip', dur: 1.5, clip: C(T.plaster), text: { at: 'top', h: ['Then the finishing.'] } },
   { type: 'clip', dur: 2.2, clip: C(T.keys), text: { at: 'top', h: ['Keys in', '==8 to 10 months.=='] } },
   CTA('Your plot. ==Our build.==', 'Free estimate · miyaardevelopers.com') ],
   vo: 'Every house starts as an empty plot. Grade-60 steel. Every pour checked. Brick by brick. Grey structure in four to five months. Keys in eight to ten.',
   caption: 'From empty plot to keys in your hand. Grey structure in 4 to 5 months, turnkey in 8 to 10, with the handover date written into the contract.\n\nMessage us your plot size for a free estimate.' },

 { id: 2, title: 'The lowest quote', hook: 'Controversial (comments)', scenes: [
   { type: 'photo', dur: 2.6, img: 'aabpara-1.jpg', kb: 'in', text: { at: 'bottom', h: ['The lowest quote is', 'the ==most expensive== one.'], size: 'md' } },
   { type: 'card', dur: 5, img: 'awt-1.jpg', card: { kind: 'list', x: 1, title: 'How cheap builds go wrong', items: ['A lump sum with no breakdown', 'Steel and cement chosen later', '“Extras” after the slab is poured', 'The finish date keeps moving'] } },
   { type: 'card', dur: 3.4, img: 'bahria-1.jpg', card: { kind: 'list', title: 'At Miyaar', items: ['An itemised BOQ before signing', 'It becomes your ==fixed-price== contract'] } },
   CTA('Get a quote you can ==check==.', 'Every material named and priced') ],
   vo: 'The lowest quote is the most expensive one. No breakdown, materials picked later, extras after the slab. With us, your itemised BOQ becomes a fixed-price contract.',
   caption: 'A low lump-sum quote with no breakdown is how “extras” appear after the slab is poured. Ask for an itemised BOQ, and make it the contract.\n\nHave you been hit with extras? Tell us below.' },

 { id: 3, title: 'What PKR 3,200 buys', hook: 'Value (saves)', scenes: [
   { type: 'clip', dur: 2.4, clip: C(T.steel), text: { at: 'top', k: 'Grey structure from PKR 3,200 per sq ft', h: ['What does it', '==actually buy?=='] } },
   { type: 'card', dur: 6.8, clip: C(T.brick), card: { kind: 'list', title: 'Named in your BOQ', step: .7, items: ['Grade-60 steel (Mughal, Amreli)', 'Fauji, Bestway or Maple Leaf cement', 'A-grade awwal bricks', '1:2:4 concrete, vibrated', 'Chenab sand, Margalla crush'] } },
   CTA('Save this before you ==hire a builder==.', 'Get your itemised BOQ free') ],
   vo: 'Grey structure from three thousand two hundred rupees a square foot. Here is what that buys: Grade-60 steel, named cement, A-grade bricks, and one-two-four concrete. All written in your BOQ.',
   caption: 'Save this before you hire a contractor. Our grey structure starts from PKR 3,200 per sq ft, and every brand and grade is written into the BOQ:\nGrade-60 steel (Mughal, Amreli), Fauji, Bestway or Maple Leaf cement, A-grade awwal bricks, 1:2:4 concrete, Chenab sand, Margalla crush.' },

 { id: 4, title: 'Building from abroad', hook: 'Story (overseas)', scenes: [
   { type: 'clip', dur: 2.6, clip: C(T.phone), text: { at: 'top', k: 'Overseas Pakistanis', h: ['Your plot is in Lahore.', '==You are not.=='] } },
   { type: 'clip', dur: 2.4, clip: C(T.grey2), text: { at: 'top', h: ['Weekly site video', 'on ==WhatsApp==, unasked.'], size: 'md' } },
   { type: 'card', dur: 4.6, img: 'lakecity-1.jpg', card: { kind: 'list', title: 'Clients in Dubai, London, Toronto, Doha and New York get', items: ['A locked BOQ: no substitutions', 'A 3D model to share with family', 'DHA, LDA, BTAP and Lake City approvals handled'] } },
   CTA('Build from ==anywhere==.', 'Overseas details · miyaardevelopers.com') ],
   vo: 'Your plot is in Lahore. You are not. You get weekly site video on WhatsApp, a locked BOQ, and approvals handled here. Clients in Dubai, London and Toronto build this way.',
   caption: 'Most of the houses we build belong to overseas Pakistanis. Weekly walkthrough video goes to your WhatsApp without asking, your BOQ locks every brand and grade, and we handle DHA, LDA, BTAP and Lake City approvals locally.\n\nTag someone abroad who owns a plot.' },

 { id: 5, title: 'Pick your elevation', hook: 'Question (comments)', scenes: [
   { type: 'photo', dur: 2.2, img: 'uet-residence.jpg', kb: 'in', text: { at: 'top', h: ['Which one would', 'you build?'] } },
   { type: 'photo', dur: 2.4, num: '1', img: 'brochure-1kanal-dha7.jpg', kb: 'right', text: { at: 'bottom', h: 'Modern contemporary', size: 'sm' } },
   { type: 'photo', dur: 2.4, num: '2', img: 'brochure-10marla-johar.jpg', kb: 'left', text: { at: 'bottom', h: 'Spanish classic', size: 'sm' } },
   { type: 'photo', dur: 2.4, num: '3', img: 'uet-residence.jpg', kb: 'in', pos: '50% 60%', text: { at: 'bottom', h: 'Modern charcoal', size: 'sm' } },
   CTA('Comment ==1, 2 or 3==.', '10 architectural styles, 5 marla to 2 kanal') ],
   vo: 'Which one would you build? Number one, modern contemporary. Number two, Spanish classic. Number three, modern charcoal. Comment one, two or three.',
   caption: 'Which elevation would you build: 1, 2 or 3? Comment below.\n\nWe build 5 marla to 2 kanal homes in 10 architectural styles, grey structure or turnkey.' },

 { id: 6, title: '5 marla can look like this', hook: 'Curiosity', scenes: [
   { type: 'photo', dur: 2.6, img: 'brochure-5marla-khayaban.jpg', kb: 'in', text: { at: 'top', h: ['Think 5 marla', 'is ==too small==?'] } },
   { type: 'photo', dur: 2.2, img: 'brochure-5marla-azadi.jpg', kb: 'right', text: { at: 'bottom', h: '5 marla design', size: 'sm' } },
   { type: 'photo', dur: 2.2, img: 'brochure-5marla-pakarab.jpg', kb: 'left', text: { at: 'bottom', h: '5 marla design', size: 'sm' } },
   { type: 'card', dur: 3.2, img: 'brochure-5marla-khayaban.jpg', card: { kind: 'price', title: 'Build your 5 marla', rows: [['Grey structure', 'from PKR 3,200/sq ft'], ['Turnkey', 'from PKR 7,500/sq ft']] } },
   CTA('Send us your ==plot size==.', 'Free estimate in writing') ],
   vo: 'Think five marla is too small? Look again. Grey structure from three thousand two hundred a square foot. Turnkey from seven thousand five hundred. Send us your plot size.',
   caption: 'A 5 marla plot can carry a house like this. Grey structure from PKR 3,200 per sq ft, turnkey from PKR 7,500.\n\nSend us your plot size and society for a free written estimate.' },

 { id: 7, title: '10 marla, Bahria Town', hook: 'Aspiration', scenes: [
   { type: 'photo', dur: 2.6, img: 'brochure-10marla-bahria-night.jpg', kb: 'in', text: { at: 'top', k: 'Bahria Town', h: ['Your 10 marla,', '==after dark.=='] } },
   { type: 'photo', dur: 2.4, img: 'brochure-10marla-bahria.jpg', kb: 'right', text: { at: 'bottom', h: '10 marla design', size: 'sm' } },
   { type: 'photo', dur: 2.4, img: 'bahria-1.jpg', kb: 'left', text: { at: 'bottom', h: 'Executive villa, Bahria Town', sub: 'Turnkey, handed over 2024', size: 'sm' } },
   CTA('Turnkey from ==PKR 7,500/sq ft==.', 'Imported tiles, solid ash wood doors, named fittings') ],
   vo: 'Your ten marla in Bahria Town, after dark. Designed, built and handed over turnkey. Imported tiles, solid ash wood doors, named fittings. Turnkey from seven thousand five hundred a square foot.',
   caption: '10 marla in Bahria Town, turnkey. Imported porcelain tiles and marble, solid ash wood doors, Grohe or Porta fittings, all named in the BOQ. Turnkey from PKR 7,500 per sq ft.' },

 { id: 8, title: '1 kanal, DHA', hook: 'Aspiration', scenes: [
   { type: 'photo', dur: 2.6, img: 'brochure-1kanal-dha8.jpg', kb: 'in', text: { at: 'top', k: 'DHA Lahore', h: ['Building a ==1 kanal==?'] } },
   { type: 'photo', dur: 2.4, img: 'brochure-1kanal-dha7.jpg', kb: 'right', text: { at: 'bottom', h: '1 kanal design, DHA Phase 7', size: 'sm' } },
   { type: 'card', dur: 4, img: 'hero-dha-residence.jpg', card: { kind: 'list', title: 'The part you cannot fix later', items: ['Grade-60 steel', 'Named cement', 'Our engineer on site'] } },
   CTA('Structure that ==outlasts== the finishing.', 'DHA approvals handled · free estimate') ],
   vo: 'Building a one kanal in DHA? Columns, beams and slabs are the part you cannot fix later. We build them with Grade-60 steel and named cement, supervised by our engineer.',
   caption: 'Columns, beams and slabs are the one part of a house you cannot fix later. We build them with Grade-60 steel and named cement, supervised by our engineer. DHA approvals handled locally.' },

 { id: 9, title: 'Grey structure vs turnkey', hook: 'Contrast (decision)', scenes: [
   { type: 'clip', dur: 2.4, clip: C(T.grey), text: { at: 'top', h: ['Grey structure', 'or ==turnkey==?'] } },
   { type: 'card', dur: 6, clip: C(T.done), card: { kind: 'compare', title: 'Which one do you need?', cols: [
     { title: 'Grey structure', price: 'PKR 3,200', lines: ['per sq ft, from', '4 to 5 months', 'Frame, walls, slabs'] },
     { title: 'Turnkey', price: 'PKR 7,500', hi: 1, lines: ['per sq ft, from', '8 to 10 months', 'Move-in ready'] } ] } },
   { ...CTA('Not sure? ==Ask us.==', 'We will price both for your plot'), dur: 3.8 } ],
   vo: 'Grey structure or turnkey? Grey structure from three thousand two hundred, done in four to five months. Turnkey from seven thousand five hundred, move-in ready in eight to ten.',
   caption: 'Grey structure (from PKR 3,200/sq ft, 4 to 5 months) gives you the frame, walls and slabs. Turnkey (from PKR 7,500/sq ft, 8 to 10 months) hands you a finished house.\n\nNot sure which you need? We will price both for your plot.' },

 { id: 10, title: 'The bill matches the quote', hook: 'Bold claim', scenes: [
   { type: 'clip', dur: 2.6, clip: C(T.keys), text: { at: 'top', h: ['The final bill', '==matches the quote.=='] } },
   { type: 'clip', dur: 2.6, clip: C(T.paper), text: { at: 'top', h: ['Your BOQ becomes', 'the contract.'], size: 'md' } },
   { type: 'clip', dur: 2.6, clip: C(T.done2), text: { at: 'top', h: ['Handover on the', '==date in writing.=='], size: 'md' } },
   CTA('No extras. ==No surprises.==', 'Fixed-price contract · miyaardevelopers.com') ],
   vo: 'The final bill matches the quote. Your BOQ becomes the contract. The number you sign is the number you pay, and the handover date is written down.',
   caption: 'The number you sign is the number you pay at handover. Your BOQ becomes the contract, and the schedule is part of the agreement, not a hope.' },

 { id: 11, title: 'Handed over in 2024', hook: 'Proof', scenes: [
   { type: 'photo', dur: 2.2, img: 'aabpara-1.jpg', kb: 'in', text: { at: 'top', h: ['Handed over ==in 2024.=='] } },
   { type: 'photo', dur: 2.2, img: 'aabpara-1.jpg', kb: 'right', text: { at: 'bottom', h: 'Modern luxury residence', sub: 'T & T Aabpara Society, turnkey', size: 'sm' } },
   { type: 'photo', dur: 2.2, img: 'awt-1.jpg', kb: 'left', text: { at: 'bottom', h: 'Contemporary designer residence', sub: 'AWT Housing Scheme, turnkey', size: 'sm' } },
   { type: 'photo', dur: 2.2, img: 'bahria-1.jpg', kb: 'in', text: { at: 'bottom', h: 'Executive modern villa', sub: 'Bahria Town, turnkey', size: 'sm' } },
   { type: 'photo', dur: 2.2, img: 'farmhouse-1.jpg', kb: 'right', text: { at: 'bottom', h: 'Luxury farmhouse estate', sub: 'Turnkey', size: 'sm' } },
   CTA('Yours could be ==next==.', '130 projects delivered') ],
   vo: 'Handed over in twenty twenty-four. A modern luxury residence. A contemporary designer home. An executive villa in Bahria Town. A luxury farmhouse. Yours could be next.',
   caption: 'Four turnkey homes we handed over in 2024: a modern luxury residence in T & T Aabpara Society, a contemporary designer residence in AWT Housing Scheme, an executive modern villa in Bahria Town and a luxury farmhouse estate.\n\nAsk us for a client reference.' },

 { id: 12, title: 'Check what is in your walls', hook: 'Trust', scenes: [
   { type: 'clip', dur: 2.6, clip: C(T.brick), text: { at: 'top', h: ['Turn up any day.', '==Check your walls.=='] } },
   { type: 'clip', dur: 2.6, clip: C(T.pour), text: { at: 'top', h: ['Brands and grades', 'written down.'], size: 'md' } },
   { type: 'clip', dur: 2.6, clip: C(T.steel), text: { at: 'top', h: ['Checked against the', 'list ==before every pour==.'], size: 'md' } },
   CTA('Build with ==nothing hidden==.', 'Itemised BOQ · weekly site video') ],
   vo: 'Turn up any day and check what went into your walls. Brands and grades are written down, and everything is checked against the list before every pour.',
   caption: 'Every brand and grade is written down. Turn up any day and verify what went into your walls.' },

 { id: 13, title: 'Lahore build rates 2026', hook: 'Value (saves)', scenes: [
   { type: 'photo', dur: 2.4, img: 'front_house_01.jpg', kb: 'in', text: { at: 'top', h: ['What does it cost', 'to ==build in 2026==?'] } },
   { type: 'card', dur: 7.2, img: 'front_house_18.jpg', card: { kind: 'price', title: 'Miyaar rates, per sq ft', rows: [['Grey structure', 'from 3,200'], ['Grey + basement', '4,500–5,500'], ['Turnkey', 'from 7,500'], ['Finishing only', 'from 3,500'], ['Furnishing', 'from 1,000']], note: 'PKR. Reviewed against steel and cement prices, then locked in your contract.' } },
   CTA('Save this. ==Share it== with family.', 'Get your exact figure free') ],
   vo: 'What does it cost to build in twenty twenty-six? Grey structure from three thousand two hundred a square foot. Turnkey from seven thousand five hundred. Your rate is locked in the contract.',
   caption: 'Our 2026 rates per sq ft (PKR): grey structure from 3,200, grey structure with basement 4,500 to 5,500, turnkey from 7,500, finishing from 3,500, furnishing from 1,000. Rates are reviewed against steel and cement prices and locked in your contract.\n\nSave this and send it to whoever is planning the house.' },

 { id: 14, title: 'Built to the BOQ you signed', hook: 'Brand film', scenes: [
   { type: 'photo', dur: 2.6, img: 'front_house_01.jpg', kb: 'in', text: { at: 'bottom', h: ['Your house,', 'built to the ==BOQ you signed.=='] } },
   { type: 'photo', dur: 2.4, img: 'front_house_18.jpg', kb: 'up', text: { at: 'bottom', h: 'Since 2011', size: 'sm', sub: '130 projects delivered' } },
   { type: 'photo', dur: 2.4, img: 'lakecity-1.jpg', kb: 'right', text: { at: 'bottom', h: 'DHA · Bahria Town · Lake City', size: 'sm', sub: 'Bahria Orchard and Fazaia Housing too' } },
   CTA('Booking ==2026 build slots==.', 'Free estimate · miyaardevelopers.com') ],
   vo: 'Your house, built to the BOQ you signed. Building in Lahore since twenty eleven, across DHA, Bahria Town and Lake City. We are booking twenty twenty-six build slots now.',
   caption: 'Your house, built to the BOQ you signed. Building since 2011 across DHA Lahore, Bahria Town, Bahria Orchard, Lake City and Fazaia Housing. Now booking 2026 build slots.' },

 { id: 15, title: '4 questions before you hire', hook: 'Value (saves + shares)', scenes: [
   { type: 'photo', dur: 2.4, img: 'awt-1.jpg', kb: 'in', text: { at: 'top', h: ['4 questions to ask', 'before you ==hire a builder==.'], size: 'md' } },
   { type: 'card', dur: 6.8, clip: C(T.dig), card: { kind: 'list', num: 1, step: .9, title: 'Ask every contractor', items: ['Will I get an itemised BOQ?', 'Are brands and grades in the contract?', 'Is the handover date in writing?', 'Will I get weekly site video?'] } },
   CTA('Our answer: ==yes to all four.==', 'Free estimate · miyaardevelopers.com') ],
   vo: 'Four questions before you hire a builder. Will I get an itemised BOQ? Are brands in the contract? Is the handover date written? Will I get weekly site video? Ours is yes to all four.',
   caption: 'Ask every contractor these 4 questions:\n1. Will I get an itemised BOQ?\n2. Are brands and grades written into the contract?\n3. Is the handover date in writing?\n4. Will I get weekly site video?\n\nSave this, and send it to someone planning a house.' },
 { id: 16, title: 'Watch this plot become a house (AI)', hook: 'Transformation (awe, shares)', scenes: [
   { type: 'clip', dur: 2.6, clip: { src: 'canva-transformation-aabpara.mp4', from: 0 }, text: { at: 'top', h: ['Watch this plot', 'become ==a house==.'], tag: 'AI visualisation of our build' } },
   { type: 'clip', dur: 3, clip: { src: 'canva-transformation-aabpara.mp4', from: 2.6 }, text: { at: 'top', h: ['Frame and brick.'] } },
   { type: 'clip', dur: 3, clip: { src: 'canva-transformation-aabpara.mp4', from: 5.6 }, text: { at: 'top', h: ['Then the finishing.'] } },
   { type: 'clip', dur: 3.5, clip: { src: 'canva-transformation-aabpara.mp4', from: 8.6 }, text: { at: 'top', h: ['Turnkey,', 'handed over ==2024==.'] } },
   CTA('Your plot could be ==next==.', 'Free estimate · miyaardevelopers.com') ],
   vo: 'Watch this empty plot become a house. Frame and brick, then the finishing. A turnkey home we handed over in twenty twenty-four. Your plot could be next.',
   caption: 'From empty plot to finished home: an AI visualisation of how we built this modern luxury residence in T & T Aabpara Society, turnkey, handed over in 2024.\n\nMessage us your plot size for a free estimate.' },
];

const posts = [
 { id: 1, type: 'photo', fit: 'cover', img: 'front_house_01.jpg', text: { at: 'bottom', h: ['Your house, built to', 'the ==BOQ you signed.=='], sub: 'Grey structure and turnkey construction in Lahore.' }, caption: 'Your house, built to the BOQ you signed. Free estimate: WhatsApp +92 300 4008598.' },
 { id: 2, type: 'card', img: 'front_house_18.jpg', card: { kind: 'price', title: 'Build rates 2026, per sq ft', rows: [['Grey structure', 'from 3,200'], ['Grey + basement', '4,500–5,500'], ['Turnkey', 'from 7,500'], ['Finishing', 'from 3,500'], ['Furnishing', 'from 1,000']], note: 'PKR, locked in your contract.' }, caption: 'Our 2026 rates per sq ft. Save this for when you plan your build.' },
 { id: 3, type: 'card', img: 'awt-1.jpg', card: { kind: 'list', x: 1, title: 'The lowest quote is the most expensive one', items: ['No breakdown', 'Materials chosen later', 'Extras after the slab', 'The date keeps moving'] }, caption: 'Why cheap quotes cost more, and how an itemised BOQ fixes it.' },
 { id: 4, type: 'card', img: 'bahria-1.jpg', card: { kind: 'list', title: 'Named in your BOQ', items: ['Grade-60 steel (Mughal, Amreli)', 'Fauji, Bestway, Maple Leaf cement', 'A-grade awwal bricks', '1:2:4 concrete, vibrated', 'Chenab sand, Margalla crush'] }, caption: 'What our grey structure is made of, in writing.' },
 { id: 5, type: 'card', img: 'hero-dha-residence.jpg', card: { kind: 'compare', title: 'Grey structure or turnkey?', cols: [{ title: 'Grey structure', price: 'PKR 3,200', lines: ['per sq ft, from', '4 to 5 months'] }, { title: 'Turnkey', price: 'PKR 7,500', hi: 1, lines: ['per sq ft, from', '8 to 10 months'] }] }, caption: 'Grey structure or turnkey? We will price both for your plot.' },
 { id: 6, type: 'photo', img: 'brochure-10marla-bahria-night.jpg', text: { at: 'bottom', k: 'Bahria Town', h: ['Your 10 marla,', '==after dark.=='], sub: 'Turnkey from PKR 7,500 per sq ft.' }, caption: '10 marla in Bahria Town, turnkey.' },
 { id: 7, type: 'photo', img: 'brochure-1kanal-dha8.jpg', text: { at: 'bottom', k: 'DHA Lahore', h: ['Building a ==1 kanal==?'], sub: 'Grade-60 steel, named cement, our engineer on site.' }, caption: 'The structure is the part you cannot fix later.' },
 { id: 8, type: 'photo', img: 'brochure-5marla-khayaban.jpg', text: { at: 'bottom', h: ['Think 5 marla is', '==too small==?'], sub: 'Send us your plot size for a free estimate.' }, caption: '5 marla can look like this.' },
 { id: 9, type: 'photo', img: 'lakecity-1.jpg', text: { at: 'bottom', k: 'Overseas Pakistanis', h: ['Your plot is in Lahore.', '==You are not.=='], sub: 'Weekly site video on WhatsApp, approvals handled here.' }, caption: 'Build from Dubai, London or Toronto.' },
 { id: 10, type: 'photo', img: 'aabpara-1.jpg', text: { at: 'bottom', k: 'Handed over 2024', h: 'Modern luxury residence', sub: 'T & T Aabpara Society, turnkey.' }, caption: 'Turnkey, handed over in 2024.' },
 { id: 11, type: 'photo', img: 'farmhouse-1.jpg', text: { at: 'bottom', k: 'Handed over 2024', h: 'Luxury farmhouse estate', sub: 'Turnkey construction.' }, caption: 'Turnkey farmhouse, handed over in 2024.' },
 { id: 12, type: 'card', img: 'uet-residence.jpg', card: { kind: 'list', num: 1, title: '4 questions before you hire a builder', items: ['Itemised BOQ?', 'Brands in the contract?', 'Handover date in writing?', 'Weekly site video?'] }, caption: 'Ask every contractor these four questions.' },
 { id: 13, type: 'photo', img: 'uet-residence.jpg', text: { at: 'bottom', h: ['The final bill', '==matches the quote.=='], sub: 'Fixed-price contract. Handover date in writing.' }, caption: 'The number you sign is the number you pay.' },
 { id: 14, type: 'photo', img: 'brochure-10marla-johar.jpg', text: { at: 'bottom', h: ['10 styles.', '==5 marla to 2 kanal.=='], sub: 'Which style would you build? Comment below.' }, caption: 'Which style would you build?' },
 { id: 15, type: 'cta', img: 'hero-dha-residence.jpg', h: 'Booking ==2026 build slots==', sub: 'Free estimate · miyaardevelopers.com', caption: 'Now booking 2026 build slots. WhatsApp +92 300 4008598.' },
];
for (const p of posts) p.tags = TAGS;
for (const r of reels) r.tags = TAGS;
module.exports = { reels, posts };
