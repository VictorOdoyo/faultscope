# Transformer Delta Yg: LL

The circuit isolates transformer delta yg for a LL fault at bus fault. Fault impedance is [0.0, 0.0] pu with the project's explicit type-specific definition. Expected phase currents and every bus phase voltage come from a separate full phase-domain modified nodal solve. Fault constraints are imposed directly in ABC coordinates: phase-to-ground, phase-to-phase, or two joined phases through a common ground impedance. The oracle never calls the production closed-form sequence fault boundary.

The augmented equation residual is 7.161e-15 pu. Current tolerance is 2e-5 A; voltage tolerance is 2e-8 pu. The floating zero mode is retained and its reference is fixed only as permitted by the fault constraint. These are synthetic engineering verification circuits, not observed utility measurements or a claim of standard certification.

Run `python -m unittest tests.test_reference_transformer_delta_yg_ll`. Data: `benchmarks/transformer_delta_yg_ll.json`.
