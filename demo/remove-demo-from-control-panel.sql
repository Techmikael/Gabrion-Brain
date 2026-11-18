-- Removes every demo row added to the gabrion-control CRM (Neon project "brain") on 2026-11-18.
-- Run before your first real customer. Only touches rows tagged [DEMO] / source_site 'demo-brain'.
begin;
delete from lead   where source_site = 'demo-brain' and organisation like '[DEMO]%';
delete from client where name  like '[DEMO]%';
delete from goal   where title like '[DEMO]%';
commit;
