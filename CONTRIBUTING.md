# Contributing

Edit root skills/ and shared/ only; never edit generated dist trees. Keep the three
Skills independent and preserve the descriptions locked in tests/trigger-contract.json.
Shared policy belongs in shared/runtime-routing-policy.md. A deliberate trigger change
requires an explicitly reviewed contract update, not a platform-specific patch.

Run the development commands in [the release guide](docs/release.md). Add meaningful
regression tests for validation or packaging changes and behavioral cases for routing
changes. All behavioral results must reference evidence; not_run is not a pass.
Update release.json and CHANGELOG.md together. Platform README sources live in
packaging/<platform>/README.md. Their repository-relative links are rebased automatically
when copied to the generated package root; both source and generated links are validated.

Do not add static model identifiers without runtime evidence, secrets, private
transcripts or employer-specific data. Preserve ask defaults and user authorization
boundaries. Public distribution is a separate owner action.
