# Angular

> Connect an Angular app to Copilot Runtime with CopilotKit.

`@copilotkit/angular` provides Angular components, directives, and services for CopilotKit. This guide gets you to a working Angular app with a chat UI backed by [Copilot Runtime](/angular/claude-sdk-python/backend/copilot-runtime). When you select an agent backend in the sidebar, the backend step below changes with it; without a selection, the guide uses CopilotKit's `BuiltInAgent`.

The runtime runs on your server, keeps model credentials out of the browser, and exposes the `default` agent that `CopilotChat` uses automatically.

<OpsPlatformCTA
  variant="inline"
  title="Take your Angular copilot from local to production"
  body="Add durable threads, inspection, and managed or self-hosted Enterprise Intelligence without changing the Angular frontend APIs in this guide."
  surface="docs:angular/quickstart:production"
/>

## What is CopilotKit for Angular?

CopilotKit for Angular is the first-party, signal-based Angular frontend for
AG-UI agents and Copilot Runtime. It provides complete chat surfaces and
headless APIs, and it supports zoneless applications.

## Prerequisites

- An OpenAI API key (or another model provider supported by [Model Selection](/angular/model-selection))
- Angular 20, 21, or 22
- Node.js 22

## Getting started

<Steps>
    <Step>
        ### Create your Angular app

        If you don't have one already, pin the CLI to one of the supported majors. This example uses Angular 22:

        ```bash
        npx @angular/cli@22 new my-copilot-app
        cd my-copilot-app
        ```
    </Step>
    <Step>
        ### Install CopilotKit

        Install the Angular frontend package, `@angular/cdk`, and `@copilotkit/runtime` for your local Copilot Runtime server:

        <Tabs groupId="package-manager" items={['npm', 'pnpm', 'yarn']}>
            <Tab value="npm">
                ```bash
                npm install @copilotkit/angular @angular/cdk @copilotkit/runtime
                npm install -D tsx typescript @types/node
                ```
            </Tab>
            <Tab value="pnpm">
                ```bash
                pnpm add @copilotkit/angular @angular/cdk @copilotkit/runtime
                pnpm add -D tsx typescript @types/node
                ```
            </Tab>
            <Tab value="yarn">
                ```bash
                yarn add @copilotkit/angular @angular/cdk @copilotkit/runtime
                yarn add -D tsx typescript @types/node
                ```
            </Tab>
        </Tabs>

        <Callout type="info" title="Match @angular/cdk to your Angular version">
          `@angular/cdk` must share your Angular major version. Most package managers resolve this for you, but if you hit a peer-dependency error, pin it explicitly (for example `@angular/cdk@^22`).
        </Callout>
    </Step>
    
    
      <Step>
        ### Connect the selected agent backend

        This URL keeps the agent backend selected. The Angular setup remains
        shared; the backend setup below comes from that integration's canonical
        showcase source.

        <Steps>
  <Step>
    ### Install the Claude Agent SDK packages

    ```bash
    uv add claude-agent-sdk ag-ui-claude-sdk ag-ui-protocol anthropic fastapi uvicorn python-dotenv
    ```
  </Step>

  <Step>
    ### Bridge Claude Agent SDK to AG-UI

    Use `ClaudeAgentAdapter` from `ag_ui_claude_sdk`. The adapter receives the
    AG-UI run input, emits AG-UI events back to CopilotKit, and can expose
    backend tools through an in-process Claude SDK MCP server.

    
~~~~python title="claude_agent_sdk_adapter.py"
async def run_with_claude_agent_sdk(
    input_data: RunAgentInput,
    *,
    system_prompt: str,
    tools: list[dict[str, Any]],
    state: Any,
    model: str,
    execute_tool: ExecuteTool,
    max_turns: int = 10,
) -> AsyncIterator[str]:
    """Run through the official AG-UI Claude adapter and emit SSE chunks."""

    encoder = EventEncoder()
    state_box = {"state": state}
    pending_state_snapshots: list[Any] = []
    sdk_tools = _build_sdk_tools(
        tools,
        execute_tool=execute_tool,
        get_state=lambda: state_box["state"],
        set_state=lambda next_state: _set_state(
            next_state,
            state_box,
            pending_state_snapshots,
        ),
    )

    options: dict[str, Any] = {
        "model": _normalize_claude_agent_sdk_model(model),
        "system_prompt": system_prompt,
        "tools": [],
        "permission_mode": "dontAsk",
        "max_turns": max_turns,
    }

    if sdk_tools:
        options["mcp_servers"] = {
            COPILOTKIT_MCP_SERVER_NAME: create_sdk_mcp_server(
                COPILOTKIT_MCP_SERVER_NAME,
                "1.0.0",
                tools=sdk_tools,
            )
        }
        options["allowed_tools"] = [
            f"{COPILOTKIT_TOOL_PREFIX}{schema['name']}" for schema in tools
        ]

    adapter = ClaudeAgentAdapter(
        name="claude-sdk-python",
        options=options,
    )
    run_input = _with_initial_state(input_data, state)

    async for event in adapter.run(run_input):
        if event.type == EventType.TOOL_CALL_RESULT and pending_state_snapshots:
            yield encoder.encode(
                StateSnapshotEvent(
                    type=EventType.STATE_SNAPSHOT,
                    snapshot=pending_state_snapshots.pop(0),
                )
            )
        yield encoder.encode(event)


~~~~

  </Step>
</Steps>

        <Callout type="info" title="Expose the selected backend through Copilot Runtime">
          Configure Copilot Runtime to register this backend as the `default`
          agent at `/api/copilotkit`. Continue with the selected backend's
          [Copilot Runtime guide](backend/copilot-runtime) for its runtime
          adapter, credentials, and server command. Do not replace it with the
          `BuiltInAgent` server from the standalone Angular path.
        </Callout>
      </Step>
    
    <Step>
        ### Import the styles

        Add the package stylesheet to your global styles. It's self-contained, so the chat renders without any other CSS.

        ```css title="src/styles.css"
        @import "@copilotkit/angular/styles.css"; /* [!code highlight] */
        ```
    </Step>
    <Step>
        ### Connect to Copilot Runtime

        Point `provideCopilotKit` at the runtime endpoint. The chat uses the agent that your runtime registers as `default`.

        ```ts title="src/app/app.config.ts"
        import { ApplicationConfig } from "@angular/core";
        import { provideCopilotKit } from "@copilotkit/angular"; // [!code highlight]

        export const appConfig: ApplicationConfig = {
          providers: [
            // [!code highlight:3]
            provideCopilotKit({
              runtimeUrl: "http://localhost:8200/api/copilotkit",
            }),
          ],
        };
        ```
    </Step>
    <Step>
        ### Add the chat UI

        Import the `CopilotChat` component into your root component and drop it into the template.

        ```ts title="src/app/app.ts"
        import { Component } from "@angular/core";
        import { CopilotChat } from "@copilotkit/angular"; // [!code highlight]

        @Component({
          selector: "app-root",
          imports: [CopilotChat], // [!code highlight]
          template: `
            <!-- [!code highlight:3] -->
            <div style="height: 100vh">
              <copilot-chat />
            </div>
          `,
        })
        export class App {}
        ```

    </Step>
    
    
      <Step>
        ### Run the backend, runtime, and Angular app

        Start the selected agent backend and Copilot Runtime with the commands
        from its runtime guide. Confirm
        `http://localhost:8200/api/copilotkit/info` reports the `default`
        agent, then start Angular:

        ```bash
        npm start
        ```

        Open the Angular CLI URL (usually `http://localhost:4200`) and send a
        message. The request now follows the selected path end to end:
        Angular → Copilot Runtime → your selected agent backend.
      </Step>
    

</Steps>

## Next steps

- [Runtime and backend docs](backend/copilot-runtime): configure the server, secure requests, and deploy without leaving the selected Angular surface.
- [Enterprise Intelligence](premium/overview): add durable threads, inspection, and cloud-hosted or self-hosted operations.
- [Angular task guides](guides/chat-ui): build chat UI, tools, generative UI, interrupts, shared state, threads, memory, attachments, and headless UI.
- [Angular feature examples](features): find runnable examples and canonical shared Angular source for each supported feature.
- [Angular API reference](/reference/angular): use components, signals, tools, context, and runtime services.
- [Production and lifecycle](/reference/angular/production-lifecycle): handle cleanup, errors, server rendering, hydration, zoneless Angular, and browser-only features.
