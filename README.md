# CopilotKit + Claude Agent SDK Python — Angular frontend

A navigable test harness for the Angular + Claude Agent SDK Python section of the CopilotKit docs.
Every guide in the sidebar is a route, and each route runs the thing its doc page teaches. Routes
with a live feature also expose a chrome-free demo at `<route>/demo`.

Docs: https://docs.copilotkit.ai/angular/claude-sdk-python

## Architecture

Three processes, not two. Unlike the React quickstart — where the runtime lives inside the Next app
— Angular has no server route, so the Copilot Runtime is its own Node process. The model key only
ever reaches the Python process.

```
Browser (Angular 22, zoneless)  ·  localhost:4200
  |  @copilotkit/angular — provideCopilotKit, copilot-chat, signal APIs
  |  POST http://localhost:8200/api/copilotkit
  v
Copilot Runtime  ·  localhost:8200               <- Node, frontend/server.ts
  |  agents: { default, support } -> new HttpAgent({ url })
  |  POST http://localhost:8000/                 <- AG-UI over SSE
  v
Claude Agent SDK Python agent  ·  localhost:8000  <- Python / FastAPI, backend/main.py
  |  ClaudeAgentAdapter(...).run(input)
  v
Model  (claude-sonnet-4-6)
```

`default` and `support` resolve to the same Claude Agent SDK Python process. `support` exists so the
doc snippets that use `agentId="support"` (Chat UI, Threads) run verbatim.

## Prerequisites

- Node.js 20+ and npm
- [uv](https://docs.astral.sh/uv/) and Python 3.13 for the backend
- An `ANTHROPIC_API_KEY` (or an already-authenticated Claude Code CLI on this machine)

## Running the project

Three terminals, in this order. All three must be up or the chat will not stream.

### 1 · The Claude Agent SDK Python agent — port 8000

```bash
cd backend
uv sync
uv run uvicorn main:app --port 8000
```

Set your key first, either in the shell or in a `backend/.env` file (`main.py` calls `load_dotenv()`):

```bash
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-6   # optional, this is the default
```

Check it: `curl http://localhost:8000/health` → `{"status":"ok"}`.

### 2 · Copilot Runtime — port 8200

```bash
cd frontend
npm install
npm run runtime
```

Check it: `curl http://localhost:8200/api/copilotkit/info` should list the `default` and `support`
agents.

### 3 · The Angular app — port 4200

```bash
cd frontend
npm start
```

Open http://localhost:4200. The Introduction route runs a live connection check against both
backends.

### Shortcut

`npm run dev` (from `frontend/`) starts the runtime and the Angular dev server together with
`concurrently`, so only the Python agent needs its own terminal.

## Configuration

| What                       | Where                                   | Default                                |
| -------------------------- | --------------------------------------- | -------------------------------------- |
| Agent URL the runtime uses | `CLAUDE_AGENT_URL` env var              | `http://localhost:8000/`               |
| Runtime port               | `PORT` env var (for `server.ts`)        | `8200`                                 |
| Runtime URL the app uses   | `runtimeUrl` in `src/app/app.config.ts` | `http://localhost:8200/api/copilotkit` |
| Model                      | `ANTHROPIC_MODEL` in `backend/`         | `claude-sonnet-4-6`                    |

## Other scripts

| Command                      | What it does                                                             |
| ---------------------------- | ------------------------------------------------------------------------ |
| `npm run build`              | Production build into `dist/`                                            |
| `npm test`                   | Unit tests with Vitest                                                   |
| `npm run gen:sources`        | Re-embed implementation files so routes display the exact code that runs |
| `npm run serve:ssr:frontend` | Serve the SSR build from `dist/`                                         |

`gen:sources` runs automatically before `start` and `build`. Run it by hand after editing anything
under `src/app/features/`, `server.ts`, `src/styles.css`, or `src/app/app.config.ts` if you want the
displayed source to refresh without a restart.

## Where things live

| Path                        | What it is                                                            |
| --------------------------- | --------------------------------------------------------------------- |
| `server.ts`                 | Copilot Runtime — the one file binding CopilotKit to the Python agent |
| `src/app/app.config.ts`     | `provideCopilotKit` at the application root                           |
| `src/app/lib/nav-config.ts` | Every route, its doc page, and its implementation status              |
| `src/app/pages/`            | One page per doc route: notes, pass/fail criteria, source             |
| `src/app/features/`         | The live implementations the demo routes mount                        |

## Troubleshooting

**Nothing streams.** Check the connection panel on the Introduction route, or hit
`http://localhost:8200/api/copilotkit/info` directly — this is the check the quickstart's
troubleshooting box prescribes. One of the two backends is down.

**Port 8200 already in use.** A runtime is already running. Stop it, or start a second one on
another port with `PORT=8299 npm run runtime` and point `runtimeUrl` at it.

**The agent answers but tools never fire.** `allowed_tools` in `backend/main.py` names each MCP tool
by its exact string (`mcp__agent_tools__getWeather`). A name mismatch silently disables the tool.

## Known limitations

These are properties of what this repo runs, not bugs to fix here. The `/status` route lists all of
them alongside the doc page each one belongs to.

- **A2UI** stays inert until an `a2ui.catalog` is supplied — supplying one is what registers the
  `render_a2ui` renderer. `/info` reporting `a2uiEnabled: true` is not sufficient.
- **Voice transcription** fails by design: the microphone records, but this runtime has no
  transcription service configured.
- **Threads and memory** come from the CopilotKit Enterprise Intelligence Platform. Unlicensed, the
  thread list stays empty, the drawer renders its locked state, and `isAvailable()` is false for
  memories — which is the expected result here.
