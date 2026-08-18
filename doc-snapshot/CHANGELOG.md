# Doc drift changelog

What the CopilotKit docs changed under this repo, written by the sync on
`/doc-sync`. Only pages that actually moved are recorded — a sync that finds
everything unchanged writes nothing here at all.

Holds the 3 most recent dated entries. When a change lands on a fourth
date, the oldest entry is dropped. Entries are counted, not aged, so a gap of
weeks between changes does not expire anything.

## 2026-08-18

### 06:37 UTC — 2 pages, highest severity medium

**Medium — Introduction** · _local snapshot edit, not an upstream change_

`/angular/claude-sdk-python` · routes `/`, `/doc-sync` · under “What is CopilotKit for Angular?”

1 heading changed.

````diff
+ ## What is CopilotKit for Angular?
````

**Low — Shared state and agent context** · _local snapshot edit, not an upstream change_

`/angular/claude-sdk-python/guides/shared-state` · route `/shared-state` · under “Read agent state”

3 prose lines changed.

````diff
- 
+ `injectAgentStore` returns a signal that resolves one agent. The store exposes
+ messages, state, and run status as nested signals.
````
