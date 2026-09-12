# Security policy

## Supported versions

Security fixes are applied to the latest released minor version.

## Reporting a vulnerability

Do not open a public issue containing secrets, private conversation data, or an exploitable automation path. A public repository and private reporting contact have not yet been configured for this release candidate. The publisher must provide a real private security-reporting channel before public distribution; once available, use that channel to contact the owner.

Include the affected version, platform, reproduction conditions, expected behavior, and observed behavior. Remove tokens, credentials, personal data, and proprietary content.

## Security model

The plugin does not grant permissions. Automatic routing remains bounded by host capabilities, existing permissions, and the selected user-control mode. Unknown capability falls back to user operation, and a state change is never reported as applied without verification.

The optional Codex metadata helper uses a fixed read-RPC allowlist, bounded elapsed
time/output and selected fields only. It never starts/resumes a thread, submits a model
prompt or writes configuration. A launched host may still update caches/logs or contact
its provider. No status-line integration, daemon, telemetry service or automatic helper
execution is installed. Do not treat a separate CLI's defaults or persisted values as
current App settings; scope and freshness checks remain necessary.
