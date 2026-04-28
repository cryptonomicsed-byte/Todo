# CONFORMANCE_TESTS_V1
Status: Draft v1
Date: 2026-04-28

## A. Syntax Guardrail Tests
1. Reject unknown primitive (e.g., `evolve "x"`).
2. Reject wrong arity for each primitive.
3. Accept UTF-8 payloads in strings.

## B. State Transition Tests
1. `think` before `birth` -> `E_STATE_NOT_BORN`.
2. `act` before `birth` -> `E_STATE_NOT_BORN`.
3. `birth` initializes required state fields.

## C. Policy Gate Tests
1. Disallowed tool returns `E_POLICY_DENIED`.
2. Locked tier tool returns `E_TOOL_NOT_UNLOCKED`.
3. Sandbox-on restricts side-effectful tools.

## D. Receipt Integrity Tests
1. Every `act` emits receipt with deterministic schema.
2. Failed `act` still emits failure receipt.
3. Receipt includes core version + library set hash.

## E. Determinism Tests
1. Same input/state/library versions -> same output/receipt hash (except declared entropy fields).
2. Policy evaluation order stable and auditable.

## F. Boundary Tests (No Primitive Expansion)
1. Slash commands must compile to 3P only.
2. Translator cannot emit any opcode beyond `birth/think/act`.
3. CI fails if grammar adds new top-level primitive token.
