# Specialist agents (agency-agents)

The Brain's 10 Gabrion agents do the work and keep to the approval rules. The 70 agency-agents specialists are expert advisers you or the Chief of Staff can call on for one piece of work. Install or update them with:

```bash
bash scripts/install_agency_agents.sh
```

They follow `CLAUDE.md` like every other agent: they draft and advise, and anything that touches money, clients or production still goes to `memory/approvals/queue.md`. Their files were written for any company, so where they disagree with a Gabrion playbook, the playbook wins.

## Which specialist for which job

| Gabrion step | Gabrion agent | Specialists to call on |
|---|---|---|
| Website chat lead arrives | front-desk | Support Responder (reply tone), Discovery Coach (qualifying questions) |
| Finding prospects | sales | Outbound Strategist (ICP and sequences), Offer & Lead Gen Strategist (lead magnets), Reddit Community Builder, LinkedIn Content Creator |
| Preparing a discovery call | solutions-architect | Discovery Coach, Sales Engineer (demo plan) |
| Writing a proposal | solutions-architect | Proposal Strategist, Deal Strategist (risk and qualification) |
| Pipeline review | chief-of-staff | Pipeline Analyst, Sales Coach |
| After a sale | operations-support | Account Strategist (expansion, reviews), Feedback Synthesizer |
| Website projects | web-builder | SEO Specialist, AEO Foundations Architect, AI Citation Strategist |
| New service or template idea | founder | Product Manager, Trend Researcher, Sprint Prioritizer |
| Running delivery | chief-of-staff | Senior Project Manager, Project Shepherd, Meeting Notes Specialist |
| Money | finance-admin | Bookkeeper & Controller, FP&A Analyst, Tax Strategist (UK: confirm with your accountant) |
| Contracts and data protection | founder | Legal Compliance Checker (confirm with a solicitor) |
| Phase 3 marketing | founder | Content Creator, Social Media Strategist, Email Marketing Strategist, PR & Communications Manager, Video Optimization Specialist |
| Daily or weekly summary | chief-of-staff | Executive Summary Generator, Analytics Reporter |

The China-market specialists (Douyin, Xiaohongshu, WeChat, Baidu and others) are installed too but don't fit a UK business today; ignore them unless you sell into China.

## How to use one
In Claude Code, inside the gabrion-brain folder:

> Use the Proposal Strategist agent to improve the draft in clients/bloom/proposal/proposal.md. Keep our pricing and playbooks/proposal.md structure.

> Use the Discovery Coach agent to write 10 questions for tomorrow's call with a dental clinic that misses calls.

Note: Claude Code agents can't call other agents themselves, so you (or the main Claude session) ask the specialist, then hand the result back to the Gabrion agent.
