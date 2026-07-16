# System Prompt

You are the senior scenario author for Project ATaS, a fictional, unclassified military staff-training simulation.

Write realistic professional email conversations while obeying these rules:
- The scenario is fictional and all domains ending in .example are synthetic.
- Preserve every supplied message ID, subject, sender, recipient, timestamp, classification, and attachment reference exactly.
- Generate only the body text for each supplied message.
- Maintain continuity across replies. Later messages may quote or briefly reference earlier messages, but avoid repeating full chains.
- Match each persona's voice and what that person knows at that point in time.
- Do not reveal instructor metadata, truth IDs, grading language, or that this is a simulation.
- No email may itself be classified. Mailbox labels may only be UNCLASSIFIED or CUI.
- A single presentation attachment may contain an erroneously embedded fictional slide marked SECRET//NOFORN. Do not invent operational details, real collection capabilities, real targeting data, or actionable classified content.
- The security thread should describe the marking and the need to report suspected spillage, not reproduce sensitive slide contents.
- Use plausible military and government-office tone without imitating any real person's private communications.
- Vary length naturally: terse replies, short coordination notes, and occasional detailed technical messages.
- Return strict JSON only, with this shape: {"emails": [{"id": "...", "body": "..."}]}.


# Thread Prompt

Author this thread using the following structured brief:

{
  "thread": {
    "thread_id": "CONG-004",
    "purpose": "Briefing deck revisions",
    "email_count": 9,
    "importance": "critical",
    "truth_ids": [
      "T-001",
      "T-002",
      "T-006",
      "T-009"
    ],
    "planned_attachments": [
      "ATaS_Congressional_Brief_v12.pptx",
      "ATaS_Congressional_Brief_v13.pptx"
    ]
  },
  "character_knowledge_states": {
    "LCDR James Maddox": {
      "2026-09-29": [
        "ATaS is expected to approach 1% error",
        "A Senate briefing is forthcoming"
      ],
      "2026-10-02": [
        "Briefing deck is being built from v17",
        "Believes validation is on track"
      ],
      "2026-10-03": [
        "Has not reviewed v18",
        "Shares general project context with Stix"
      ],
      "2026-10-04": [
        "Still believes 1% is defensible",
        "Sends v13 deck to Stix without noticing slide 14"
      ],
      "2026-10-05 0730": [
        "Inbox remains unprocessed",
        "Does not understand full validation concern",
        "Has not reported suspected disclosure"
      ]
    },
    "COL Jesse Abreu": {
      "2026-09-29": [
        "Believes ATaS is a major improvement"
      ],
      "2026-10-02": [
        "Believes 1% is mature enough for briefing"
      ],
      "2026-10-04": [
        "Uses outdated deck and talking points"
      ],
      "2026-10-05 0730": [
        "Unaware of v18 concerns",
        "Unaware of disclosure"
      ]
    },
    "Capt Alicia Scott": {
      "2026-10-01": [
        "Knows Senator Lane supports modernization but prioritizes oversight"
      ],
      "2026-10-03": [
        "Sends updated questions and priorities"
      ],
      "2026-10-04": [
        "Assumes deck will be revised before briefing"
      ]
    }
  },
  "messages_to_author": [
    {
      "id": "CONG-004-001",
      "thread_index": 1,
      "sent_at": "2026-09-29T09:24:00.021442-04:00",
      "from": {
        "name": "Capt Alicia Scott",
        "email": "alicia.scott@congressional-liaison.example"
      },
      "to": [
        {
          "name": "Senator Lane Staff",
          "email": "sasc.lane.staff@senate.example"
        }
      ],
      "cc": [
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        },
        {
          "name": "COL Jesse Abreu",
          "email": "jesse.abreu@jiaitf.example"
        }
      ],
      "subject": "ATaS brief v12",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-002",
      "thread_index": 2,
      "sent_at": "2026-09-30T09:51:00.487437-04:00",
      "from": {
        "name": "Senator Lane Staff",
        "email": "sasc.lane.staff@senate.example"
      },
      "to": [
        {
          "name": "Capt Alicia Scott",
          "email": "alicia.scott@congressional-liaison.example"
        }
      ],
      "cc": [],
      "subject": "RE: ATaS brief v12",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "CONG-004-001",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-003",
      "thread_index": 3,
      "sent_at": "2026-09-30T16:56:00.085425-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "Capt Alicia Scott",
          "email": "alicia.scott@congressional-liaison.example"
        }
      ],
      "cc": [],
      "subject": "Slide edits requested",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "CONG-004-002",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-004",
      "thread_index": 4,
      "sent_at": "2026-10-01T21:44:00.095415-04:00",
      "from": {
        "name": "COL Jesse Abreu",
        "email": "jesse.abreu@jiaitf.example"
      },
      "to": [
        {
          "name": "Capt Alicia Scott",
          "email": "alicia.scott@congressional-liaison.example"
        }
      ],
      "cc": [
        {
          "name": "Senator Lane Staff",
          "email": "sasc.lane.staff@senate.example"
        },
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "subject": "ATaS brief v13",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "CONG-004-003",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-005",
      "thread_index": 5,
      "sent_at": "2026-10-02T09:07:00.577171-04:00",
      "from": {
        "name": "Capt Alicia Scott",
        "email": "alicia.scott@congressional-liaison.example"
      },
      "to": [
        {
          "name": "Senator Lane Staff",
          "email": "sasc.lane.staff@senate.example"
        }
      ],
      "cc": [],
      "subject": "RE: ATaS brief v13",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [
        {
          "id": "ATT-CONG-004-005-01",
          "filename": "ATaS_Congressional_Brief_v12.pptx",
          "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
          "path": "attachments/ATaS_Congressional_Brief_v12.pptx"
        }
      ],
      "in_reply_to": "CONG-004-004",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-006",
      "thread_index": 6,
      "sent_at": "2026-10-02T13:31:00.317206-04:00",
      "from": {
        "name": "Senator Lane Staff",
        "email": "sasc.lane.staff@senate.example"
      },
      "to": [
        {
          "name": "Capt Alicia Scott",
          "email": "alicia.scott@congressional-liaison.example"
        }
      ],
      "cc": [],
      "subject": "Civilian safeguards slide missing",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "CONG-004-005",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-007",
      "thread_index": 7,
      "sent_at": "2026-10-03T14:03:00.009399-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "Capt Alicia Scott",
          "email": "alicia.scott@congressional-liaison.example"
        }
      ],
      "cc": [
        {
          "name": "Senator Lane Staff",
          "email": "sasc.lane.staff@senate.example"
        },
        {
          "name": "COL Jesse Abreu",
          "email": "jesse.abreu@jiaitf.example"
        }
      ],
      "subject": "Deck version check",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "CONG-004-006",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-008",
      "thread_index": 8,
      "sent_at": "2026-10-04T17:07:00.019106-04:00",
      "from": {
        "name": "COL Jesse Abreu",
        "email": "jesse.abreu@jiaitf.example"
      },
      "to": [
        {
          "name": "Capt Alicia Scott",
          "email": "alicia.scott@congressional-liaison.example"
        }
      ],
      "cc": [],
      "subject": "Final deck for Monday",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "CONG-004-007",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    },
    {
      "id": "CONG-004-009",
      "thread_index": 9,
      "sent_at": "2026-10-04T20:31:00.602938-04:00",
      "from": {
        "name": "Capt Alicia Scott",
        "email": "alicia.scott@congressional-liaison.example"
      },
      "to": [
        {
          "name": "Senator Lane Staff",
          "email": "sasc.lane.staff@senate.example"
        }
      ],
      "cc": [],
      "subject": "RE: Final deck for Monday",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [
        {
          "id": "ATT-CONG-004-009-01",
          "filename": "ATaS_Congressional_Brief_v12.pptx",
          "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
          "path": "attachments/ATaS_Congressional_Brief_v12.pptx"
        },
        {
          "id": "ATT-CONG-004-009-02",
          "filename": "ATaS_Congressional_Brief_v13.pptx",
          "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
          "path": "attachments/ATaS_Congressional_Brief_v13.pptx"
        }
      ],
      "in_reply_to": "CONG-004-008",
      "purpose": "Briefing deck revisions",
      "facts_to_support": [
        "T-001",
        "T-002",
        "T-006",
        "T-009"
      ]
    }
  ],
  "quality_requirements": [
    "The conversation must have a clear beginning, progression, and ending.",
    "Do not make every message equally long or polished.",
    "Technical concerns should emerge incrementally rather than through one smoking-gun email.",
    "Do not put instructor truth IDs into email bodies.",
    "Do not fabricate attachment contents beyond what the scenario requires."
  ]
}
