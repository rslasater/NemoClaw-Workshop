Author this thread using the following structured brief:

{
  "thread": {
    "thread_id": "SEC-004",
    "purpose": "Slide sanity check and disclosure",
    "email_count": 5,
    "importance": "critical",
    "truth_ids": [
      "T-006",
      "T-019"
    ],
    "planned_attachments": [
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
    "LCDR Jeff \"Stix\" Martinez": {
      "2026-10-03": [
        "Knows James supports an AI targeting project"
      ],
      "2026-10-04": [
        "Receives v13 deck",
        "Recognizes slide marked SECRET//NOFORN",
        "Warns James"
      ]
    }
  },
  "messages_to_author": [
    {
      "id": "SEC-004-001",
      "thread_index": 1,
      "sent_at": "2026-09-30T09:12:00.870067-04:00",
      "from": {
        "name": "LCDR Jeff \"Stix\" Martinez",
        "email": "jeff.martinez@navy.example"
      },
      "to": [
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "cc": [
        {
          "name": "JIAITF Security Office",
          "email": "security@jiaitf.example"
        }
      ],
      "subject": "Can you sanity check this deck?",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Slide sanity check and disclosure",
      "facts_to_support": [
        "T-006",
        "T-019"
      ]
    },
    {
      "id": "SEC-004-002",
      "thread_index": 2,
      "sent_at": "2026-10-01T21:12:00.469132-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "LCDR Jeff \"Stix\" Martinez",
          "email": "jeff.martinez@navy.example"
        }
      ],
      "cc": [],
      "subject": "RE: Can you sanity check this deck?",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "SEC-004-001",
      "purpose": "Slide sanity check and disclosure",
      "facts_to_support": [
        "T-006",
        "T-019"
      ]
    },
    {
      "id": "SEC-004-003",
      "thread_index": 3,
      "sent_at": "2026-10-02T07:12:00.347127-04:00",
      "from": {
        "name": "JIAITF Security Office",
        "email": "security@jiaitf.example"
      },
      "to": [
        {
          "name": "LCDR Jeff \"Stix\" Martinez",
          "email": "jeff.martinez@navy.example"
        }
      ],
      "cc": [],
      "subject": "Slide 14",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [
        {
          "id": "ATT-SEC-004-003-01",
          "filename": "ATaS_Congressional_Brief_v13.pptx",
          "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
          "path": "attachments/ATaS_Congressional_Brief_v13.pptx"
        }
      ],
      "in_reply_to": "SEC-004-002",
      "purpose": "Slide sanity check and disclosure",
      "facts_to_support": [
        "T-006",
        "T-019"
      ]
    },
    {
      "id": "SEC-004-004",
      "thread_index": 4,
      "sent_at": "2026-10-03T11:38:00.810563-04:00",
      "from": {
        "name": "LCDR Jeff \"Stix\" Martinez",
        "email": "jeff.martinez@navy.example"
      },
      "to": [
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "cc": [
        {
          "name": "JIAITF Security Office",
          "email": "security@jiaitf.example"
        }
      ],
      "subject": "RE: Slide 14",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "SEC-004-003",
      "purpose": "Slide sanity check and disclosure",
      "facts_to_support": [
        "T-006",
        "T-019"
      ]
    },
    {
      "id": "SEC-004-005",
      "thread_index": 5,
      "sent_at": "2026-10-05T07:25:00-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "LCDR Jeff \"Stix\" Martinez",
          "email": "jeff.martinez@navy.example"
        }
      ],
      "cc": [],
      "subject": "Delete that attachment",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [
        {
          "id": "ATT-SEC-004-005-01",
          "filename": "ATaS_Congressional_Brief_v13.pptx",
          "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
          "path": "attachments/ATaS_Congressional_Brief_v13.pptx"
        }
      ],
      "in_reply_to": "SEC-004-004",
      "purpose": "Slide sanity check and disclosure",
      "facts_to_support": [
        "T-006",
        "T-019"
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