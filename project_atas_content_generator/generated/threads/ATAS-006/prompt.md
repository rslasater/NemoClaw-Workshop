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
    "thread_id": "ATAS-006",
    "purpose": "Validation Report v17",
    "email_count": 3,
    "importance": "high",
    "truth_ids": [
      "T-009",
      "T-011"
    ],
    "planned_attachments": [
      "ATaS_Validation_Report_v17.pdf"
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
      "id": "ATAS-006-001",
      "thread_index": 1,
      "sent_at": "2026-09-30T13:56:00.285272-04:00",
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
      "subject": "Validation Report v17 posted",
      "classification": "UNCLASSIFIED",
      "importance": "high",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Validation Report v17",
      "facts_to_support": [
        "T-009",
        "T-011"
      ]
    },
    {
      "id": "ATAS-006-002",
      "thread_index": 2,
      "sent_at": "2026-10-02T09:12:00.467238-04:00",
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
      "subject": "RE: Validation Report v17 posted",
      "classification": "UNCLASSIFIED",
      "importance": "high",
      "attachments": [
        {
          "id": "ATT-ATAS-006-002-01",
          "filename": "ATaS_Validation_Report_v17.pdf",
          "mime_type": "application/pdf",
          "path": "attachments/ATaS_Validation_Report_v17.pdf"
        }
      ],
      "in_reply_to": "ATAS-006-001",
      "purpose": "Validation Report v17",
      "facts_to_support": [
        "T-009",
        "T-011"
      ]
    },
    {
      "id": "ATAS-006-003",
      "thread_index": 3,
      "sent_at": "2026-10-04T08:03:00.190918-04:00",
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
      "subject": "Use v17 for deck",
      "classification": "UNCLASSIFIED",
      "importance": "high",
      "attachments": [
        {
          "id": "ATT-ATAS-006-003-01",
          "filename": "ATaS_Validation_Report_v17.pdf",
          "mime_type": "application/pdf",
          "path": "attachments/ATaS_Validation_Report_v17.pdf"
        }
      ],
      "in_reply_to": "ATAS-006-002",
      "purpose": "Validation Report v17",
      "facts_to_support": [
        "T-009",
        "T-011"
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
