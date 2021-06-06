#!/usr/bin/env python

"""
Simulate the simplifie Banana selling environment.

Each episode is selling a single banana.
"""

# Core Library
import logging.config
import math
import random
from typing import Any, Dict, List, Tuple

# Third party
import cfg_load
import gym
import numpy as np
import pkg_resources
from gym import spaces

path = "config.yaml"  # always use slash in packages
filepath = pkg_resources.resource_filename("gym_banana", path)
config = cfg_load.load(filepath)
logging.config.dictConfig(config["LOGGING"])


def get_chance(x: float) -> float:
    """Get probability that a banana will be sold at price x."""
    e = math.exp(1)
    return (1.0 + e) / (1.0 + math.exp(x + 1))


class BananaEnv(gym.Env):
    """
    Define a simple Banana environment.

    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self) -> None:
        self.__version__ = "0.1.0"
        logging.info(f"BananaEnv - Version {self.__version__}")

        # General variables defining the environment
        self.MAX_PRICE = 2.0
        # This results in TOTAL_TIME_STEPS+1 potential banana sales
        self.TOTAL_TIME_STEPS = 2

        self.curr_step = -1
        self.is_banana_sold = False

        # Define what the agent can do
        # Sell at 0.00 EUR, 0.10 Euro, ..., 2.00 Euro
        self.action_space = spaces.Discrete(21)

        # Observation is the remaining time
        low = np.array([0.0])  # remaining_tries
        high = np.array([self.TOTAL_TIME_STEPS])  # remaining_tries
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory: List[Any] = []

    def step(self, action: int) -> Tuple[List[int], float, bool, Dict[Any, Any]]:
        """
        The agent takes a step in the environment.

        Parameters
        ----------
        action : int

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob : List[int]
                an environment-specific object representing your observation of
                the environment.
            reward : float
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over : bool
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info : Dict
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if self.is_banana_sold:
            raise RuntimeError("Episode is done")
        self.curr_step += 1
        self._take_action(action)
        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.is_banana_sold, {}

    def _take_action(self, action: int) -> None:
        self.action_episode_memory[self.curr_episode].append(action)
        self.price = (float(self.MAX_PRICE) / (self.action_space.n - 1)) * action

        chance_to_take = get_chance(self.price)
        banana_is_sold = random.random() < chance_to_take

        if banana_is_sold:
            self.is_banana_sold = True

        remaining_steps = self.TOTAL_TIME_STEPS - self.curr_step
        time_is_over = remaining_steps <= 0
        throw_away = time_is_over and not self.is_banana_sold
        if throw_away:
            self.is_banana_sold = True  # abuse this a bit
            self.price = 0.0

    def _get_reward(self) -> float:
        """Reward is given for a sold banana."""
        if self.is_banana_sold:
            return self.price - 1
        else:
            return 0.0

    def reset(self) -> List[int]:
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation: List[int]
            The initial observation of the space.
        """
        self.curr_step = -1
        self.curr_episode += 1
        self.action_episode_memory.append([])
        self.is_banana_sold = False
        self.price = 1.00
        return self._get_state()

    def _render(self, mode: str = "human", close: bool = False) -> None:
        return None

    def _get_state(self) -> List[int]:
        """Get the observation."""
        ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        return ob

    def seed(self, seed: int) -> None:
        random.seed(seed)
        np.random.seed
