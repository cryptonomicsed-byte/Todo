# LIBRARY_INTERFACE_V1 — Capability & Policy Libraries
Status: Draft v1
Date: 2026-04-28

## 1. Purpose
All complexity beyond `birth/think/act` is implemented as libraries.
No library may add new language primitives.

## 2. Library Classes
1. Policy Libraries
   - permissions
   - budget/cost controls
   - ethics/guardrails
   - rhythm/cooldowns
   - reputation model
2. Capability Libraries
   - web/search
   - browser automation
   - code execution
   - payments/chain ops
   - multi-agent coordination
3. Storage Libraries
   - private memory backends
   - public knowledge/index backends
   - chain receipt storage

## 3. Required Interfaces
Each library SHOULD expose:
- `name()`
- `version()`
- `capabilities()`
- `validate(input, state, policy_ctx)`
- `execute(input, state, policy_ctx)`
- `emit_receipt(result, state)`

Policy libraries additionally expose:
- `evaluate(action_ctx) -> allow|deny|transform`

## 4. Invocation Pipeline
1. Primitive parsed by core.
2. Core builds action context.
3. Policy chain evaluates (ordered, deterministic).
4. Capability executes if allowed.
5. Receipt emitted + state transition committed.

## 5. Determinism + Safety
- Policy ordering is explicit and version-pinned.
- Libraries must be side-effect declared.
- Non-deterministic operations must record entropy source in receipt.

## 6. Compatibility Rules
- Libraries can evolve without changing language grammar.
- Breaking interface change requires major version bump.
- Core must reject incompatible library manifests at startup.
