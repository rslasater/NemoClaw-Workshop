# PROJECT_HANDOFF.md

# Project ATaS --- Development Handoff

**Status:** Ready to transition from design to implementation.

## Repository

Target repository: `rslasater/NemoClaw-Workshop`

## Vision

Project ATaS is a story-driven Agentic AI workshop built around NVIDIA
NemoClaw.

Students act as the AI Executive Assistant to **LCDR James Maddox**,
Executive Officer of the Joint Interagency Artificial Intelligence Task
Force (JIAITF), preparing **COL Jesse Abreu** for a Senate Armed
Services Committee briefing after a week of accumulated email.

The objective is not email summarization. The objective is planning,
reasoning, prioritization, attachment analysis, and safe tool use.

## Completed Design Work

-   Scenario Bible
-   Thread Catalog
-   Instructor Guide
-   Truth Matrix
-   Mailbox Blueprint
-   Character Knowledge States
-   Fake email API architecture
-   Webmail UI concept

## Mailbox

-   Approximately 235 unread emails
-   Realistic Outlook reply chains
-   Chronological over one week
-   Mixed signal and noise
-   Real Office attachments
-   Stable message IDs

## Major Story Arcs

1.  Project ATaS
2.  Congressional Briefing
3.  JIAITF Operations
4.  Security Incident
5.  James Maddox's Personal Life
6.  Newsletters, Spam, and Phishing

## Critical Truths

Students should discover:

-   Congressional priorities shifted toward ethics and civilian
    protection.
-   The briefing deck is outdated.
-   The advertised 1% error rate is not supported by the latest
    validation.
-   Dr. Josh Brunner is increasingly uncomfortable with the public
    messaging.
-   Validation remains incomplete.
-   James unintentionally sent a presentation containing one embedded
    SECRET//NOFORN slide.
-   Outlook recall did not resolve the incident.
-   There is no evidence the incident was reported.
-   COL Abreu is preparing using outdated information.

## Security Constraint

The mailbox itself is UNCLASSIFIED.

There are no classified emails.

The only classified content is a single embedded slide inside one
PowerPoint attachment.

## Architecture

Email source → SQLite → FastAPI → FakeMail Web UI → NemoClaw tools

Students interact only through the API.

## Recommended Repository Layout

docs/ Scenario_Bible.md Thread_Catalog.md Instructor_Guide.md
Truth_Matrix.md

fake-email-api/

project-atas/ blueprints/ threads/ attachments/ compiler/ generated/

student-lab/

## Next Milestones

1.  Finish FakeMail API.
2.  Add attachment endpoints.
3.  Build mailbox compiler.
4.  Define Markdown authoring format.
5.  Author email threads.
6.  Compile to emails.json.
7.  Generate Office documents.
8.  Seed SQLite.
9.  Integrate NemoClaw.
10. Complete workshop lab.

## Guiding Principles

-   Every critical fact should appear multiple times.
-   Characters only know what they realistically know on a given day.
-   Noise should feel authentic.
-   Students should synthesize evidence rather than locate a single
    email.
-   Keep the dataset deterministic and version-controlled.

## Long-Term Vision

Project ATaS should become a reusable simulation platform.

Future scenarios should reuse the FakeMail platform, mailbox compiler,
attachment pipeline, and instructor framework while swapping only the
scenario content.
