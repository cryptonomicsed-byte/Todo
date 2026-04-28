# SPEC_V1 — 3-Primitive Agent Language
Status: Draft v1
Date: 2026-04-28

## 1. Language Contract
The public language surface is permanently constrained to exactly three primitives:
- `birth "name"`
- `think "intent"`
- `act "tool" "params"`

No additional top-level primitives are permitted.

## 2. Grammar (EBNF)
```ebnf
program     = { statement } ;
statement   = birth_stmt | think_stmt | act_stmt ;

birth_stmt  = "birth" string ;
think_stmt  = "think" string ;
act_stmt    = "act" string string ;

string      = '"' { char } '"' ;
char        = ? any UTF-8 char except unescaped quote ? ;
```

## 3. State Model
- Agent state fields (minimum):
  - `id`, `name`, `created_at`
  - `reputation` (0..100)
  - `tier`
  - `memory_private_ref`, `memory_public_ref`
  - `traits` (extensible map)
  - `tool_unlocks`
  - `sandbox_mode`

## 4. Primitive Semantics

### 4.1 `birth`
Input: agent name.
Effects:
- Creates agent identity.
- Initializes policy context and hidden runtime principles.
- Seeds default memory, reputation, and tool gating.
- Emits birth receipt/event.

### 4.2 `think`
Input: natural-language intent.
Effects:
- Updates cognition state (traits, plans, memory embeddings/indices).
- Writes private memory by default (unless explicit publish path via translator sugar).
- May produce plan suggestions but no privileged side effects.
- Emits think receipt/event.

### 4.3 `act`
Input: tool name + serialized params string.
Effects:
- Validates tool permission/tier/policy constraints.
- Executes capability via library adapter.
- Persists execution receipt.
- Updates reputation according to policy engine.
- Emits action receipt/event.

## 5. Execution Invariants
1. Parser MUST reject unknown primitives.
2. Interpreter MUST be deterministic for identical state + input + library version.
3. Every `act` MUST produce an auditable receipt (success/failure).
4. Tool execution MUST pass through policy gate.
5. Public/private memory boundaries MUST be explicit and auditable.

## 6. Error Model
- `E_PARSE_UNKNOWN_PRIMITIVE`
- `E_PARSE_BAD_ARITY`
- `E_STATE_NOT_BORN`
- `E_POLICY_DENIED`
- `E_TOOL_NOT_FOUND`
- `E_TOOL_NOT_UNLOCKED`
- `E_SANDBOX_RESTRICTION`
- `E_EXECUTION_FAILED`

Errors return structured payload:
- `code`, `message`, `hint`, `receipt_id?`

## 7. Versioning
- Language core: semantic versioned, strict backward compatibility for syntax.
- Libraries: independent semantic versions; loaded via manifest.
- Runtime must record `{core_version, library_set_hash}` in receipts.
