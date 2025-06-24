"""
Modern Snake Game Sprites Module

This module contains the modernized sprite classes for the Snake game,
implementing modern Python practices including type hints, enums, and dataclasses.
"""

from __future__ import annotations
import pygame
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random


@dataclass
class Position:
    """Represents a 2D position with x and y coordinates."""
    x: int
    y: int
    
    def __iter__(self):
        """Allow unpacking as tuple."""
        return iter((self.x, self.y))
    
    def __getitem__(self, index: int) -> int:
        """Allow indexing like a tuple."""
        return (self.x, self.y)[index]


@dataclass
class Size:
    """Represents 2D dimensions with width and height."""
    width: int
    height: int
    
    def __iter__(self):
        """Allow unpacking as tuple."""
        return iter((self.width, self.height))


@dataclass
class Color:
    """Represents RGB color values."""
    red: int
    green: int
    blue: int
    
    def __iter__(self):
        """Allow unpacking as tuple."""
        return iter((self.red, self.green, self.blue))
    
    def __getitem__(self, index: int) -> int:
        """Allow indexing like a tuple."""
        return (self.red, self.green, self.blue)[index]


class Direction(Enum):
    """Enumeration for snake movement directions."""
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    
    def is_opposite(self, other: Direction) -> bool:
        """Check if this direction is opposite to another direction."""
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return opposites.get(self) == other


class Apple(pygame.sprite.Sprite):
    """
    Apple sprite that the snake can eat to grow.
    
    Represents the food item in the Snake game. When consumed by the snake,
    it increases the snake's length and the player's score.
    """
    
    DEFAULT_COLOR = Color(255, 0, 0)  # Red
    DEFAULT_SIZE = Size(10, 10)
    
    def __init__(self, 
                 position: Position,
                 color: Optional[Color] = None, 
                 size: Optional[Size] = None) -> None:
        """
        Initialize an Apple sprite.
        
        Args:
            position: The position where the apple should be placed
            color: RGB color values (defaults to red)
            size: Width and height dimensions (defaults to 10x10)
            
        Raises:
            ValueError: If position is None
        """
        super().__init__()
        
        if position is None:
            raise ValueError("Position cannot be None")
        
        self.color = color or self.DEFAULT_COLOR
        self.size = size or self.DEFAULT_SIZE
        self.position = position
        
        # Create the sprite surface and rectangle
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position


class SnakeTile:
    """Represents a single tile of the snake's body."""
    
    def __init__(self, position: Position, color: Color, size: Size) -> None:
        """Initialize a snake tile."""
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position


class SnakeHead(pygame.sprite.Sprite):
    """Represents the head of the snake."""
    
    def __init__(self, position: Position, color: Color, size: Size) -> None:
        """Initialize the snake head."""
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position


class SnakeTail:
    """Manages the snake's tail segments."""
    
    def __init__(self) -> None:
        """Initialize an empty tail."""
        self.tiles: List[SnakeTile] = []
    
    def add_tile(self, position: Position, color: Color, size: Size) -> None:
        """Add a new tile to the tail."""
        tile = SnakeTile(position, color, size)
        self.tiles.append(tile)
    
    def get_positions(self) -> List[Position]:
        """Get all tail tile positions."""
        return [Position(tile.rect.x, tile.rect.y) for tile in self.tiles]


class Snake(pygame.sprite.Sprite):
    """
    Snake sprite that represents the player-controlled snake.
    
    The snake consists of a head and a tail made up of multiple segments.
    It can move in four directions and grows when eating apples.
    """
    
    DEFAULT_COLOR = Color(0, 255, 0)  # Green
    DEFAULT_SIZE = Size(10, 10)
    DEFAULT_POSITION = Position(30, 30)
    
    def __init__(self, 
                 position: Optional[Position] = None,
                 color: Optional[Color] = None, 
                 size: Optional[Size] = None) -> None:
        """
        Initialize a Snake sprite.
        
        Args:
            position: Starting position (defaults to (30, 30))
            color: RGB color values (defaults to green)
            size: Width and height dimensions (defaults to 10x10)
            
        Raises:
            ValueError: If size width and height are not equal
        """
        super().__init__()
        
        self.color = color or self.DEFAULT_COLOR
        self.size = size or self.DEFAULT_SIZE
        self.position = position or self.DEFAULT_POSITION
        
        if self.size.width != self.size.height:
            raise ValueError("Snake tile size must be square (width == height)")
        
        # Initialize head
        self.head = SnakeHead(self.position, self.color, self.size)
        
        # Initialize tail with 2 segments
        self.tail = SnakeTail()
        tail_pos1 = Position(self.position.x - self.size.width, self.position.y)
        tail_pos2 = Position(self.position.x - 2 * self.size.width, self.position.y)
        
        self.tail.add_tile(tail_pos1, self.color, self.size)
        self.tail.add_tile(tail_pos2, self.color, self.size)
    
    def move(self, direction: Direction, frame_width: int, frame_height: int) -> bool:
        """
        Move the snake in the specified direction.
        
        Args:
            direction: Direction to move
            frame_width: Width of the game frame
            frame_height: Height of the game frame
            
        Returns:
            bool: True if move was successful, False if collision occurred
        """
        step_size = self.size.width
        current_head_pos = Position(self.head.rect.x, self.head.rect.y)
        
        # Calculate new head position
        new_head_position = self._calculate_new_position(
            current_head_pos, direction, step_size, frame_width, frame_height
        )
        
        # Check for self-collision
        if self.occupies_position(new_head_position):
            return False
        
        # Move head to new position
        old_head_position = Position(self.head.rect.x, self.head.rect.y)
        self.head.rect.topleft = new_head_position
        
        # Move tail segments
        self._move_tail(old_head_position)
        
        return True
    
    def _calculate_new_position(self, 
                              current_pos: Position, 
                              direction: Direction, 
                              step_size: int,
                              frame_width: int, 
                              frame_height: int) -> Position:
        """Calculate the new position based on direction and frame wrapping."""
        new_x, new_y = current_pos.x, current_pos.y
        
        if direction == Direction.UP:
            new_y = (new_y - step_size) % frame_height
        elif direction == Direction.DOWN:
            new_y = (new_y + step_size) % frame_height
        elif direction == Direction.RIGHT:
            new_x = (new_x + step_size) % frame_width
        elif direction == Direction.LEFT:
            new_x = (new_x - step_size) % frame_width
        
        return Position(new_x, new_y)
    
    def _move_tail(self, old_head_position: Position) -> None:
        """Move all tail segments forward."""
        previous_position = old_head_position
        
        for tile in self.tail.tiles:
            current_position = Position(tile.rect.x, tile.rect.y)
            tile.rect.topleft = previous_position
            previous_position = current_position
    
    def occupies_position(self, position: Position) -> bool:
        """
        Check if the snake occupies a given position.
        
        Args:
            position: Position to check
            
        Returns:
            bool: True if snake occupies the position
        """
        if position is None or position.x is None or position.y is None:
            return True
        
        # Check head position
        head_pos = Position(self.head.rect.x, self.head.rect.y)
        if head_pos.x == position.x and head_pos.y == position.y:
            return True
        
        # Check tail positions
        for tile in self.tail.tiles:
            tile_pos = Position(tile.rect.x, tile.rect.y)
            if tile_pos.x == position.x and tile_pos.y == position.y:
                return True
        
        return False
    
    def lengthen_tail(self, segments: int, current_direction: Direction) -> None:
        """
        Add segments to the snake's tail.
        
        Args:
            segments: Number of segments to add
            current_direction: Current movement direction
        """
        if segments <= 0:
            return
        
        step_size = self.size.width
        
        for i in range(segments):
            if not self.tail.tiles:
                continue
                
            last_tile = self.tail.tiles[-1]
            last_pos = Position(last_tile.rect.x, last_tile.rect.y)
            
            # Calculate new tile position based on direction
            new_pos = self._calculate_tail_extension_position(
                last_pos, current_direction, step_size, i
            )
            
            self.tail.add_tile(new_pos, self.color, self.size)
    
    def _calculate_tail_extension_position(self, 
                                         last_pos: Position, 
                                         direction: Direction, 
                                         step_size: int, 
                                         offset: int) -> Position:
        """Calculate where to place a new tail segment."""
        x, y = last_pos.x, last_pos.y
        
        if direction == Direction.UP:
            y = y - step_size + (offset * step_size)
        elif direction == Direction.DOWN:
            y = y + step_size + (offset * step_size)
        elif direction == Direction.RIGHT:
            x = x - step_size + (offset * step_size)
        elif direction == Direction.LEFT:
            x = x + step_size + (offset * step_size)
        
        return Position(x, y)
    
    def get_all_positions(self) -> List[Position]:
        """Get positions of all snake segments (head + tail)."""
        positions = [Position(self.head.rect.x, self.head.rect.y)]
        positions.extend(self.tail.get_positions())
        return positions