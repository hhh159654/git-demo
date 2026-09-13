# paper1

- Topic: TODO: define a concrete research question
- Domain: EDA / analog circuit simulation
- Target: strong CCF-C; stretch goal weak CCF-B
- Default compute: at most one remote A800 unless explicitly approved otherwise

## Review loop

1. Codex reads `AGENTS.md`, performs research/implementation, writes `steps/` and `results/`.
2. Push current branch to GitHub.
3. ChatGPT reviewer reads this paper folder only and creates a new `review_roundN.md`.
4. Pull the branch locally.
5. Codex implements the atomic action items and writes `response_roundN.md`.
6. Repeat until the evidence is strong enough or the direction is archived.

Use `autoresearch status paper1` to inspect the 16-stage research state.
