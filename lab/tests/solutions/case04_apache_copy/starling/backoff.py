# Copyright 2023 The Gustwind Authors
# SPDX-License-Identifier: Apache-2.0
# Modified by Robin Vale in 2026: added full jitter to every delay.

"""Exponential backoff for retrying calls that fail for a moment, with full jitter."""

import random


def delays(base: float = 0.5, cap: float = 30.0, attempts: int = 6) -> list[float]:
    return [random.uniform(0, min(cap, base * 2**n)) for n in range(attempts)]
