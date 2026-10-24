# Sequence-network schema v1

Native JSON uses a common `base_mva`. Bus `base_kv` is the local line-to-line voltage base. Each impedance is `[R,X]` pu on that power base and the appropriate winding voltage base. Neutral impedances use the same local base and enter zero sequence as 3Zn. R and X are nonnegative; zero source/branch series impedance is rejected. Missing z0 is an open zero-sequence path, not zero impedance.

Branches are lines or ideal transformers with series z1/z2/z0, from-side tap magnitude and phase shift. Transformer winding labels are grounded wye Yg, ungrounded wye Y or delta D. Sources have positive-sequence internal EMF, z1/z2, optional grounded z0 and neutral impedance. Buses may have multiple sources. Status is explicit boolean. Equipment duty ratings are independent of the electrical model.
