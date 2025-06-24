"""
Modern Snake Game Implementation

A modernized version of the classic Snake game using pygame with proper
object-oriented design, type hints, and modern Python practices.
"""

from __future__ import annotations
import pygame
import random
import sys
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple
import logging

from sprites_modernized import Snake, Apple, Direction, Position, Size, Color

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameState(Enum):
    """Enumeration for different game states."""
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    PAUSED = "PAUSED"
    QUIT = "QUIT"


@dataclass
class GameConfig:
    """Configuration settings for the Snake game."""
    screen_width: int = 640
    screen_height: int = 480
    tile_size: int = 10
    initial_direction: Direction = Direction.RIGHT
    update_speed: int = 100  # milliseconds
    background_color: Color = Color(0, 0, 0)  # Black
    
    @property
    def screen_size(self) -> Size:
        """Get screen size as Size object."""
        return Size(self.screen_width, self.screen_height)
    
    @property
    def grid_width(self) -> int:
        """Get number of horizontal grid cells."""
        return self.screen_width // self.tile_size
    
    @property
    def grid_height(self) -> int:
        """Get number of vertical grid cells."""
        return self.screen_height // self.tile_size


class SnakeGame:
    """
    Main Snake Game class that manages game state, rendering, and logic.
    
    This class encapsulates all game functionality including the game loop,
    event handling, collision detection, and rendering.
    """
    
    def __init__(self, config: Optional[GameConfig] = None) -> None:
        """
        Initialize the Snake game.
        
        Args:
            config: Game configuration settings
        """
        self.config = config or GameConfig()
        self.state = GameState.PLAYING
        self.score = 0
        self.direction = self.config.initial_direction
        self.last_update_time = 0
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self._initialize_game_objects()
        
        logger.info("Snake game initialized successfully")
    
    def _initialize_game_objects(self) -> None:
        """Initialize the snake and apple objects."""
        # Create snake at center of screen
        snake_start_pos = Position(
            self.config.screen_width // 2,
            self.config.screen_height // 2
        )
        snake_size = Size(self.config.tile_size, self.config.tile_size)
        self.snake = Snake(position=snake_start_pos, size=snake_size)
        
        # Create first apple
        self.apple = self._create_apple()
    
    def _create_apple(self) -> Apple:
        """
        Create a new apple at a random position not occupied by the snake.
        
        Returns:
            Apple: New apple instance
            
        Raises:
            RuntimeError: If no valid position can be found (game board full)
        """
        max_attempts = self.config.grid_width * self.config.grid_height
        attempts = 0
        
        while attempts < max_attempts:
            # Generate random grid position
            grid_x = random.randint(0, self.config.grid_width - 1)
            grid_y = random.randint(0, self.config.grid_height - 1)
            
            # Convert to pixel position
            pixel_x = grid_x * self.config.tile_size
            pixel_y = grid_y * self.config.tile_size
            position = Position(pixel_x, pixel_y)
            
            # Check if position is free
            if not self.snake.occupies_position(position):
                apple_size = Size(self.config.tile_size, self.config.tile_size)
                return Apple(position=position, size=apple_size)
            
            attempts += 1
        
        # This should rarely happen unless the snake fills the entire screen
        raise RuntimeError("Cannot find valid position for apple - game board may be full")
    
    def _handle_events(self) -> None:
        """Handle pygame events including keyboard input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.QUIT
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
    
    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard input events.
        
        Args:
            event: Pygame keyboard event
        """
        key_direction_map = {
            pygame.K_UP: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_w: Direction.UP,
            pygame.K_s: Direction.DOWN,
            pygame.K_a: Direction.LEFT,
            pygame.K_d: Direction.RIGHT,
        }
        
        if event.key == pygame.K_ESCAPE:
            self.state = GameState.QUIT
        elif event.key == pygame.K_SPACE and self.state == GameState.GAME_OVER:
            self._restart_game()
        elif event.key == pygame.K_p and self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif event.key == pygame.K_p and self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
        elif event.key in key_direction_map and self.state == GameState.PLAYING:
            new_direction = key_direction_map[event.key]
            # Prevent snake from reversing into itself
            if not new_direction.is_opposite(self.direction):
                self.direction = new_direction
    
    def _update_game_logic(self) -> None:
        """Update game logic including snake movement and collision detection."""
        if self.state != GameState.PLAYING:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time < self.config.update_speed:
            return
        
        # Move snake
        move_successful = self.snake.move(
            self.direction, 
            self.config.screen_width, 
            self.config.screen_height
        )
        
        if not move_successful:
            self.state = GameState.GAME_OVER
            logger.info(f"Game over! Final score: {self.score}")
            return
        
        # Check apple collision
        snake_head_pos = Position(self.snake.head.rect.x, self.snake.head.rect.y)
        apple_pos = Position(self.apple.rect.x, self.apple.rect.y)
        
        if snake_head_pos.x == apple_pos.x and snake_head_pos.y == apple_pos.y:
            self._handle_apple_eaten()
        
        self.last_update_time = current_time
    
    def _handle_apple_eaten(self) -> None:
        """Handle when the snake eats an apple."""
        self.score += 1
        self.snake.lengthen_tail(1, self.direction)
        
        try:
            self.apple = self._create_apple()
        except RuntimeError:
            # Game board is full - player wins!
            self.state = GameState.GAME_OVER
            logger.info("Congratulations! You filled the entire board!")
        
        self._update_window_title()
        logger.info(f"Apple eaten! Score: {self.score}")
    
    def _update_window_title(self) -> None:
        """Update the window title with current score and game state."""
        if self.state == GameState.GAME_OVER:
            title = f"Snake Game - Score: {self.score} - GAME OVER (Press SPACE to restart)"
        elif self.state == GameState.PAUSED:
            title = f"Snake Game - Score: {self.score} - PAUSED (Press P to resume)"
        else:
            title = f"Snake Game - Score: {self.score}"
        
        pygame.display.set_caption(title)
    
    def _render(self) -> None:
        """Render all game objects to the screen."""
        # Clear screen
        self.screen.fill(self.config.background_color)
        
        if self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Render apple
            self.screen.blit(self.apple.image, self.apple.rect)
            
            # Render snake head
            self.screen.blit(self.snake.head.image, self.snake.head.rect)
            
            # Render snake tail
            for tile in self.snake.tail.tiles:
                self.screen.blit(tile.image, tile.rect)
        
        if self.state == GameState.PAUSED:
            self._render_pause_message()
        elif self.state == GameState.GAME_OVER:
            self._render_game_over_message()
        
        pygame.display.flip()
    
    def _render_pause_message(self) -> None:
        """Render pause message overlay."""
        font = pygame.font.Font(None, 36)
        text = font.render("PAUSED - Press P to resume", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2))
        self.screen.blit(text, text_rect)
    
    def _render_game_over_message(self) -> None:
        """Render game over message overlay."""
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to restart or ESC to quit", True, (255, 255, 255))
        
        # Center the text
        game_over_rect = game_over_text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2 - 40))
        score_rect = score_text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2))
        restart_rect = restart_text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2 + 40))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def _restart_game(self) -> None:
        """Restart the game with initial settings."""
        self.state = GameState.PLAYING
        self.score = 0
        self.direction = self.config.initial_direction
        self.last_update_time = 0
        self._initialize_game_objects()
        self._update_window_title()
        logger.info("Game restarted")
    
    def run(self) -> None:
        """
        Main game loop.
        
        Handles events, updates game logic, and renders the game until quit.
        """
        logger.info("Starting game loop")
        
        while self.state != GameState.QUIT:
            self._handle_events()
            self._update_game_logic()
            self._update_window_title()
            self._render()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        logger.info("Game ended")


def main() -> None:
    """Main entry point for the Snake game."""
    try:
        # Create custom configuration if desired
        config = GameConfig(
            screen_width=800,
            screen_height=600,
            tile_size=20,
            update_speed=150  # Slightly slower for better playability
        )
        
        game = SnakeGame(config)
        game.run()
        
    except Exception as e:
        logger.error(f"Game crashed with error: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()