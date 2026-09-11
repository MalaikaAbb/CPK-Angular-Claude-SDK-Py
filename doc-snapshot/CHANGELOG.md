# Doc drift changelog

What the CopilotKit docs changed under this repo, written by the sync on
`/doc-sync`. Only pages that actually moved are recorded — a sync that finds
everything unchanged writes nothing here at all.

Holds the 3 most recent dated entries. When a change lands on a fourth
date, the oldest entry is dropped. Entries are counted, not aged, so a gap of
weeks between changes does not expire anything.

## 2026-09-04

### 15:14 UTC — 5 pages, highest severity high

**High — Frontend tools and generative UI**

`/angular/claude-sdk-python/guides/frontend-tools-generative-ui` · route `/frontend-tools-generative-ui` · under “Let the agent display one of your components”

36 code lines, 1 heading, 21 prose lines changed. The number of fenced code blocks changed.

````diff
+ ## Let the agent display one of your components
+ 
+ The simplest generative UI there is, and the only kind that needs nothing on the
+ agent side. `registerComponent` registers a standalone component as a tool the
+ agent can call to show it. The agent decides when, and fills the props.
+ 
+ ```ts title="src/app/incident-card.component.ts"
+ import { Component, input } from "@angular/core";
````

**High — Human-in-the-loop and interrupts**

`/angular/claude-sdk-python/guides/human-in-the-loop` · route `/human-in-the-loop` · under “Human-in-the-loop and interrupts”

26 code lines, 3 headings, 26 prose lines changed. The number of fenced code blocks changed.

````diff
- | Interrupt | The backend agent emits an AG-UI interrupt | `injectInterrupt` |
+ | Interrupt | The backend agent emits an AG-UI interrupt | `AgentStore.interruptController`, `injectInterrupt` |
- ## Handle an interrupt
+ ## Handle an interrupt from the store
+ An interrupt is a state of one conversation: this agent, this thread, this run
+ is waiting for a decision. The store that already exposes that conversation's
+ messages and state exposes its pending interrupt too, so a component that holds
+ a store needs nothing else:
````

**Medium — Introduction**

`/angular/claude-sdk-python` · routes `/`, `/doc-sync` · under “Angular”

1 heading, 19 prose lines changed.

````diff
- body="Add durable threads, inspection, and managed or self-hosted Enterprise Intelligence without changing the Angular frontend APIs in this guide."
+ body="Add durable threads, inspection, and managed or self-hosted CopilotKit Intelligence without changing the Angular frontend APIs in this guide."
- - Angular 20, 21, or 22
+ - Angular 22
- If you don't have one already, pin the CLI to one of the supported majors. This example uses Angular 22:
+ If you don't have one already, pin the CLI to the supported major:
+ <Step>
+ ### Open Inspector and confirm setup
````

**Medium — Quickstart**

`/angular/claude-sdk-python/quickstart` · route `/quickstart` · under “Angular”

1 heading, 19 prose lines changed.

````diff
- body="Add durable threads, inspection, and managed or self-hosted Enterprise Intelligence without changing the Angular frontend APIs in this guide."
+ body="Add durable threads, inspection, and managed or self-hosted CopilotKit Intelligence without changing the Angular frontend APIs in this guide."
- - Angular 20, 21, or 22
+ - Angular 22
- If you don't have one already, pin the CLI to one of the supported majors. This example uses Angular 22:
+ If you don't have one already, pin the CLI to the supported major:
+ <Step>
+ ### Open Inspector and confirm setup
````

**Low — A2UI schemas, styling, and recovery**

`/angular/claude-sdk-python/guides/a2ui` · route `/a2ui` · under “Angular support boundaries”

2 prose lines changed.

````diff
- - **Hashbrown is unsupported.** The stable Hashbrown Angular package does not support the complete Angular 20 through 22 policy.
+ - **Hashbrown is unsupported.** The stable Hashbrown Angular package does not support the Angular 22 policy.
````

---

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
