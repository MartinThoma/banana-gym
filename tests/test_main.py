#!/usr/bin/env python

# Core Library
import unittest

# Third party
import gym

# First party
import gym_banana  # noqa


class Environments(unittest.TestCase):
    def test_env(self):
        env = gym.make("Banana-v0")
        env.seed(0)
        env.reset()
        env.step(0)
