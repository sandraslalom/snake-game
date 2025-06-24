"""
Snake Game Package

A modernized implementation of the classic Snake game using pygame.
"""

__version__ = "2.0.0"
__author__ = "Snake Game Developer"
__email__ = "developer@example.com"

from .sprites_modernized import Snake, Apple, Direction, Position, Size, Color
from .game_modernized import SnakeGame, GameConfig, GameState

__all__ = [
    "Snake",
    "Apple", 
    "Direction",
    "Position",
    "Size",
    "Color",
    "SnakeGame",
    "GameConfig", 
    "GameState",
]