# Equivalent-source screening and standard boundary

The screening action scales the three-phase reference voltage by a user c factor, calculates initial symmetrical RMS current, and estimates peak current using `kappa=1.02+0.98 exp(-3R/X)` and `ip=sqrt(2) kappa Ik`. The thermal number is a constant-RMS `Ik² duration`, not an IEC decrement-adjusted thermal equivalent. A pure-reactance DC time constant is reported null because it is unbounded in this idealized model.

The selected reference context is **IEC 60909-0:2016**, but this is explicitly an incomplete single-equivalent screening method. Equipment/source correction factors, meshed-network peak methods, breaking-current time behavior and converter-specific rules are absent. It must not be presented as a complete IEC/ANSI-compliant short-circuit calculation. Classical fault phasors remain separately available and do not silently receive a c factor.
