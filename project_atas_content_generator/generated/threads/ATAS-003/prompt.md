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
    "thread_id": "ATAS-003",
    "purpose": "Validation testing",
    "email_count": 10,
    "importance": "critical",
    "truth_ids": [
      "T-003",
      "T-005",
      "T-011",
      "T-012",
      "T-013",
      "T-014",
      "T-015"
    ],
    "planned_attachments": [
      "Urban_Test_Results.xlsx"
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
    "Dr. Josh Brunner": {
      "2026-09-29": [
        "Optimistic about model improvement"
      ],
      "2026-10-02": [
        "Recognizes urban performance remains weaker"
      ],
      "2026-10-03": [
        "Sees aggregate performance trending near 2%"
      ],
      "2026-10-04": [
        "Not comfortable representing 1% as final",
        "Wants more validation"
      ],
      "2026-10-05 0730": [
        "Prepared to answer honestly if asked"
      ]
    },
    "Rebecca Shaw": {
      "2026-09-29": [
        "Supports 1% projected-performance narrative"
      ],
      "2026-10-02": [
        "Knows validation is incomplete"
      ],
      "2026-10-03": [
        "Keeps external messaging aligned to 1%"
      ],
      "2026-10-04": [
        "Continues emphasizing projected performance and future validation"
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
      "id": "ATAS-003-001",
      "thread_index": 1,
      "sent_at": "2026-09-29T08:31:00.162146-04:00",
      "from": {
        "name": "Dr. Josh Brunner",
        "email": "josh.brunner@aegis-technologies.example"
      },
      "to": [
        {
          "name": "Rebecca Shaw",
          "email": "rebecca.shaw@aegis-technologies.example"
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
      "subject": "Validation test plan",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-002",
      "thread_index": 2,
      "sent_at": "2026-09-30T16:24:00.683120-04:00",
      "from": {
        "name": "Rebecca Shaw",
        "email": "rebecca.shaw@aegis-technologies.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
        }
      ],
      "cc": [],
      "subject": "RE: Validation test plan",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-001",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-003",
      "thread_index": 3,
      "sent_at": "2026-09-30T20:44:00.315838-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
        }
      ],
      "cc": [],
      "subject": "Initial validation results",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-002",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-004",
      "thread_index": 4,
      "sent_at": "2026-10-01T13:07:00.977418-04:00",
      "from": {
        "name": "COL Jesse Abreu",
        "email": "jesse.abreu@jiaitf.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
        }
      ],
      "cc": [
        {
          "name": "Rebecca Shaw",
          "email": "rebecca.shaw@aegis-technologies.example"
        },
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "subject": "Weather cohort results",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-003",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-005",
      "thread_index": 5,
      "sent_at": "2026-10-02T11:56:00.255061-04:00",
      "from": {
        "name": "Dr. Josh Brunner",
        "email": "josh.brunner@aegis-technologies.example"
      },
      "to": [
        {
          "name": "Rebecca Shaw",
          "email": "rebecca.shaw@aegis-technologies.example"
        }
      ],
      "cc": [],
      "subject": "Urban cohort results",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-004",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-006",
      "thread_index": 6,
      "sent_at": "2026-10-02T22:56:00.225106-04:00",
      "from": {
        "name": "Rebecca Shaw",
        "email": "rebecca.shaw@aegis-technologies.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
        }
      ],
      "cc": [],
      "subject": "RE: Urban cohort results",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [
        {
          "id": "ATT-ATAS-003-006-01",
          "filename": "Urban_Test_Results.xlsx",
          "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "path": "attachments/Urban_Test_Results.xlsx"
        }
      ],
      "in_reply_to": "ATAS-003-005",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-007",
      "thread_index": 7,
      "sent_at": "2026-10-03T08:03:00.471861-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
        }
      ],
      "cc": [
        {
          "name": "Rebecca Shaw",
          "email": "rebecca.shaw@aegis-technologies.example"
        },
        {
          "name": "COL Jesse Abreu",
          "email": "jesse.abreu@jiaitf.example"
        }
      ],
      "subject": "Civilian proximity cases",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-006",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-008",
      "thread_index": 8,
      "sent_at": "2026-10-03T21:24:00.052535-04:00",
      "from": {
        "name": "COL Jesse Abreu",
        "email": "jesse.abreu@jiaitf.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
        }
      ],
      "cc": [],
      "subject": "Validation sample size",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-007",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-009",
      "thread_index": 9,
      "sent_at": "2026-10-04T22:18:00.326985-04:00",
      "from": {
        "name": "Dr. Josh Brunner",
        "email": "josh.brunner@aegis-technologies.example"
      },
      "to": [
        {
          "name": "Rebecca Shaw",
          "email": "rebecca.shaw@aegis-technologies.example"
        }
      ],
      "cc": [],
      "subject": "Weekend validation update",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "ATAS-003-008",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
      ]
    },
    {
      "id": "ATAS-003-010",
      "thread_index": 10,
      "sent_at": "2026-10-05T07:25:00-04:00",
      "from": {
        "name": "Rebecca Shaw",
        "email": "rebecca.shaw@aegis-technologies.example"
      },
      "to": [
        {
          "name": "Dr. Josh Brunner",
          "email": "josh.brunner@aegis-technologies.example"
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
      "subject": "RE: Weekend validation update",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [
        {
          "id": "ATT-ATAS-003-010-01",
          "filename": "Urban_Test_Results.xlsx",
          "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          "path": "attachments/Urban_Test_Results.xlsx"
        }
      ],
      "in_reply_to": "ATAS-003-009",
      "purpose": "Validation testing",
      "facts_to_support": [
        "T-003",
        "T-005",
        "T-011",
        "T-012",
        "T-013",
        "T-014",
        "T-015"
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
