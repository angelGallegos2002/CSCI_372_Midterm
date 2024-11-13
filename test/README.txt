Unit Tests for Space Invaders Game Components

This repository contains unit tests for various game components used in the Space Invaders game, built with Pygame. These tests ensure that the game objects and their behaviors are implemented correctly. The tests cover different game elements, including particles, lasers, ships, players, enemies, floating text, powerups, shields, and collision detection.

Test Overview

1. Particle Class (TestParticle)
- test_particle_initialization: Verifies that a particle is initialized with the correct position, color, and speed.
- test_particle_movement: Ensures that the particle moves in the expected direction when the move() method is called.
- test_particle_fade: Tests that the particle fades over time when the fade() method is called.
- test_particle_removal: Verifies that the particle is removed from the sprite group when its alpha becomes negative.

2. Laser Class (TestLaser)
- test_laser_initialization: Ensures the laser is initialized with the correct position.
- test_laser_movement: Verifies that the laser moves correctly when the move() method is called.
- test_laser_collision: Simulates a laser collision with an object and checks that the laser correctly detects the collision.

3. Ship Class (TestShip)
- test_ship_initialization: Verifies that the ship is initialized with the correct health and cooldown state.
- test_ship_cooldown: Tests that the ship's cooldown counter is correctly reset after being updated.
- test_ship_shoot: Ensures that the ship correctly shoots lasers when the shoot() method is called.

4. Player Class (TestPlayer)
- test_player_initialization: Verifies that the player is initialized with the correct health and speed boost state.
- test_player_powerup_update: Tests that the player's powerup states are updated correctly, such as the cooldown powerup.

5. Enemy Class (TestEnemy)
- test_enemy_initialization: Ensures that the enemy is initialized with the correct health and position.
- test_enemy_movement: Verifies that the enemy moves correctly according to its movement speed.

6. FloatingText Class (TestFloatingText)
- test_floating_text_initialization: Verifies that the floating text object is initialized with the correct text and color.
- test_floating_text_fade: Tests that the floating text fades over time, simulating the effect of text disappearing after a set period.

7. Shield Class (TestShield)
- test_shield_initialization: Ensures that the shield is initialized with the correct health and color.

8. Powerup Class (TestPowerup)
- test_powerup_initialization: Verifies that the powerup is initialized with the correct type and position.

Dependencies

This project requires Pygame and unittest for testing. You can install Pygame via pip if it's not already installed:

pip install pygame

Running the Tests

To run all tests, execute the following command:

python -m unittest test_game_components.py

This will run all the test cases, which will verify the correctness of the various game components.
