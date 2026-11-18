# Workflow: automation, chat or AI receptionist project

**Lead:** automation-builder (automations) or voice-chat-builder (chat, receptionist) · **Factories:** `factories/automation.md`, `factories/ai-receptionist.md` · **Ends with:** a `real-data` or `go-live` approval

| # | Step | Who | Reviewer | Output |
|---|---|---|---|---|
| 1 | Map today's process and the tools | lead with `specialized-workflow-architect` | | Process map |
| 2 | Design the automation or agent | lead with `automation-governance-architect` (who decides, what if it fails) | | Design + failure plan |
| 3 | Prompts and knowledge | `engineering-prompt-engineer`, `engineering-rag-pipeline-engineer` | | Prompts, knowledge files |
| 4 | Voice set-up (receptionists) | `engineering-voice-ai-integration-engineer` | | Test number |
| 5 | Build on sample data | lead with `engineering-ai-engineer` | `security-ai-generated-code-auditor` | Working sandbox |
| 6 | Test: 20 realistic cases, including angry, off-topic and Danish | `testing-api-tester`, `testing-reality-checker` | | Test log |
| 7 | Data protection check | `data-privacy-officer` | | Notes for the founder |
| 8 | Approval queue, type `real-data` then `go-live` | lead | | Queue items |
