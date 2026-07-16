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
    "thread_id": "SEC-005",
    "purpose": "Message recall attempt",
    "email_count": 3,
    "importance": "critical",
    "truth_ids": [
      "T-007",
      "T-008"
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
      "id": "SEC-005-001",
      "thread_index": 1,
      "sent_at": "2026-09-29T21:07:00.346047-04:00",
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
      "subject": "Recall: Can you sanity check this deck?",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": null,
      "purpose": "Message recall attempt",
      "facts_to_support": [
        "T-007",
        "T-008"
      ]
    },
    {
      "id": "SEC-005-002",
      "thread_index": 2,
      "sent_at": "2026-10-02T07:44:00.955492-04:00",
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
      "subject": "RE: Recall attempt",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "SEC-005-001",
      "purpose": "Message recall attempt",
      "facts_to_support": [
        "T-007",
        "T-008"
      ]
    },
    {
      "id": "SEC-005-003",
      "thread_index": 3,
      "sent_at": "2026-10-03T22:44:00.303020-04:00",
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
      "subject": "Message recall will not remove it",
      "classification": "UNCLASSIFIED",
      "importance": "critical",
      "attachments": [],
      "in_reply_to": "SEC-005-002",
      "purpose": "Message recall attempt",
      "facts_to_support": [
        "T-007",
        "T-008"
      ]
    }
  ],
  "quality_requirements": [
    "The conversation must have a clear beginning, progression, and ending.",
    "Do not make every message equally long or polished.",
    "Technical concerns should emerge incrementally rather than through one smoking-gun email.",
    "Do not put instructor truth IDs into email bodies.",
    "Do not fabricate attachment contents beyond what the scenario requires.",
    "This is an approved security-spillage thread; references to the embedded slide marking may appear only as needed."
  ]
}
