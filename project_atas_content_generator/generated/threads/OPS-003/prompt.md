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
    "thread_id": "OPS-003",
    "purpose": "Action tracker",
    "email_count": 7,
    "importance": "medium",
    "truth_ids": [
      "T-002",
      "T-005"
    ],
    "planned_attachments": [
      "JIAITF_Action_Tracker.xlsx"
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
    }
  },
  "messages_to_author": [
    {
      "id": "OPS-003-001",
      "thread_index": 1,
      "sent_at": "2026-09-29T11:24:00.867035-04:00",
      "from": {
        "name": "JIAITF Operations",
        "email": "operations@jiaitf.example"
      },
      "to": [
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "cc": [
        {
          "name": "COL Jesse Abreu",
          "email": "jesse.abreu@jiaitf.example"
        }
      ],
      "subject": "ATaS action tracker",
      "classification": "CUI",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
      ]
    },
    {
      "id": "OPS-003-002",
      "thread_index": 2,
      "sent_at": "2026-09-30T20:31:00.384460-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "JIAITF Operations",
          "email": "operations@jiaitf.example"
        }
      ],
      "cc": [],
      "subject": "RE: ATaS action tracker",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-003-001",
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
      ]
    },
    {
      "id": "OPS-003-003",
      "thread_index": 3,
      "sent_at": "2026-10-01T13:12:00.741721-04:00",
      "from": {
        "name": "COL Jesse Abreu",
        "email": "jesse.abreu@jiaitf.example"
      },
      "to": [
        {
          "name": "JIAITF Operations",
          "email": "operations@jiaitf.example"
        }
      ],
      "cc": [],
      "subject": "Overdue actions",
      "classification": "CUI",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-003-002",
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
      ]
    },
    {
      "id": "OPS-003-004",
      "thread_index": 4,
      "sent_at": "2026-10-02T10:44:00.529217-04:00",
      "from": {
        "name": "JIAITF Operations",
        "email": "operations@jiaitf.example"
      },
      "to": [
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "cc": [
        {
          "name": "COL Jesse Abreu",
          "email": "jesse.abreu@jiaitf.example"
        }
      ],
      "subject": "Slide update action",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [
        {
          "id": "ATT-OPS-003-004-01",
          "filename": "JIAITF_Action_Tracker.xlsx",
          "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "path": "attachments/JIAITF_Action_Tracker.xlsx"
        }
      ],
      "in_reply_to": "OPS-003-003",
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
      ]
    },
    {
      "id": "OPS-003-005",
      "thread_index": 5,
      "sent_at": "2026-10-03T16:56:00.905459-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "JIAITF Operations",
          "email": "operations@jiaitf.example"
        }
      ],
      "cc": [],
      "subject": "Validation review action",
      "classification": "CUI",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-003-004",
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
      ]
    },
    {
      "id": "OPS-003-006",
      "thread_index": 6,
      "sent_at": "2026-10-03T21:07:00.772198-04:00",
      "from": {
        "name": "COL Jesse Abreu",
        "email": "jesse.abreu@jiaitf.example"
      },
      "to": [
        {
          "name": "JIAITF Operations",
          "email": "operations@jiaitf.example"
        }
      ],
      "cc": [],
      "subject": "Security review action",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-003-005",
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
      ]
    },
    {
      "id": "OPS-003-007",
      "thread_index": 7,
      "sent_at": "2026-10-05T07:25:00-04:00",
      "from": {
        "name": "JIAITF Operations",
        "email": "operations@jiaitf.example"
      },
      "to": [
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "cc": [
        {
          "name": "COL Jesse Abreu",
          "email": "jesse.abreu@jiaitf.example"
        }
      ],
      "subject": "Monday action status",
      "classification": "CUI",
      "importance": "medium",
      "attachments": [
        {
          "id": "ATT-OPS-003-007-01",
          "filename": "JIAITF_Action_Tracker.xlsx",
          "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "path": "attachments/JIAITF_Action_Tracker.xlsx"
        }
      ],
      "in_reply_to": "OPS-003-006",
      "purpose": "Action tracker",
      "facts_to_support": [
        "T-002",
        "T-005"
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
