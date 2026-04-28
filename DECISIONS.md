# DECISIONS

## D-001: Use dedicated `todo` repo as execution memory
- Date: 2026-04-28
- Context: Need persistent progress tracking and recall continuity.
- Decision: Maintain roadmap/tasks/decisions/log with context snapshots.
- Consequence: Clearer accountability and less state loss.


## D-002: Strategic direction after repo deep dive
- Date: 2026-04-28
- Context: Multiple repos show broad agent language features, but product direction demands strict surface minimalism.
- Decision: Keep only `birth/think/act` on the public language surface; move all other capabilities into internal libraries and translator sugar.
- Consequence: Stronger long-term coherence, simpler UX, and safer governance of feature growth.
