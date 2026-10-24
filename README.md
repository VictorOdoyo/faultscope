# FaultScope

**Traceable sequence-network fault analysis, with explicit grounding and current contributions.**

[![CI](https://github.com/VictorOdoyo/faultscope/actions/workflows/ci.yml/badge.svg)](https://github.com/VictorOdoyo/faultscope/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776ab)](https://www.python.org/)
[![MIT](https://img.shields.io/badge/license-MIT-b5dfbb)](LICENSE)

FaultScope provides a reusable NumPy engineering library, JSON CLI and local browser workbench. Numerical results preserve model assumptions, equations or timing conventions, version, UTC timestamp, input hash and options. Source code, independent reference fixtures and engineering notes are reviewable together.

## Start

```sh
git clone https://github.com/VictorOdoyo/faultscope.git
cd faultscope
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
python -m faultscope serve
```

Open **http://127.0.0.1:8768**. Choose an example, edit an element or native model JSON, inspect the visible study options, and run. Model edits validate before applying and invalidate previous exports. Undo retains 30 snapshots. Export native model JSON separately from complete study JSON, or print a report with your browser. Drafts remain in browser local storage; exported files are durable records.

## Capabilities

- Three-phase, phase-A SLG, B-C LL and common-ground B/C DLG faults with explicit fault impedance.
- Positive/negative/zero-sequence networks, complex taps, grounded neutrals and grounded-wye/delta zero-sequence paths.
- Floating zero-sequence components with fault-imposed neutral displacement, without artificial grounding.
- Fault-bus driving-point impedances, source increments and total/incremental currents at both branch terminals.
- No-load source-driven pre-fault voltage or an explicit imported GridFlow positive-sequence profile.
- Bus fault scans and equipment rating comparisons with unsupported quantities left null.
- Separately named equivalent-source c-factor, peak and constant-current thermal screening; complete IEC/ANSI compliance is not claimed.

## Python and CLI

```python
from faultscope.cli import load_case
from faultscope.studies import run

model = load_case("example:sequence_asymmetry")
result = run(model)
print(result["fault"])
```

```sh
python -m faultscope examples
python -m faultscope study example:sequence_asymmetry
python -m faultscope study model.json --action scan --output study.json
python -m unittest discover -s tests -v
```

The [schema](docs/schema.md), [CLI](docs/cli.md), [study actions](docs/studies.md) and [local HTTP contract](docs/http.md) document units and errors. See [fault definitions](docs/faults.md), [zero-sequence paths](docs/zero_sequence.md) and [screening limits](docs/screening.md).

## Independent verification

**60 reference fixtures** each have checked-in expected values, a dedicated regression and an engineering note. Fifteen electrical conditions cross four fault types. Expected values come from a separate full ABC modified-nodal formulation with explicit phase fault constraints; it does not use the production closed-form sequence fault equations. Analytical and integration tests additionally check floating grounding, sequence transforms, contribution conventions, standard-screen boundaries, CLI and HTTP behavior.

These are synthetic verification circuits/characteristics, not laboratory certification. See [validation methodology](docs/validation.md), [fixtures](benchmarks) and the independent generator in tools/. Normal tests need only NumPy and never regenerate expected values from the implementation under test.

## Scope and limitations

This is a classical linear RMS sequence-network tool. It does not model unbalanced pre-fault loads, time-varying generator decrement, inverter control, transformer saturation, mutual zero-sequence circuits or line charging. Winding models use idealized zero-sequence paths. The screening action is explicitly incomplete relative to IEC 60909-0:2016: correction factors, meshed peak methods and breaking-current time behavior are not implemented. Equipment comparisons are screening proxies, not certified switchgear selection.

The standard-library server binds to loopback for a trusted local workstation. It is not hardened internet hosting. Dense numerical matrices and bounded study sizes target small/medium reviewable engineering studies. Consult the [engineering references](docs/references.md) and relevant manufacturer/standard documents for actual equipment applications.

MIT licensed. Created by Victor Odoyo. Related repositories: [PowerCalcs](https://github.com/VictorOdoyo/powercalcs), [GridFlow](https://github.com/VictorOdoyo/gridflow), [PhaseLab](https://github.com/VictorOdoyo/phaselab).
