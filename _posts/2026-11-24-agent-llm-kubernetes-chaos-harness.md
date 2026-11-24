---
title: "Tracing a Kubernetes Chaos Test Through a Python State Machine"
date: "2026-11-24"
categories: ["Software Engineering", "Agent Systems"]
tags: ["python", "kubernetes", "etcd", "llm-agents", "state-machines", "observability"]
excerpt: "A Python chaos harness injects etcd faults, constrains an LLM caller with state machines, and prints the redacted agent–LLM conversation with --verbose. One run also exposed a verifier gap."
---

*Audience: you can read Python and know basic Kubernetes vocabulary. No chaos-engineering or agent-framework experience needed.*

At the end of one run, every etcd member passed the final health check. The harness scored that run zero on `strict_loop_success`.

The run was one of four against a lab Kubernetes cluster. A Python harness injected a wrong registered peer URL on `vm2`, then asked a local model served by Ollama to diagnose and repair it. The model never produced the correct diagnosis, never received a gate receipt, and left the fault in place. Verification still printed `etcd healthy: 3/3 members, quorum 2`.

That was a verifier defect, not a subtle scoring choice. `cluster/verify_etcd_healthy.sh` checks Ready nodes, running etcd pods, member count, and local endpoint health. It does not compare the registered peer URL with the intended topology. The strict metric caught the bad path anyway; the older `loop_success` metric can be inflated by this scenario because it only needs a correct diagnosis, passing verification, and a repair-shaped record.

I fixed the verifier after finding this: the runner now reuses the fault-present predicate after the agent loop and requires the fault to be cleared as part of verification. The harness can also print the agent–LLM exchange with `./chaos run --verbose`; the output is redacted and tied to the run ID, so the conversational side is visible while the run is live. The tracing, scoring, and guard behavior below come from the original run; the verifier fix is the change that run prompted.

## Setup and provenance

The numbers in this post come from `results.sqlite3`, not from a demo script.

| Field | Value |
| --- | --- |
| Run | `etcd-wrong-peer-url-ollama-0-441a4807` |
| Backend / model | `ollama` / `qwen3.8:27b` |
| Quantization | not recorded |
| Harness SHA | `88d122adb7fe875fabcb58413df08dab80ac0a6e` |
| Prompt hash | not recorded |
| Temperature / seed | `0.2` / `0` (seed is metadata, not a sampler control) |
| Scenario hash | `62a62f30baa7f8f7146aa3f4e2399e41a4a2933dba16cd02f102068056e90f2c` |
| Topology hash | `29e67a5cab5a263103f3a8b42412587e2109a29855ecd9d84cc7a2a9c4465058` |

The four runs used the same model, backend, and one attempt per scenario. Run-era code excerpts link to `88d122a`; the verbose tracing excerpt links to `fae1375`.

## The traced run

The event log is the source of truth. The gate phase column below is folded from the stored `gate.*` events; non-gate rows leave it unchanged. These are real rows from `trace_events`.

| seq | event | detail | gate phase: before -> after |
| --- | --- | --- | --- |
| 3 | `reset` | `ok=true` | `await_diagnosis` -> `await_diagnosis` |
| 4 | `baseline` | `ok=true`, 3-member quorum | `await_diagnosis` -> `await_diagnosis` |
| 5 | `inject` | wrong peer URL on `vm2` | `await_diagnosis` -> `await_diagnosis` |
| 6 | `fault_check` | `present=true`, target `vm2` | `await_diagnosis` -> `await_diagnosis` |
| 35 | `gate.nudge` | `kind=budget`, `step=4` | `await_diagnosis` -> `await_diagnosis` |
| 38 | `gate.diagnosis_submitted` | `label=no_fault`, `correct=false`, attempt 1 | `await_diagnosis` -> `await_diagnosis` |
| 63 | `gate.diagnosis_submitted` | `label=etcd_member_unreachable`, `correct=false`, attempt 2 | `await_diagnosis` -> `escalated` |
| 86 | `run.agent_done` | `gate_terminal=escalated`, `gate_reason=budget_tokens` | `escalated` -> `escalated` |
| 87 | `verify_started` | timeout 300 | `escalated` -> `escalated` |
| 88 | `verify` | `ok=true`, `etcd healthy: 3/3 members, quorum 2` | `escalated` -> `escalated` |
| 90 | `record` | `verify_ok=true`, `strict_loop_success=false` | `escalated` -> `escalated` |

The truth was `etcd_config_error`. The second diagnosis attempt consumed the allowed attempts, so the gate moved to `escalated`. No repair was proposed or executed. The health check then ran and passed, because it never inspected the field that the fault had changed.

The two diagnosis-policy violations are also real. `submit_diagnosis` was denied twice with `violation_kind="diagnosis"`; the scorer counts both denials, which is why `scores.policy_violations` is `2` for this run.

## Finding and fixing the verifier gap

The final verifier does useful work. It waits for Ready nodes, running etcd pods, the expected member count, and healthy endpoints. The last lines of [cluster/verify_etcd_healthy.sh](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/cluster/verify_etcd_healthy.sh) make its contract explicit:

```bash
if [[ "$member_count_ok" != "true" ]]; then
  echo "could not confirm $EXPECTED etcd members from any pod" >&2
  exit 1
fi
...
echo "etcd healthy: $EXPECTED/$EXPECTED members, quorum $QUORUM"
```

Those checks cannot distinguish a repaired peer URL from the wrong one injected by this scenario. The fault-present predicate already knew the difference: the stored artifact said `registered peer URL is https://10.2.0.4:2399`. The fix runs that same predicate after the agent loop and folds the result into `verify_ok`:

```python
        if scenario is not None:
            fault_cleared, fault_detail = fault_checks.check_fault_cleared(
                scenario, targets or [], env=spec.run_env,
            )
            suffix = f"FAULT CLEARED: {fault_detail}"
            output = f"{output}\n{suffix}" if output else suffix
        return cls(
            ok=health_ok and fault_cleared,
            output=output,
            fault_cleared=fault_cleared,
            fault_detail=fault_detail,
        )
```

A no-op calibration test now covers every fault scenario: health command passes, the fault predicate still reports the fault present, and final verification must fail. Live destructive no-op calibration on the cluster is still a separate operator task; the test does not touch infrastructure.

The design lesson is narrower than "trust the scorer". Use the same invariant before and after the agent acts. If the pre-agent check can see a fault, the post-agent verifier must fail while that fault remains.

## Scenario and preflight

A prompt is a poor place to define operational policy. The harness starts with a scenario file. [scenarios/etcd-member-down.json](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/scenarios/etcd-member-down.json) is a representative example, abridged here:

```json
{
  "id": "etcd-member-down",
  "root_cause": "etcd_member_unreachable",
  "target_nodes": ["second"],
  "avoid_local_target": true,
  "acceptable_repairs": ["restart_member"],
  "forbidden_repairs": ["full_cluster_reset"],
  "inject": "faults/etcd_member_down.sh \"$TARGET_NODE\"",
  "verify": "cluster/verify_etcd_healthy.sh",
  "timeout_seconds": 300,
  "fault_present_timeout_seconds": 60,
  "risk": "disruptive",
  "impact_class": "single_member_fault"
}
```

`root_cause` is hidden truth. `target_nodes` is resolved against a frozen topology snapshot, so `second` means the second eligible control plane, not a literal hostname. `acceptable_repairs` and `forbidden_repairs` are repair policy. `risk` and `impact_class` are validated and used by the CLI and capability checks; they are metadata, not a second authorization layer.

The runner discovers topology, applies the destructive guard, checks capability, and validates resolved target names before any fault command runs. The guard in [tools/safety.py](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/tools/safety.py) accepts either an allow-listed kubectl context or cluster ID, and checks a topology hash only when a topology allow-list is configured. Resolved names are matched against `^[A-Za-z0-9][A-Za-z0-9_.-]*$` before scenario commands expand them through a shell.

Everything after that follows one order:

```text
validate scenario -> discover + freeze topology -> safety guard
   -> reset -> baseline verify -> inject fault -> fault-present check
        -> agent loop (diagnose -> repair, gated)
             -> final verify -> record + score
```

`_run_fresh` executes those stages in [run_benchmark.py](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/run_benchmark.py). Reset restores clean etcd state, baseline verification proves the cluster was healthy first, injection applies the fault, and `fault_checks.wait_for_fault` proves the intended stimulus was observed. Each stage has its own end reason: `reset_failed`, `baseline_failed`, `injection_failed`, or `fault_not_observed`. Those runs are excluded from headline scoring. A reset failure must not claim the baseline passed, so `baseline_ok` now starts as `False` and is set only when the baseline command actually runs.

The model is invoked only after all four checks pass.

## Machines and the model loop

Scenario files say which repair is acceptable. They do not say whether a repair is legal before a diagnosis. The gate machine in [harness/machines/gate.py](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/harness/machines/gate.py) supplies that order.

| Phase | Event | Outcome |
| --- | --- | --- |
| `AWAIT_DIAGNOSIS` | repair proposed | stays put, records `PREMATURE_REPAIR` |
| `AWAIT_DIAGNOSIS` | repair finished | rejected |
| `APPROVED` | repair proposed, forbidden | stays `APPROVED`, records `FORBIDDEN_REPAIR` |
| `APPROVED` | repair proposed, not acceptable | stays `APPROVED`, records `UNACCEPTABLE_REPAIR` |
| `APPROVED` | repair proposed, acceptable | marks the repair proposed |

One transition from the table:

```python
    (GatePhase.AWAIT_DIAGNOSIS, GateEvent.REPAIR_PROPOSED): Transition(
        GateState(),
        (_effect(EffectKind.RECORD_VIOLATION, violation=GateViolation.PREMATURE_REPAIR.value),),
        update=_violation_update(GateViolation.PREMATURE_REPAIR),
    ),
```

An illegal call becomes a recorded rejection, not an unlogged change to state. Escalation is a terminal phase, which lets the harness stop cleanly when the diagnosis budget is exhausted.

The model sees a narrow interface. [harness/prompt.py](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/harness/prompt.py) includes these constraints:

```text
Read-only investigation tools are safe to call at any time. Submit a diagnosis with submit_diagnosis before any repair.
root_cause MUST be exactly one of: {', '.join(ROOT_CAUSE_LABELS)}. Do not write a sentence, a node name, or an explanation in root_cause.
If the diagnosis is accepted, the harness gate is open internally; do not pass receipts or approval tokens to repair calls.
submit_diagnosis accepts at most two attempts. If rejected, gather one new decisive observation before the final attempt; do not brute-force labels.
```

The gate receipt is a correctness handshake derived from folded state. It is not passed as a tool argument and is not the authorization boundary; the gate rules and scenario repair policy are.

`harness/loop.py` calls the model with tool schemas at temperature `0.2`, binds each returned call to a registered tool, and journals the execution. If the model stops without diagnosing, the harness nudges it. If it exhausts the budget, the run ends with a specific reason. The model proposes calls; Python decides what they mean.

## Printing the Agent–LLM conversation

The event log is the durable record. It is not a live debugging view. The runner now has a `--verbose` switch that prints the Agent–LLM exchange as it happens. `chaos_cli.py` forwards the flag to `run_benchmark.py`, which stores it on `ExperimentSpec.verbose`; [harness/loop.py](https://github.com/ratulb/k8s-chaos-harness/blob/fae13756a7013fcf6269e60339a1964cc78b7033/harness/loop.py) uses that field to decide whether to print.

```python
if spec.verbose:
    for message in messages[printed_messages:]:
        _print_llm_message("request", budget.steps, message.to_dict())
```

```python
if spec.verbose:
    _print_llm_message("response", budget.steps, msg.to_dict())
printed_messages = len(messages)
```

Each line goes through the same redaction helper used by the journal:

```python
def _print_llm_message(direction: str, step: int, message: dict[str, Any]) -> None:
    payload = Message.redact_payload(message)
    print(
        f"[llm {direction} {step}] {json.dumps(payload, sort_keys=True, default=str)}",
        flush=True,
    )
```

The `printed_messages` offset prevents the whole history from being reprinted on every turn. New tool results and nudges appear in the next request batch; responses are printed once when they arrive. Quiet runs print none of it.

This is real output from the mocked control run used by the regression test. The system prompt is the first request; this excerpt starts at the user turn:

```text
=== llm conversation verbose-demo ===
[llm request 1] {"content": "Investigate the Kubernetes cluster for an etcd fault. Diagnose and repair if needed.", "role": "user"}
[llm response 1] {"content": "", "role": "assistant", "tool_calls": [{"function": {"arguments": "{\"root_cause\": \"no_fault\"}", "name": "submit_diagnosis"}, "id": "call-1"}]}
[llm request 2] {"content": "diagnosis accepted; gate approved", "role": "tool", "tool_call_id": "call-1"}
```

The printed exchange explains why the harness does not trust the model with protocol state. The model proposes a `no_fault` label; the gate decides whether it is correct. Verbose output makes that boundary observable without giving the model a new capability.

## Journal and scoring

Events are appended to `trace_events` with a per-run sequence number. Machine events rebuild folded state, and run columns are projections of that state. `replay.py` reads the same rows and renders a static, redacted HTML view; it cannot change a score. Event sourcing is a standard pattern for keeping a replayable history [2].

Scoring reads the folded run state and the gate path. [common/scoring.py](https://github.com/ratulb/k8s-chaos-harness/blob/88d122adb7fe875fabcb58413df08dab80ac0a6e/common/scoring.py) keeps `loop_success` for historical comparison, but the headline is `strict_loop_success`:

```python
        strict = bool(
            fault_present
            and run_state.get("status") == "finished"
            and run_state.get("phase") == "finished"
            and gate_path.terminal in STRICT_TERMINALS
            and (gate_path.terminal != "repaired" or "approved" in gate_path.visited)
            and gate_path.first_attempt_correct
            and gate_path.receipt_issued
            and verify_ok
            and not violations
            and reason == STRICT_END_REASON
            and reason not in BUDGET_END_REASONS
            and not is_excluded(record)
            and not forbidden
            and repair_acceptable
            and (gate_path.repair_executed if not no_fault else not gate_path.repair_proposed)
        )
```

For the traced run, `fault_present`, `status`, and `phase` pass. The first failing condition is `gate_path.terminal in STRICT_TERMINALS`: the phase is `escalated`, not `repaired`. Later conditions fail too: the first attempt was wrong, no gate receipt was issued, and the reason was `budget_tokens`. The original verifier gap is now closed by the fault-cleared check, so a future health-check pass cannot hide an unrepaired fault.

That is the link between the opening and the score. The trace shows the path; the strict block says which parts of that path count.

## Results

The table below uses raw violation counts from `scores.policy_violations`. It comes from `python3 score.py --db results.sqlite3 --format md`.

| Scenario | Truth -> submitted label | Attempts | Gate receipt | Verify | Violations | Strict | End reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `etcd-member-down` | `etcd_member_unreachable` -> `etcd_member_unreachable` | 1 | yes | pass | 0 | **yes** | `budget_tokens` |
| `etcd-member-wiped` | `etcd_member_data_loss` -> `etcd_member_unreachable` | 1 | no | fail | 1 | no | `budget_tokens` |
| `etcd-quorum-loss` | `etcd_quorum_loss` -> `etcd_member_unreachable` | 2 | no | fail | 2 | no | `budget_tokens` |
| `etcd-wrong-peer-url` | `etcd_config_error` -> `etcd_member_unreachable` | 2 | no | pass | 2 | no | `budget_tokens` |

One of four runs was a strict success. The three failures were diagnosis failures: the model submitted `etcd_member_unreachable` for three different root causes. The wrong-peer-url run also exposed the verifier gap described above. A final health check alone would have hidden that gap; the path-based score did not.

## What this does not show

Four runs on one self-hosted backend are not a model ranking. Each scenario ran once, quantization and prompt hash were not recorded, and the seed was metadata rather than a controlled sampler input. The strict metric is deliberately narrow: it does not grade whether an escalation message was clear, which matters for runs where stopping is the right answer.

The no-op calibration is automated with mocked fault predicates, not run as a live destructive sweep. The harness is destructive, and a live calibration needs an explicitly disposable cluster.

Chaos engineering is the practice of injecting controlled faults to learn how a system behaves [1]. These runs show how one harness keeps that experiment checkable; they do not estimate operational reliability in general.

## Common pitfalls

**Letting the model own the protocol.** If prose decides whether diagnosis happened, there is no stable fact to replay. A named tool call becomes an event, and the transition table decides what it means.

**Treating the gate receipt as authorization.** The receipt marks an accepted diagnosis. Repair safety depends on canonical repair names and scenario policy.

**Verifying a different invariant.** The `etcd-wrong-peer-url` run passed endpoint health while the injected peer URL remained. The same fault predicate must be checked before and after the agent runs.

**Overstating the guard's reach.** `require_destructive_guard` runs in `run_benchmark.py`'s main path. It protects benchmark runs, not someone invoking `faults/*.sh` or `cluster/reset_cluster.sh` by hand.

**Calling pre-agent failures "zero scores."** Those runs are excluded from headline scoring. Their end reason says which infrastructure stage failed.

## Conclusion

The harness separates three questions that a final health check merges: was the fault real, what path did the agent take, and did the fault actually clear. The scenario and preflight answer the first. State machines, named tools, the journal, and `--verbose` output answer the second. The fault-cleared verifier and strict score answer the third.

The LLM is part of the experiment, not the design contract. It supplies candidate labels and tool calls. The harness supplies truth, legal transitions, repair policy, and recorded meaning.

To watch a new run, pass `--verbose` to `./chaos run`. To reproduce the reporting side, run `python3 score.py --db results.sqlite3 --format md` and `./chaos replay --output replay.html`. The code is available at [github.com/ratulb/k8s-chaos-harness](https://github.com/ratulb/k8s-chaos-harness).

> **Warning.** Run the harness only against a disposable lab cluster, and expect it to refuse unless the cluster is allow-listed.

## Appendix: references

[1] [AWS Prescriptive Guidance - Overview of chaos engineering](https://docs.aws.amazon.com/prescriptive-guidance/latest/chaos-engineering-on-aws/overview.html)

[2] [Microsoft Azure Architecture Center - Event Sourcing pattern]: https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
