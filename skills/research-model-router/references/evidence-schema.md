# Research Model Router evidence schema

This schema is internal diagnostic evidence. Do not render it in ordinary compact routing output. Read it only when the user requests diagnostics or when maintaining the router implementation.

```yaml
skill: research-model-router
phase: short description of the upcoming work phase
task_requirements:
  capabilities: [phase-specific needs, not model names]
  reasoning_demand: low | moderate | high
  quality_and_validation: short requirement
  latency_and_usage: user constraints or unspecified
discovery:
  status: not_probed | available | partial | unavailable | permission_denied | error | stale | scope_mismatch
  attempts: [source, outcome and limitation, without secrets]
  scope: product, surface, execution host and effective context
  observed_at: timestamp | unknown
  missing_information: []
capability_evidence:
  source: runtime description | official documentation | task evaluation | unavailable
  reference: source identifier or URL | null
  observed_at: timestamp | unknown
  recommendation_basis: inferred | measured | insufficient
current_configuration:
  model: observed model name | unknown
  reasoning_effort: observed effort | unknown | unsupported
  evidence: runtime metadata | user-provided settings | cached observation | unavailable
  scope: matching live configuration | user-reported | unknown
model_catalog:
  availability: available | unknown
  source: runtime metadata | user-provided settings | cached observation | versioned fallback | unavailable
  observed_at: timestamp | unknown
  cache_scope: current session | host-defined short lifetime | none
  applicable_to_context: verified | unverified | mismatch
assessment: suitable | change_recommended | unverified | deferred
minimum_sufficient_setting:
  model: supported model name | CURRENT | null
  reasoning_effort: supported effort | CURRENT | null
  availability: verified | unverified | unknown
  reason: why this is sufficient for the task
recommended_setting:
  model: supported model name | CURRENT | null
  reasoning_effort: supported effort | CURRENT | null
  availability: verified | unverified | unknown
upgrade_value: low | medium | high
upgrade_reason: additional value over the minimum, or why a stronger pair would not help
confidence: 0.00-1.00
reason: one concise phase-specific explanation
mode: off | ask | auto
disposition: skipped | awaiting_user_confirmation | awaiting_user_action | applied | kept_current
revisit_at: meaningful next stage transition | null
runtime_capabilities:
  surface: identified surface or unknown
  switch_current_model: agent | orchestrator | user_only | unavailable | unknown
  set_model_for_new_run: agent | orchestrator | user_only | unavailable | unknown
  set_reasoning_effort: agent | orchestrator | user_only | unavailable | unknown
  evidence: runtime metadata | user-provided settings | cached observation | unavailable
  observed_at: timestamp | unknown
  confidence: 0.00-1.00
execution:
  requested_owner: agent | orchestrator | user | none
  effective_owner: agent | orchestrator | user | none
  status: skipped | awaiting_user_confirmation | awaiting_user_action | applied | retained_current | blocked
  reason: concise explanation
  manual_action: null | surface-specific instruction
```

In `ask`, record `disposition: awaiting_user_confirmation` and the matching execution
status after presenting the settings, even when the current pair appears suitable;
`manual_action` may hold the surface-specific control. In `auto`, when switching is
unavailable but downstream work remains authorized, record `disposition: kept_current`
and `execution.status: retained_current` while continuing with the current setting.
