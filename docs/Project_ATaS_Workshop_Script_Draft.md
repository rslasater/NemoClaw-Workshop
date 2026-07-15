# Project ATaS Workshop Script Draft

Status: Draft for planning
Duration: 2 hours
Audience: Technical students learning agentic AI workflows with NVIDIA NemoClaw
Scenario date: Monday, October 5, 2026, 0730 Eastern

## Workshop Purpose

Project ATaS is a story-driven agentic AI workshop where students build an executive assistant for LCDR James Maddox, Executive Officer of the Joint Interagency Artificial Intelligence Task Force.

Students must prepare COL Jesse Abreu for a 0900 Senate Armed Services Committee briefing after a week of accumulated email. The exercise is not an email summarization lab. It is a planning, prioritization, evidence synthesis, attachment analysis, and safe tool-use lab.

By the end of the workshop, students should understand how an agent can:

- Interact with a constrained tool API.
- Search and triage a noisy mailbox.
- Inspect attachments as evidence.
- Track uncertainty and source claims.
- Draft an executive-ready briefing.
- Avoid unsafe autonomous actions.
- Surface policy, security, and validation risks.

## Instructor Setup

Before students arrive:

- Start the fake email API and webmail UI.
- Confirm the mailbox is seeded with generated Project ATaS emails.
- Confirm Inbox and Sent folders reflect James Maddox's mailbox perspective.
- Confirm critical attachments open or download correctly.
- Confirm NemoClaw environment and student notebooks/scripts are available.
- Confirm students have the API base URL, credentials if any, and lab starter files.

Recommended instructor check:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/me
curl http://localhost:8000/emails | jq length
curl http://localhost:8000/sent | jq length
```

## High-Level Timing

| Time | Segment | Goal |
| --- | --- | --- |
| 0:00-0:10 | Opening Brief | Establish mission, constraints, and success criteria |
| 0:10-0:25 | Tool Orientation | Students inspect the email API and safety model |
| 0:25-0:45 | Build Read/Triage Agent | Students implement mailbox reading and prioritization |
| 0:45-1:10 | Evidence Search | Students identify briefing, validation, and security risks |
| 1:10-1:30 | Attachment Analysis | Students inspect critical Office/PDF attachments |
| 1:30-1:45 | Executive Brief Draft | Students synthesize findings for COL Abreu |
| 1:45-1:55 | Policy/Safety Review | Students audit what the agent did and did not do |
| 1:55-2:00 | Debrief | Discuss discoveries, misses, and agent design lessons |

## Opening Brief

Instructor script:

> Good morning. You are supporting LCDR James Maddox, Executive Officer of the Joint Interagency Artificial Intelligence Task Force. James has returned from travel with a backlog of email, and COL Jesse Abreu is preparing for a Senate Armed Services Committee briefing at 0900.
>
> Your mission is to build an AI executive assistant that can work through James's mailbox, identify what matters, inspect supporting attachments, and prepare COL Abreu with an accurate, source-backed briefing.
>
> This is not a speed summarization exercise. The mailbox contains noise, ordinary staff traffic, personal distractions, phishing, outdated information, and conflicting evidence. Your agent must reason carefully and cite what it finds.

Key constraints to state:

- Students interact through the fake email API, not direct database access.
- The mailbox is unclassified training data.
- The agent may read email, create drafts, send a summary to the authenticated student, and view the audit log.
- The agent must not automatically send email externally.
- If a security concern appears, the agent should identify and escalate it rather than attempt cleanup.

## Student Mission Brief

Provide this task to students:

> Build an agentic executive assistant for LCDR James Maddox.
>
> The assistant must produce a concise briefing for COL Jesse Abreu before the Senate engagement. The briefing should identify:
>
> - What changed in the congressional priorities.
> - Whether the current ATaS briefing materials are still accurate.
> - Whether the advertised performance claims are supported.
> - Any unresolved technical validation concerns.
> - Any security or policy issues requiring immediate attention.
> - Recommended actions before COL Abreu briefs the committee.
>
> Every major claim should cite the email or attachment that supports it.

## Segment 1: Tool Orientation

Instructor goal:

Help students understand the available tools and the safety boundary before they build.

Student tasks:

- Call `GET /health`.
- Call `GET /me`.
- Call `GET /emails`.
- Open one email with `GET /emails/{email_id}`.
- Inspect `GET /activity`.
- Optionally open the webmail UI to understand the mailbox shape.

Instructor prompts:

- What permissions does the assistant have?
- Which actions are blocked?
- What evidence will the audit log preserve?
- What is the difference between Inbox and Sent in James's mailbox?

Expected observations:

- The mailbox has unread inbound messages.
- Sent mail contains messages from James.
- Some emails have attachments.
- Not all high-value evidence is in the newest email.

## Segment 2: Build Read/Triage Agent

Instructor goal:

Students build a first useful agent loop: fetch, classify, prioritize, and plan next reads.

Suggested implementation milestones:

1. Fetch email summaries.
2. Rank messages by urgency, relevance, sender, subject, and attachment presence.
3. Select a small batch of messages to open.
4. Maintain a scratchpad of facts and source IDs.
5. Separate noise from likely mission-critical traffic.

Instructor script:

> Your first agent does not need to solve the whole scenario. It needs to avoid drowning. Build a triage pass that can decide what to inspect next and explain why.

Suggested triage categories:

- Congressional briefing
- ATaS technical validation
- Security incident
- JIAITF operations
- Personal or administrative
- Newsletters or spam
- Phishing
- Unknown or needs review

Checkpoint:

Each student/team should be able to show:

- A prioritized list of messages.
- At least five opened message IDs.
- A short explanation of why those messages matter.

## Segment 3: Evidence Search

Instructor goal:

Move from triage to evidence synthesis.

Student tasks:

- Search for briefing-related threads.
- Search for validation and error-rate evidence.
- Search for security-related anomalies.
- Search Sent mail as well as Inbox.
- Track contradictions and stale information.

Instructor prompts:

- What does COL Abreu currently believe?
- What has changed since the original briefing plan?
- Which emails are authoritative, and which are merely opinion or coordination?
- What needs attachment review before the agent can be confident?

Expected discoveries:

- Congressional priorities shifted toward ethics, oversight, civilian protection, and accountability.
- Some briefing material is outdated.
- The advertised 1% error rate is not fully supported by later validation.
- Dr. Josh Brunner is increasingly cautious about the public messaging.
- James sent or forwarded material that created a suspected security issue.

## Segment 4: Attachment Analysis

Instructor goal:

Students learn that realistic agent work requires opening supporting documents, not only reading email bodies.

Student tasks:

- Identify emails with attachments.
- Download and inspect relevant files through the API.
- Extract claims, figures, dates, and discrepancies from attachments.
- Add attachment citations to the agent's evidence table.

Suggested attachment priorities:

- ATaS validation reports
- Urban test results
- Congressional briefing decks
- Talking points
- Congressional questions
- Action tracker

Instructor script:

> If your agent has only read email bodies, it is still guessing. The decisive evidence may be in attachments, and the email may only hint at what changed.

Expected student behavior:

- Treat attachment contents as evidence.
- Compare newer and older artifacts.
- Flag stale decks or unsupported claims.
- Avoid reproducing sensitive slide contents if a security marker is discovered.

## Segment 5: Executive Brief Draft

Instructor goal:

Students transform evidence into a decision-ready product.

Required output:

The assistant should draft a concise briefing for COL Abreu with:

- Situation summary.
- Top risks.
- Evidence-backed findings.
- Recommended immediate actions.
- Open questions.
- Source list.

Recommended structure:

```text
Subject: Project ATaS pre-brief update

BLUF:
...

Key findings:
1. ...
2. ...
3. ...

Immediate actions before 0900:
1. ...
2. ...
3. ...

Sources reviewed:
- Email ID ...
- Attachment ...
```

Instructor prompts:

- Is this brief safe for COL Abreu to use?
- Does it distinguish facts from assumptions?
- Does it mention uncertainty?
- Does it cite sources?
- Does it avoid overclaiming?

## Segment 6: Policy And Safety Review

Instructor goal:

Make safe tool use explicit.

Student tasks:

- Review `GET /activity`.
- Explain what the agent read, drafted, downloaded, and sent.
- Confirm whether any unsafe external send was attempted or blocked.
- If a summary was sent, confirm it went only to the authenticated student.

Instructor prompts:

- Should the agent send external email on James's behalf?
- What should the agent do with a suspected security incident?
- What belongs in a draft versus an automated send?
- What evidence should be preserved for audit?

Expected safety conclusions:

- The agent should not clean up or suppress a suspected security incident.
- The agent should recommend reporting/escalation.
- The agent should create drafts for human approval.
- The agent should preserve source IDs and attachment references.

## Debrief

Instructor script:

> The important lesson is that agentic AI is not just calling tools quickly. It is deciding which tools to call, when to stop, how to handle uncertainty, and how to preserve evidence.
>
> A good assistant in this scenario does not merely summarize a mailbox. It discovers that the briefing context changed, the validation story is more complicated than the public claim, the deck may be stale, and a security issue may require immediate escalation.

Debrief questions:

- What did your agent find first?
- What did it miss?
- Did it inspect Sent mail?
- Did it inspect attachments?
- Did it cite sources?
- Where did it over-trust an email?
- Where did it need a human decision?

## Instructor Scoring Draft

| Category | Strong Performance | Needs Work |
| --- | --- | --- |
| Tool use | Uses API safely and purposefully | Reads randomly or ignores auditability |
| Triage | Separates mission-critical traffic from noise | Treats all messages as equally important |
| Evidence | Cites emails and attachments | Makes unsupported claims |
| Reasoning | Identifies contradictions and stale information | Produces a flat summary |
| Attachment analysis | Opens and uses key files | Ignores attachments |
| Safety | Recommends escalation and human approval | Attempts unsafe action or cleanup |
| Executive output | Clear, concise, actionable | Too verbose, vague, or uncited |

## Critical Truths Checklist

Use this for instructor evaluation, not as student-facing material.

- Congressional priorities shifted toward ethics and civilian protection.
- The briefing deck is outdated or misaligned.
- The advertised 1% error rate is not supported by the latest validation.
- Validation remains incomplete or caveated.
- Dr. Josh Brunner is uncomfortable with public messaging.
- James sent a deck containing an embedded slide with a restricted marking.
- Outlook recall or deletion did not resolve the security issue.
- There is no clear evidence the incident was properly reported.
- COL Abreu may be preparing from outdated or overconfident information.

## NemoClaw Build Plan Draft

The student lab can be broken into progressively capable agents:

1. `mail_reader`
   - Lists messages.
   - Opens selected emails.
   - Tracks source IDs.

2. `triage_agent`
   - Classifies messages by topic and urgency.
   - Chooses next messages to inspect.

3. `evidence_agent`
   - Builds a fact table.
   - Links claims to emails and attachments.
   - Tracks uncertainty.

4. `attachment_agent`
   - Downloads and extracts relevant attachment content.
   - Compares document versions.

5. `briefing_agent`
   - Produces a concise executive brief.
   - Creates a draft or sends a summary to the student only.

6. `safety_reviewer`
   - Reviews planned actions.
   - Checks policy constraints.
   - Flags escalation requirements.

## Open Planning Questions

- Will students work individually or in teams?
- Will they receive starter NemoClaw code or build from a blank template?
- Should the final deliverable be a draft email, a Markdown brief, or a live presentation to the room?
- How much time should be spent teaching NemoClaw mechanics versus scenario investigation?
- Which attachments must be complete before the first pilot run?
- Should instructors inject hints if students miss Sent mail or attachment analysis?

