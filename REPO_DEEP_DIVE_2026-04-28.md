# Repo Deep Dive — Swibe → 3-Primitive Convergence
Date: 2026-04-28

## Objective
Unify the ecosystem around a strict 3-primitive surface (`birth`, `think`, `act`) while moving all additional capabilities into libraries/runtime modules.

## Repos Reviewed
- https://github.com/Bino-Elgua/Swibe
- https://github.com/Bino-Elgua/Aether
- https://github.com/Bino-Elgua/OsO
- https://github.com/Bino-Elgua/Oso-Aether
- https://github.com/omo-koda/Swibe
- https://github.com/omo-koda/The-Aether

## Architectural Read (no mascot-specific scope)

### 1) Swibe (Bino-Elgua)
- Current state: large, multi-primitive, multi-layer language with broad surface area and 44 backend targets.
- Strengths to preserve as libraries:
  - security policy model (`secure`, sandbox intent, receipts, audits)
  - permission/budget governance
  - orchestration concepts (swarm/team/coordination)
  - packaging, plugin and runtime ergonomics
- Migration implication:
  - Swibe surface is too broad for strict 3-primitive doctrine.
  - Best use: source of runtime libraries + compiler internals, not final surface language.

### 2) Aether / The-Aether
- Current state: sovereign agent language framing, with marketplace/economy motifs and governance components.
- Core opportunity:
  - semantics of sovereignty and verifiable operations map cleanly into hidden runtime rules under `think`/`act`.
- Gap vs target:
  - still exposes additional top-level concepts (ethics/permission/receipt) as first-class primitives.
  - must be collapsed into internal policy engines and slash-sugar translation.

### 3) OsO / Oso-Aether
- Current state: strongest alignment with strict language minimalism in Rust core.
- Notable direction fit:
  - parser/interpreter boundary is explicit.
  - translation + execution logic living in Rust is aligned with “single source of truth.”
  - tool gating, memory, reputation, public/private publishing already modeled near execution layer.
- Gap vs target:
  - still needs canonicalized library boundaries so features remain extensions, never surface primitives.

### 4) Fork topology (omo-koda mirrors)
- `omo-koda/Swibe` and `omo-koda/The-Aether` appear as mirrors/forks useful for diffing divergence and preserving alternate experiments.
- Recommendation: treat as reference lanes, not canonical trunk.

## Convergence Plan (Swibe -> 3 primitives)

### A. Language Contract (non-negotiable)
- Public grammar remains only:
  - `birth "..."`
  - `think "..."`
  - `act "tool" "params"`
- Everything else becomes:
  - translator sugar, or
  - runtime library modules, or
  - policy configs consumed internally.

### B. Runtime Layering
1. **Core Kernel (Rust)**
   - parser + interpreter + state machine + receipts + policy evaluation.
2. **Policy Libraries (internal)**
   - hermetic principles mapping, permissions, sandbox, rhythm/cooldowns, reputation.
3. **Capability Libraries (tool packs)**
   - web, code, browser, payments, orchestration.
4. **Adapters**
   - chain storage, encrypted memory backends, index/search layers.
5. **UX Sugar Layer**
   - slash commands and NL prompts compile to 3 primitives.

### C. Migration Moves
1. Freeze primitive expansion in Swibe/Aether branches.
2. Extract reusable subsystems from Swibe into crates/packages:
   - security policy engine
   - budget/permission evaluator
   - orchestration planner
3. Standardize one canonical interpreter contract:
   - `translate_input`
   - `execute`
   - `process`
   - deterministic receipt output
4. Move all command-like UX into translator mapping table.
5. Add compatibility mode to parse legacy scripts and transpile to 3-primitive IR.

## Decisions Captured
- Final system identity: **3-primitive sovereign agent framework**.
- Swibe contributes power as **library source**, not as exposed syntax model.
- Rust core remains single source of truth for state, execution, and reputation.
- Hidden soul/policy model remains internal (never command surface).

## Immediate Backlog
1. Write formal 3-primitive spec v1 (grammar + semantics + error model).
2. Define Library Interface Spec (tool packs, policies, storage).
3. Create migration matrix: Swibe primitive -> internal library/policy mapping.
4. Build conformance tests to guarantee no new surface primitives leak.
5. Draft repo governance: canonical repo + satellite repos.
