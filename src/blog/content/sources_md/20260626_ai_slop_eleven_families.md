# Eleven Families of AI Code Slop

This is the second of two posts on AI code slop. The first covered why AI-generated code fails differently from human-written code, and why some traditional quality signals have started pointing the wrong direction. This one is the practical companion: what slop actually looks like, organized by the kind of damage it does.

These families came from surveying 70+ AI code quality tools, selecting 42 for deep rule analysis, and cataloging 575 individual rules. Each family groups patterns by what they break in the codebase. I'm including the best code example I found for each.

## 1. Hygiene Debris

Leftovers from the generation process that should have been cleaned before commit. Unused imports, dead functions, debug logging, commented-out code, ephemeral planning files like `PLAN.md` and `SCRATCH.md`.

Models generate artifacts as part of solving a task but don't track whether those artifacts end up wired into the final solution. There's no feedback signal when something goes unused, so over many sessions these leftovers accumulate silently. One project accumulated 11,903 lines of dead code in 7 months, including entire orphaned extension subsystems for Telegram, Signal, Matrix, and iMessage.

This is the most statically detectable family. About 33 of 37 rules need no LLM at all: just AST analysis, module graphs, and pattern matching.

## 2. Annotation Noise

Comments that add no information beyond what the code already says.

```python
# Check for missing, null, or empty type
if exposure_type is None or (isinstance(exposure_type, str) and exposure_type == ""):
    ...

# Get the allowed set for this type
allowed_fields = {
    "Gateway": gateway_allowed,
    "DirectPort": directport_allowed,
    "Balancer": balancer_allowed,
}.get(exposure_type, set())
```

Both comments restate what the next line does. This isn't under-documented code. It's code with extra text because the model writes in explanation mode. Models can't distinguish contexts where comments add value (non-obvious business logic, API contracts) from contexts where they restate the code.

One team built a compiled Go binary that fires on every file write to intercept narrator comments in real time. Another went through a five-month escalation, eventually concluding that "cleanup" framing enables write-now-delete-later behavior. They reframed to "do not write in the first place."

## 3. Redundant Guarding

Runtime guards that duplicate guarantees the type system or call context already provides.

```python
config.get("database", {}).get("host", {}).get("primary", "localhost")
```

When the dict structure is known from the caller, this fallback chain is pure noise. Models produce guards as part of "careful code" without tracking whether the guarantee already exists. Defensive programming was a positive signal in training data, so the model keeps producing it regardless.

Detection requires type checker integration, making this harder to clean automatically than the first two families.

## 4. Structural Bloat

The largest family at 102 rules. Unnecessary wrappers, premature abstractions, factories that always return the same thing, over-fragmented file structures.

Models produce structure because training data rewards structure, but humans had a natural brake: creating an abstraction costs effort, so you only do it when the payoff exceeds the cost. Models have no production cost. They create a helper for every operation, an interface for every class, a wrapper for every boundary.

The classic example: a single-implementation interface where `AbstractUserRepository` has exactly one concrete `UserRepository`. Or an async function wrapping a synchronous call with no internal await. One project's AGENTS.md captures the right instinct: "New helpers and files must pay rent immediately."

## 5. Duplication by Regeneration

Models don't copy-paste. When a model needs a helper that already exists, it writes a new one from scratch. The result is functionally identical code that's syntactically different, which traditional clone detectors miss entirely.

One project explicitly bans this in their AGENTS.md: "NEVER create local `formatAge`, `formatDuration`, `formatElapsedTime` functions." That ban exists because agents kept creating them. The root cause is simple: humans remember what they've already written. Models don't. Each invocation starts fresh.

## 6. Test Slop

Tests that exist to pass rather than to catch bugs.

```python
def test_calculate_tax():
    amount = 100
    rate = 0.15
    expected = amount * rate  # same formula as the implementation
    assert calculate_tax(amount, rate) == expected
```

This is circular verification: the test recomputes the expected value using the same formula as the production code, so it can never fail. When a test fails, the cheapest path to green is weakening the test rather than fixing the code, and models have no feedback signal that distinguishes these two actions.

Other patterns: zero-assertion tests, tests that mock the unit under test itself, and `@pytest.mark.skip` where the agent disabled the test rather than fixing the underlying failure. One project treats weakened test expectations as a violation triggering mandatory halt.

## 7. Integrity and Fake-Done

Agent output that misrepresents the state of the work.

```python
def enforce_rate_limit(user_id: str, action: str) -> bool:
    """Return whether the user is allowed to perform this action."""
    # TODO: integrate with Redis-backed limiter
    return True
```

This isn't just an incomplete TODO. The damaging part is the executable success path: callers can now build on a function that claims to enforce a policy but silently permits every request.

This family also includes cross-language leakage:

```python
results = []
items.forEach(lambda item: results.push(normalize(item)))
```

JavaScript Array methods leaked into Python. The code *looks* like it could work, which is exactly what makes it dangerous.

This is the hardest family to mitigate. Even the deepest prevention system I surveyed, with three converging skills and verification requirements, has documented failures where agents fabricate entire verification dialogues.

## 8. Error-Swallowing

Mechanisms that suppress or silently discard error signals. Detected by 18 tools, the strongest convergence signal in the survey.

```python
try:
    type_class = getattr(builtins, type_name)
    for name in dir(type_class):
        ...
except Exception:
    pass
return attributes
```

Models reproduce the *form* of error handling without the *substance*. A catch block that returns a default looks identical to robust error handling in training data, even though at runtime it silently swallows the error. The same checkpoint that produced this had 35 swallowed-exception findings versus 11 in the reference solution.

Detection is heavily static: empty catch bodies, broad exception types, `_ = err` patterns. One of the easiest families to detect deterministically.

## 9. Type Laxity

Type system escape hatches.

```typescript
const result = response.data as unknown as UserProfile;
```

The double-cast `as unknown as X` is a pattern nearly exclusive to AI generation. In agentic workflows, type errors block the generation loop. `as any` or `as unknown as X` unblocks immediately, so models that optimize for compilable output converge on escape hatches. Nine tools detect unsafe type assertions, making it one of the most agreed-upon patterns.

## 10. Kinetic Slop

The agent does more than was asked. Scope creep, drive-by edits to unrelated code, bundled refactoring, formatting changes mixed with functional changes.

This is harder to demonstrate with a code example because it's about diff scope rather than any single pattern. The test is lineage: every modified line must trace to the user's request. If it doesn't, revert it. One project tracks net LOC growth as a slop signal. Another enforces "touch only what was asked" at the harness level rather than relying on the model's self-restraint.

## 11. Naming Drift

Names that obscure meaning, break project conventions, or signal AI generation.

```python
def process_data(input_data):
    result = helper_1(input_data)
    temp = helper_2(result)
    return temp
```

`process_data`, `handle_response`, `get_result`, `do_thing`. Models produce names drawn from the average of training data rather than matching the conventions of the project. The result is generic names that compile and work but carry no domain meaning. The opposite tendency also appears: over-verbose names like `currentUserAuthenticationStatusBoolean` where `isAuthenticated` would do.

## The Common Thread

Every family is a different surface where the same fundamental property shows up: models optimize for plausible output rather than durable code. Comments that look helpful, tests that look thorough, structure that looks professional, error handling that looks robust. The code *looks right* because the model is optimized to produce text that looks right. Whether it serves the project is a question the model has no mechanism to answer.

These families fall into three tooling modes. Some can be cleaned deterministically (hygiene debris, annotation noise, obvious error-swallowing, shallow integrity stubs). Some need an LLM or human to judge whether the fix is correct (structural bloat, semantic duplication, deep integrity violations). And some are better prevented than cleaned (kinetic slop, test weakening, regenerated duplication). A useful system needs all three.
