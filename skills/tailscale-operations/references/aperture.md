# Aperture access adapter

Official documentation checked on 2026-09-11. Recheck before setup or after
an upgrade. Keep installation, discovery, and successful execution separate.

## Connect an existing gateway

Use the actual gateway URL supplied by its owner, with its `/v1/mcp` endpoint
and Streamable HTTP transport. Discover the exposed tool schemas instead of
assuming this document's names are installed. Connector IDs prefix tool names.
Use current `connectors.servers` configuration for new connectors.
See [MCP server proxying](https://tailscale.com/docs/aperture/mcp-server).

Store endpoint configuration with the agent client and credentials with its
approved secret store. Do not put credentials in a skill or Nix derivation.
Adding a connector does not require changing the agent's model provider.

## Built-in connector facts

The built-in connectors remain alpha in the checked documentation.
They need admin setup. Tailscale SSH needs a gateway with its own tailnet node,
SSH-enabled targets, and suitable tailnet policy.

With default connector IDs:

- `TailnetSSH_list_machines` lists SSH-enabled machines, not the whole fleet.
- `TailnetSSH_run_command` requires `machine` and `command`. Optional `user`
  defaults to root; `timeout` defaults to 300 seconds, maximum 600.
- Each command uses a fresh session. Remote nonzero exit codes are tool results,
  not MCP transport errors. Output can truncate near 1 MiB. Audit records
  include the command, not its output.
- `Tailnet_provision_node` starts browser approval, then returns a single-use
  join key on a later call. Approval is required for each new node.
- SSH guided setup grants `TailnetSSH/**` to the configuring admin. Inspect
  that grant before claiming discovery-only access.

See [built-in connectors](https://tailscale.com/docs/aperture/connectors/built-in-connectors)
for current setup, enrollment timing, and tool schemas.

## Apply narrow authority

Gateway connectivity does not grant tool access. Grants are additive; a narrow
grant cannot cancel a broader one. A `restricted` label does not restrict access.
Review every matching grant. Aperture-local grants omit `dst`; grants placed
in the tailnet policy include the gateway destination.
See [how grants work](https://tailscale.com/docs/aperture/how-grants-work).

Start a new integration with discovery alone. Enable command execution only
for the intended caller, target cohort, and remote user. A shell tool grant
allows arbitrary commands as that user; calling it a read-only workflow does
not enforce read-only access. Keep the unattended planner separate from an
executor with mutation authority.

For each SSH call, explicitly set the intended unprivileged `user`, exact
`machine`, and a task-appropriate `timeout` (30 seconds for a small observation).
Include needed working-directory setup in that call. Keep credentials out of
command text. Check the remote exit status and output completeness, then verify
the owning task's postcondition. On timeout, reconcile state before repeating.

If discovery or execution fails, distinguish client-to-gateway access, connector
setup/grants, gateway-to-target access, and remote command failure. Do not switch
to another identity to work around a denial. Retain an independently authorized
CLI route for gateway outages; report which identity supplied each observation.

## Qualification

Before adopting an integration, demonstrate narrow discovery, a harmless command
as the intended user, interpretation of a nonzero remote exit, and denied access
outside the agreed scope. Use disposable fixtures for failure tests. Record the
gateway/connector versions, policy revision, caller and remote identities, and
verification date. Requalify after changes to those contracts. Skill presence
alone is not evidence of MCP readiness.
