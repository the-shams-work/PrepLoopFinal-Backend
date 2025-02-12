from __future__ import annotations

from enum import Enum

__all__ = ("Duration", "InterviewFlag")


class Duration(Enum):
    _1week = 604800
    _2week = 1209600
    _3week = 1814400
    _4week = 2419200


class InterviewFlag(str, Enum):
    GUIDED = "guided"
    PRACTICE = "practice"
