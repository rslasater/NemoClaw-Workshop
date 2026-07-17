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
    "thread_id": "HOME-002",
    "purpose": "VA loan preapproval",
    "email_count": 6,
    "importance": "noise",
    "truth_ids": [
      "T-016",
      "T-018"
    ],
    "planned_attachments": [
      "VA_Loan_Preapproval.pdf"
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
    }
  },
  "messages_to_author": [
    {
      "id": "HOME-002-001",
      "thread_index": 1,
      "sent_at": "2026-09-30T10:03:00-04:00",
      "from": {
        "name": "Emily Maddox",
        "email": "emily.maddox@example.com"
      },
      "to": [
        {
          "name": "Megan Ortiz",
          "email": "megan@coastalkeyrealty.example"
        }
      ],
      "cc": [
        {
          "name": "Daniel Cho",
          "email": "daniel.cho@harborviewlending.example"
        },
        {
          "name": "LCDR James Maddox",
          "email": "james.maddox@jiaitf.example"
        }
      ],
      "subject": "VA loan preapproval",
      "classification": "UNCLASSIFIED",
      "importance": "noise",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "VA loan preapproval",
      "facts_to_support": [
        "T-016",
        "T-018"
      ]
    },
    {
      "id": "HOME-002-002",
      "thread_index": 2,
      "sent_at": "2026-09-30T13:56:00-04:00",
      "from": {
        "name": "Megan Ortiz",
        "email": "megan@coastalkeyrealty.example"
      },
      "to": [
        {
          "name": "Emily Maddox",
          "email": "emily.maddox@example.com"
        }
      ],
      "cc": [],
      "subject": "RE: VA loan preapproval",
      "classification": "UNCLASSIFIED",
      "importance": "noise",
      "attachments": [],
      "in_reply_to": "HOME-002-001",
      "purpose": "VA loan preapproval",
      "facts_to_support": [
        "T-016",
        "T-018"
      ]
    },
    {
      "id": "HOME-002-003",
      "thread_index": 3,
      "sent_at": "2026-10-01T16:51:00-04:00",
      "from": {
        "name": "Daniel Cho",
        "email": "daniel.cho@harborviewlending.example"
      },
      "to": [
        {
          "name": "Emily Maddox",
          "email": "emily.maddox@example.com"
        }
      ],
      "cc": [],
      "subject": "Documents needed",
      "classification": "UNCLASSIFIED",
      "importance": "noise",
      "attachments": [],
      "in_reply_to": "HOME-002-002",
      "purpose": "VA loan preapproval",
      "facts_to_support": [
        "T-016",
        "T-018"
      ]
    },
    {
      "id": "HOME-002-004",
      "thread_index": 4,
      "sent_at": "2026-10-02T21:51:00-04:00",
      "from": {
        "name": "LCDR James Maddox",
        "email": "james.maddox@jiaitf.example"
      },
      "to": [
        {
          "name": "Emily Maddox",
          "email": "emily.maddox@example.com"
        }
      ],
      "cc": [
        {
          "name": "Megan Ortiz",
          "email": "megan@coastalkeyrealty.example"
        },
        {
          "name": "Daniel Cho",
          "email": "daniel.cho@harborviewlending.example"
        }
      ],
      "subject": "Rate lock options",
      "classification": "UNCLASSIFIED",
      "importance": "noise",
      "attachments": [
        {
          "id": "ATT-HOME-002-004-01",
          "filename": "VA_Loan_Preapproval.pdf",
          "mime_type": "application/pdf",
          "path": "attachments/VA_Loan_Preapproval.pdf"
        }
      ],
      "in_reply_to": "HOME-002-003",
      "purpose": "VA loan preapproval",
      "facts_to_support": [
        "T-016",
        "T-018"
      ]
    },
    {
      "id": "HOME-002-005",
      "thread_index": 5,
      "sent_at": "2026-10-03T13:03:00-04:00",
      "from": {
        "name": "Emily Maddox",
        "email": "emily.maddox@example.com"
      },
      "to": [
        {
          "name": "Megan Ortiz",
          "email": "megan@coastalkeyrealty.example"
        }
      ],
      "cc": [],
      "subject": "Debt-to-income follow-up",
      "classification": "UNCLASSIFIED",
      "importance": "noise",
      "attachments": [],
      "in_reply_to": "HOME-002-004",
      "purpose": "VA loan preapproval",
      "facts_to_support": [
        "T-016",
        "T-018"
      ]
    },
    {
      "id": "HOME-002-006",
      "thread_index": 6,
      "sent_at": "2026-10-03T20:18:00-04:00",
      "from": {
        "name": "Megan Ortiz",
        "email": "megan@coastalkeyrealty.example"
      },
      "to": [
        {
          "name": "Emily Maddox",
          "email": "emily.maddox@example.com"
        }
      ],
      "cc": [],
      "subject": "Updated preapproval letter",
      "classification": "UNCLASSIFIED",
      "importance": "noise",
      "attachments": [
        {
          "id": "ATT-HOME-002-006-01",
          "filename": "VA_Loan_Preapproval.pdf",
          "mime_type": "application/pdf",
          "path": "attachments/VA_Loan_Preapproval.pdf"
        }
      ],
      "in_reply_to": "HOME-002-005",
      "purpose": "VA loan preapproval",
      "facts_to_support": [
        "T-016",
        "T-018"
      ]
    }
  ],
  "quality_requirements": [
    "The conversation must have a clear beginning, progression, and ending.",
    "Do not make every message equally long or polished.",
    "Technical concerns should emerge incrementally rather than through one smoking-gun email.",
    "Do not put instructor truth IDs into email bodies.",
    "Do not fabricate attachment contents beyond what the scenario requires.",
    "Do not include the string SECRET//NOFORN or any classified-document marking in this thread."
  ]
}
