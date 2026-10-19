"""Causal impact of a policy change via difference-in-differences.

Scenario: a stricter approval policy is rolled out to a *treated* segment (e.g. self-employed)
at vintage T. Did it lower the default rate, or would it have dropped anyway? DiD compares the
before/after change in treated vs. a control group, assuming parallel trends.

    python -m src.causal
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def simulate_policy(true_effect=-0.015, seed=1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for g, base in [("treated", 0.10), ("control", 0.07)]:     # different levels, same trend
        for t in range(24):
            n = 800
            rate = base + 0.001 * t + (true_effect if (g == "treated" and t >= 12) else 0)
            rows.append(pd.DataFrame(dict(treated=int(g == "treated"), post=int(t >= 12), t=t, y=rng.binomial(1, rate, n))))
    return pd.concat(rows)


def main():
    d = simulate_policy()
    naive = d[(d.treated == 1) & (d.post == 1)].y.mean() - d[(d.treated == 1) & (d.post == 0)].y.mean()
    fit = smf.ols("y ~ treated * post", d).fit(cov_type="HC1")
    est, ci = fit.params["treated:post"], fit.conf_int().loc["treated:post"]
    print(f"Naive before/after change (treated only): {naive:+.4f}  <- confounded by time trend")
    print(f"DiD estimate: {est:+.4f}  95% CI [{ci[0]:+.4f}, {ci[1]:+.4f}]   (true effect: -0.0150)")

    # Placebo / parallel-trends check: fake the policy date inside the pre-period
    pre = d[d.post == 0].assign(post=lambda x: (x.t >= 6).astype(int))
    pl = smf.ols("y ~ treated * post", pre).fit(cov_type="HC1")
    print(f"Placebo DiD (fake policy at t=6): {pl.params['treated:post']:+.4f}, p={pl.pvalues['treated:post']:.2f}  (should be ~0)")


if __name__ == "__main__":
    main()
