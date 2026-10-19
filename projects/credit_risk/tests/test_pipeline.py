import numpy as np
import pandas as pd

from src.data import make_portfolio
from src.features import add_features
from src.metrics import ks_statistic, pd_to_score, psi
from src.train import time_split


def test_time_split_has_no_overlap_and_is_ordered():
    tr, va, te = time_split(make_portfolio(5000))
    assert tr.vintage.max() < va.vintage.min() <= va.vintage.max() < te.vintage.min()


def test_features_do_not_touch_target():
    df = make_portfolio(500)
    flipped = df.assign(default_12m=1 - df.default_12m)
    pd.testing.assert_frame_equal(add_features(df).drop(columns="default_12m"),
                                  add_features(flipped).drop(columns="default_12m"))


def test_psi_zero_for_same_and_large_for_shift():
    x = np.random.default_rng(0).normal(size=5000)
    assert psi(x, x) < 1e-6
    assert psi(x, x + 1.5) > 0.25


def test_ks_perfect_and_random():
    y = np.array([0] * 50 + [1] * 50)
    assert ks_statistic(y, y.astype(float)) == 1.0
    r = np.random.default_rng(0)
    assert ks_statistic(r.integers(0, 2, 5000), r.random(5000)) < 0.1


def test_score_decreases_with_pd():
    s = pd_to_score(np.array([0.01, 0.05, 0.2]))
    assert s[0] > s[1] > s[2]
    assert abs(pd_to_score(np.array([1 / 51]))[0] - 600) < 1e-6   # odds 50:1 -> base score
