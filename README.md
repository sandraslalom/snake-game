# Snake Game - Modernized

A modernized implementation of the classic Snake game using Python and pygame, featuring modern Python practices, type hints, and object-oriented design.

## Features

- **Modern Python**: Uses Python 3.8+ features including type hints, dataclasses, and enums
- **Object-Oriented Design**: Clean separation of concerns with proper class structure
- **Configurable**: Easy to customize game settings through configuration
- **Robust**: Proper error handling and logging
- **Extensible**: Well-structured code that's easy to modify and extend

## Requirements

- Python 3.8 or higher
- pygame 2.0.0 or higher

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/sandraslalom/snake-game.git
cd snake-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python game_modernized.py
```

### Using pip (if published)

```bash
pip install snake-game
snake-game
```

## How to Play

- Use arrow keys or WASD to control the snake
- Eat red apples to grow and increase your score
- Avoid hitting the snake's own body
- Press ESC to quit
- Press P to pause/unpause
- Press SPACE to restart after game over

## Game Controls

| Key | Action |
|-----|--------|
| ↑ or W | Move Up |
| ↓ or S | Move Down |
| ← or A | Move Left |
| → or D | Move Right |
| P | Pause/Resume |
| ESC | Quit Game |
| SPACE | Restart (when game over) |

## Configuration

The game can be customized by modifying the `GameConfig` class in `game_modernized.py`:

```python
config = GameConfig(
    screen_width=800,      # Screen width in pixels
    screen_height=600,     # Screen height in pixels
    tile_size=20,          # Size of each game tile
    update_speed=150,      # Game speed (lower = faster)
    background_color=Color(0, 0, 0)  # Background color (RGB)
)
```

## Development

### Setting up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
isort .
```

4. Type checking:
```bash
mypy .
```

### Building Executable

To create a standalone executable:

```bash
pyinstaller --onefile --windowed game_modernized.py
```

## Architecture

The modernized codebase follows these principles:

- **Type Safety**: Full type hints throughout the codebase
- **Separation of Concerns**: Game logic, rendering, and input handling are separated
- **Modern Python**: Uses dataclasses, enums, and other modern Python features
- **Error Handling**: Proper exception handling and logging
- **Configurability**: Easy to customize game behavior

### Key Classes

- `SnakeGame`: Main game controller managing the game loop
- `Snake`: Represents the player-controlled snake
- `Apple`: Represents the food items
- `GameConfig`: Configuration settings for the game
- `Direction`: Enum for movement directions
- `GameState`: Enum for different game states

## Changes from Original

This modernized version includes:

- ✅ Fixed import issues and deprecated dependencies
- ✅ Added comprehensive type hints
- ✅ Implemented proper object-oriented design
- ✅ Added configuration management
- ✅ Improved error handling and logging
- ✅ Added pause functionality
- ✅ Better game state management
- ✅ Modern Python packaging with setuptools
- ✅ Comprehensive documentation
- ✅ Development tooling setup

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite and linting
6. Submit a pull request

## Changelog

### Version 2.0.0
- Complete modernization of the codebase
- Added type hints and modern Python features
- Improved game architecture and error handling
- Added configuration system and pause functionality
- Updated packaging and dependencies