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
    "thread_id": "OPS-002",
    "purpose": "Leadership synchronization",
    "email_count": 8,
    "importance": "medium",
    "truth_ids": [
      "T-009",
      "T-016"
    ],
    "planned_attachments": []
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
      "id": "OPS-002-001",
      "thread_index": 1,
      "sent_at": "2026-09-29T07:03:00.767229-04:00",
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
      "subject": "Leadership sync notes",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-002",
      "thread_index": 2,
      "sent_at": "2026-09-30T15:07:00.737043-04:00",
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
      "subject": "RE: Leadership sync notes",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-001",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-003",
      "thread_index": 3,
      "sent_at": "2026-09-30T15:51:00.301461-04:00",
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
      "subject": "ATaS decision points",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-002",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-004",
      "thread_index": 4,
      "sent_at": "2026-10-02T08:56:00.571593-04:00",
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
      "subject": "Monday prep status",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-003",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-005",
      "thread_index": 5,
      "sent_at": "2026-10-02T22:18:00.315414-04:00",
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
      "subject": "Open leadership questions",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-004",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-006",
      "thread_index": 6,
      "sent_at": "2026-10-03T16:18:00.014142-04:00",
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
      "subject": "RE: Open leadership questions",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-005",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-007",
      "thread_index": 7,
      "sent_at": "2026-10-04T07:56:00.245462-04:00",
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
      "subject": "Sunday evening update",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-006",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
      ]
    },
    {
      "id": "OPS-002-008",
      "thread_index": 8,
      "sent_at": "2026-10-04T17:56:00.950298-04:00",
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
      "subject": "0730 status",
      "classification": "UNCLASSIFIED",
      "importance": "medium",
      "attachments": [],
      "in_reply_to": "OPS-002-007",
      "purpose": "Leadership synchronization",
      "facts_to_support": [
        "T-009",
        "T-016"
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
