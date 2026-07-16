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
    "thread_id": "OPS-004",
    "purpose": "Meeting minutes",
    "email_count": 5,
    "importance": "low",
    "truth_ids": [
      "T-005"
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
      "id": "OPS-004-001",
      "thread_index": 1,
      "sent_at": "2026-09-29T10:12:00.049837-04:00",
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
      "subject": "ATaS working group minutes",
      "classification": "UNCLASSIFIED",
      "importance": "low",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Meeting minutes",
      "facts_to_support": [
        "T-005"
      ]
    },
    {
      "id": "OPS-004-002",
      "thread_index": 2,
      "sent_at": "2026-10-01T08:18:00.336748-04:00",
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
      "subject": "RE: ATaS working group minutes",
      "classification": "UNCLASSIFIED",
      "importance": "low",
      "attachments": [],
      "in_reply_to": "OPS-004-001",
      "purpose": "Meeting minutes",
      "facts_to_support": [
        "T-005"
      ]
    },
    {
      "id": "OPS-004-003",
      "thread_index": 3,
      "sent_at": "2026-10-02T08:44:00.396935-04:00",
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
      "subject": "Friday meeting minutes",
      "classification": "UNCLASSIFIED",
      "importance": "low",
      "attachments": [],
      "in_reply_to": "OPS-004-002",
      "purpose": "Meeting minutes",
      "facts_to_support": [
        "T-005"
      ]
    },
    {
      "id": "OPS-004-004",
      "thread_index": 4,
      "sent_at": "2026-10-03T20:24:00.652200-04:00",
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
      "subject": "Weekend coordination notes",
      "classification": "UNCLASSIFIED",
      "importance": "low",
      "attachments": [],
      "in_reply_to": "OPS-004-003",
      "purpose": "Meeting minutes",
      "facts_to_support": [
        "T-005"
      ]
    },
    {
      "id": "OPS-004-005",
      "thread_index": 5,
      "sent_at": "2026-10-04T21:51:00.050085-04:00",
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
      "subject": "Sunday closeout minutes",
      "classification": "UNCLASSIFIED",
      "importance": "low",
      "attachments": [],
      "in_reply_to": "OPS-004-004",
      "purpose": "Meeting minutes",
      "facts_to_support": [
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
