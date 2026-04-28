# MIGRATION_MATRIX_SWIBE_TO_3P
Status: Draft v1
Date: 2026-04-28

Goal: Preserve Swibe power while collapsing exposed syntax to 3 primitives.

| Swibe Surface Concept | 3P Mapping | Destination |
|---|---|---|
| ethics | `birth` init + policy checks on `think/act` | Policy library |
| secure block | enforced at `act` gate and runtime sandbox | Policy/runtime library |
| permission | evaluated before `act` | Policy library |
| budget | checked before/during `act` | Policy library |
| remember | internal side effect of `think`/`act` | Storage library |
| plan/chain | generated during `think` | Cognition library |
| swarm/team/coordinate | invoked as `act "swarm.*"` tools | Capability library |
| mcp/bridge/pilot/edit | invoked as `act` tool calls | Capability library |
| mint/receipt/seal/walrus | receipt + persistence adapters | Chain/storage libraries |
| loop/self-heal | orchestration policy over repeated `think/act` cycles | Runtime orchestrator library |
| plugin/pkg system | library manifest/registry | Library platform |

## Migration Steps
1. Freeze addition of new syntax primitives in source branches.
2. Define canonical intermediate representation for 3P execution.
3. Implement transpiler from legacy Swibe scripts to 3P action sequences.
4. Port policy/security modules first; then capability modules.
5. Add equivalence tests: legacy scenario vs 3P runtime output.
