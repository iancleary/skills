from __future__ import annotations

from dataclasses import dataclass, field

from helpers.pinmap import ConnectionDef, PinDef


@dataclass(frozen=True)
class EndpointSchema:
    family: str
    pin_count: int | None = None
    required_signals: tuple[str, ...] = ()
    allowed_signals: tuple[str, ...] | None = None
    exact_signals: tuple[str, ...] | None = None
    pin_map: tuple[tuple[str, str], ...] | None = None


@dataclass(frozen=True)
class HarnessSchema:
    name: str
    left: EndpointSchema
    right: EndpointSchema
    required_connections: tuple[tuple[str, str], ...] = ()
    forbid_unconnected_signals: bool = True
    ignored_signals: tuple[str, ...] = ("NC", "NC1", "NC2", "NC3", "NC4")
    aliases: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class BusParticipant:
    label: str
    role: str
    pins: tuple[PinDef, ...]
    shield_policy: str = "none"
    drain_policy: str = "none"
    termination_policy: str = "none"
    bias_policy: str = "none"
    pullup_policy: str = "none"
    poe_policy: str = "none"


@dataclass(frozen=True)
class BusSchema:
    name: str
    roles: dict[str, EndpointSchema]
    min_role_counts: dict[str, int] = field(default_factory=dict)
    max_role_counts: dict[str, int | None] = field(default_factory=dict)
    shield_values: tuple[str, ...] = ("none",)
    drain_values: tuple[str, ...] = ("none",)
    termination_values: tuple[str, ...] = ("none",)
    bias_values: tuple[str, ...] = ("none",)
    pullup_values: tuple[str, ...] = ("none",)
    poe_values: tuple[str, ...] = ("none",)
    required_role_policies: dict[str, dict[str, tuple[str, ...]]] = field(default_factory=dict)
    forbidden_role_policies: dict[str, dict[str, tuple[str, ...]]] = field(default_factory=dict)


def normalize_signal_name(signal: str, aliases: dict[str, str] | None = None) -> str:
    value = signal.strip().upper().replace(" ", "").replace("-", "")
    if aliases:
        value = aliases.get(value, value)
    return value


def pin_signals(pins: list[PinDef], aliases: dict[str, str] | None = None) -> list[str]:
    return [normalize_signal_name(pin.signal, aliases) for pin in pins]


def connection_pairs(
    connections: list[ConnectionDef],
    aliases: dict[str, str] | None = None,
) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for connection in connections:
        left = normalize_signal_name(connection.left_signal, aliases)
        right = normalize_signal_name(connection.right_signal or connection.left_signal, aliases)
        pairs.append((left, right))
    return pairs


def validate_endpoint_schema(label: str, pins: list[PinDef], schema: EndpointSchema) -> None:
    signals = pin_signals(pins)
    signal_set = set(signals)

    if schema.pin_count is not None and len(pins) != schema.pin_count:
        raise ValueError(f"{label}: expected {schema.pin_count} pins for {schema.family}, got {len(pins)}")

    missing = [signal for signal in schema.required_signals if signal not in signal_set]
    if missing:
        raise ValueError(f"{label}: missing required signals for {schema.family}: {', '.join(missing)}")

    if schema.allowed_signals is not None:
        allowed = set(schema.allowed_signals)
        unknown = [signal for signal in signals if signal not in allowed]
        if unknown:
            raise ValueError(f"{label}: unknown signals for {schema.family}: {', '.join(unknown)}")

    if schema.exact_signals is not None:
        exact = set(schema.exact_signals)
        extras = [signal for signal in signals if signal not in exact]
        missing_exact = [signal for signal in schema.exact_signals if signal not in signal_set]
        if extras or missing_exact:
            detail = []
            if extras:
                detail.append(f"extras: {', '.join(extras)}")
            if missing_exact:
                detail.append(f"missing: {', '.join(missing_exact)}")
            raise ValueError(f"{label}: signal set mismatch for {schema.family} ({'; '.join(detail)})")

    if schema.pin_map is not None:
        actual_by_pin = {str(pin.pin): normalize_signal_name(pin.signal) for pin in pins}
        expected_by_pin = {str(pin): normalize_signal_name(signal) for pin, signal in schema.pin_map}

        missing_pins = [pin for pin in expected_by_pin if pin not in actual_by_pin]
        extra_pins = [pin for pin in actual_by_pin if pin not in expected_by_pin]
        mismatches = [
            f"{pin}: expected {expected_by_pin[pin]}, got {actual_by_pin[pin]}"
            for pin in expected_by_pin
            if pin in actual_by_pin and expected_by_pin[pin] != actual_by_pin[pin]
        ]
        if missing_pins or extra_pins or mismatches:
            detail = []
            if missing_pins:
                detail.append(f"missing pins: {', '.join(sorted(missing_pins, key=str))}")
            if extra_pins:
                detail.append(f"extra pins: {', '.join(sorted(extra_pins, key=str))}")
            if mismatches:
                detail.append(f"mismatches: {'; '.join(mismatches)}")
            raise ValueError(f"{label}: pin map mismatch for {schema.family} ({'; '.join(detail)})")


def validate_harness_schema(
    left_label: str,
    left_pins: list[PinDef],
    right_label: str,
    right_pins: list[PinDef],
    connections: list[ConnectionDef],
    schema: HarnessSchema,
) -> None:
    validate_endpoint_schema(left_label, left_pins, schema.left)
    validate_endpoint_schema(right_label, right_pins, schema.right)

    aliases = schema.aliases
    left_signals = set(pin_signals(left_pins, aliases))
    right_signals = set(pin_signals(right_pins, aliases))
    pairs = connection_pairs(connections, aliases)

    seen_left: set[str] = set()
    seen_right: set[str] = set()
    for left_signal, right_signal in pairs:
        if left_signal not in left_signals:
            raise ValueError(f"{schema.name}: connection references missing left signal {left_signal}")
        if right_signal not in right_signals:
            raise ValueError(f"{schema.name}: connection references missing right signal {right_signal}")
        if left_signal in seen_left:
            raise ValueError(f"{schema.name}: duplicate connection from left signal {left_signal}")
        if right_signal in seen_right:
            raise ValueError(f"{schema.name}: duplicate connection to right signal {right_signal}")
        seen_left.add(left_signal)
        seen_right.add(right_signal)

    missing_pairs = [
        f"{left}->{right}"
        for left, right in schema.required_connections
        if (normalize_signal_name(left, aliases), normalize_signal_name(right, aliases)) not in pairs
    ]
    if missing_pairs:
        raise ValueError(f"{schema.name}: missing required connections: {', '.join(missing_pairs)}")

    if schema.forbid_unconnected_signals:
        ignored = {normalize_signal_name(signal, aliases) for signal in schema.ignored_signals}
        unconnected_left = sorted(signal for signal in left_signals - seen_left if signal not in ignored)
        unconnected_right = sorted(signal for signal in right_signals - seen_right if signal not in ignored)
        if unconnected_left or unconnected_right:
            detail = []
            if unconnected_left:
                detail.append(f"left unconnected: {', '.join(unconnected_left)}")
            if unconnected_right:
                detail.append(f"right unconnected: {', '.join(unconnected_right)}")
            raise ValueError(f"{schema.name}: unconnected required signals ({'; '.join(detail)})")


def validate_bus_schema(participants: list[BusParticipant], schema: BusSchema) -> None:
    role_counts = {role: 0 for role in schema.roles}

    for participant in participants:
        endpoint_schema = schema.roles.get(participant.role)
        if endpoint_schema is None:
            allowed = ", ".join(sorted(schema.roles))
            raise ValueError(f"{schema.name}: unknown role {participant.role} for {participant.label} (allowed: {allowed})")

        validate_endpoint_schema(participant.label, list(participant.pins), endpoint_schema)
        role_counts[participant.role] = role_counts.get(participant.role, 0) + 1

        _validate_policy_value(schema.name, participant.label, "shield_policy", participant.shield_policy, schema.shield_values)
        _validate_policy_value(schema.name, participant.label, "drain_policy", participant.drain_policy, schema.drain_values)
        _validate_policy_value(
            schema.name,
            participant.label,
            "termination_policy",
            participant.termination_policy,
            schema.termination_values,
        )
        _validate_policy_value(schema.name, participant.label, "bias_policy", participant.bias_policy, schema.bias_values)
        _validate_policy_value(schema.name, participant.label, "pullup_policy", participant.pullup_policy, schema.pullup_values)
        _validate_policy_value(schema.name, participant.label, "poe_policy", participant.poe_policy, schema.poe_values)

        required = schema.required_role_policies.get(participant.role, {})
        forbidden = schema.forbidden_role_policies.get(participant.role, {})
        _validate_policy_requirements(schema.name, participant, required, forbidden)

    for role, minimum in schema.min_role_counts.items():
        count = role_counts.get(role, 0)
        if count < minimum:
            raise ValueError(f"{schema.name}: role {role} requires at least {minimum} participant(s), got {count}")

    for role, maximum in schema.max_role_counts.items():
        count = role_counts.get(role, 0)
        if maximum is not None and count > maximum:
            raise ValueError(f"{schema.name}: role {role} allows at most {maximum} participant(s), got {count}")


def _validate_policy_value(
    schema_name: str,
    label: str,
    field_name: str,
    value: str,
    allowed_values: tuple[str, ...],
) -> None:
    if value not in allowed_values:
        allowed = ", ".join(allowed_values)
        raise ValueError(f"{schema_name}: {label} uses unsupported {field_name}={value} (allowed: {allowed})")


def _validate_policy_requirements(
    schema_name: str,
    participant: BusParticipant,
    required: dict[str, tuple[str, ...]],
    forbidden: dict[str, tuple[str, ...]],
) -> None:
    for field_name, allowed_values in required.items():
        value = getattr(participant, field_name)
        if value not in allowed_values:
            allowed = ", ".join(allowed_values)
            raise ValueError(
                f"{schema_name}: {participant.label} role {participant.role} requires {field_name} in {{{allowed}}}, got {value}"
            )

    for field_name, banned_values in forbidden.items():
        value = getattr(participant, field_name)
        if value in banned_values:
            banned = ", ".join(banned_values)
            raise ValueError(
                f"{schema_name}: {participant.label} role {participant.role} forbids {field_name} in {{{banned}}}"
            )
