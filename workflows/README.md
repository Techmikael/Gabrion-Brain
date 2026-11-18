# Workflows: how the agents work together

A workflow says, step by step, which lead agent owns the job, which specialists help, who reviews the work before
the founder sees it, and where the approval sits. Playbooks (`playbooks/`) say *how* a step is done; workflows say
*who* does it and in what order. Rules: `docs/AGENT-RULES.md`.

| Workflow | Starts when | Lead |
|---|---|---|
| [new-enquiry](new-enquiry.md) | A website form, chat or email arrives | front-desk |
| [outbound-week](outbound-week.md) | Every Monday | sales |
| [discovery-to-proposal](discovery-to-proposal.md) | A discovery call is booked | solutions-architect |
| [website-project](website-project.md) | A website proposal is signed | web-builder |
| [automation-ai-project](automation-ai-project.md) | An automation, chat or receptionist proposal is signed | automation-builder / voice-chat-builder |
| [software-project](software-project.md) | A software proposal is signed | software-engineer |
| [client-support](client-support.md) | A client ticket or alert | operations-support |
| [marketing-week](marketing-week.md) | Every Tuesday | founder (drafts by marketing specialists) |
| [month-end](month-end.md) | Last working day of the month | finance-admin |
| [learning-review](learning-review.md) | Every Friday | chief-of-staff |

Every workflow ends the same way: the lead updates the task row on `memory/tasks/board.csv`, every agent that
learned something adds a line to its lessons file, and anything that needs the founder is in the approval queue.
