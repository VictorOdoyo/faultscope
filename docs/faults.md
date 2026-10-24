# Fault boundary definitions

Supported types are balanced three-phase, phase-A-to-ground SLG, B-C line-to-line, and B/C joined at a common ground impedance DLG. In LL, Zf is the total impedance between the two phases. In DLG, both phases meet at a common point whose single Zf goes to ground, so its current is Ib+Ic=3I0. Three-phase Zf is per phase. These definitions avoid the common factor-of-three ambiguity.

The pre-fault positive-sequence voltage drives the closed-form sequence boundary. Compensation columns produce all post-fault bus voltages. A floating zero path makes SLG current zero and makes DLG current reduce to an LL fault, while its phase-to-ground voltage is set by the fault constraint. No unbalanced load model is present; prefault load currents are excluded unless a supplied positive-sequence voltage profile is used as the compensation reference.
