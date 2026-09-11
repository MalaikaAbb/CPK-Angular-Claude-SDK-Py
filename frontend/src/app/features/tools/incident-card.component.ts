/**
 * "Let the agent display one of your components", verbatim.
 * https://docs.copilotkit.ai/angular/claude-sdk-python/guides/frontend-tools-generative-ui
 *
 * Three deviations from the published snippet, all mechanical: `standalone: true` is dropped — it
 * is the default on Angular v20+ and frontend/AGENTS.md forbids setting it — the two imports are
 * narrowed to `type` imports, and prettier rewrites the template's double quotes to single ones.
 * All three match weather-card.component.ts.
 *
 * Unlike WeatherCardComponent this renderer never reads `call.result`: a display-only component has
 * no application code behind it, so the tool completes with an empty result and the args are the
 * whole payload.
 */
import { Component, input } from '@angular/core';
import { type AngularToolCall, type ToolRenderer } from '@copilotkit/angular';

type IncidentArgs = { id: string; severity: string };

@Component({
  selector: 'app-incident-card',
  template: `
    @let call = toolCall();
    @if (call.status === 'in-progress') {
      <p>Loading incident…</p>
    } @else {
      <article>
        <strong>{{ call.args.id }}</strong>
        <span>{{ call.args.severity }}</span>
      </article>
    }
  `,
})
export class IncidentCardComponent implements ToolRenderer<IncidentArgs> {
  readonly toolCall = input.required<AngularToolCall<IncidentArgs>>();
}
