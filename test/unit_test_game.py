import unittest
import pygame
from unittest.mock import Mock
import os
import sys


parent_directory = os.path.abspath(os.path.join(os.getcwd(), '..\\CSCI_372_Midterm'))
sys.path.append(parent_directory)
print(sys.path)


from GameLoop import (
    Particle, Laser, Ship, Player, Enemy, FloatingText, Powerup, Shield
)

# Test for Particle class
class TestParticle(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.groups = pygame.sprite.Group()
        self.particle = Particle(self.groups, [100, 100], (255, 255, 255), pygame.math.Vector2(1, 1), 5)

    def test_particle_initialization(self):
        # Test if the particle initializes correctly
        self.assertEqual(self.particle.pos, [100, 100])
        self.assertEqual(self.particle.color, (255, 255, 255))
        self.assertEqual(self.particle.speed, 5)

    def test_particle_movement(self):
        # Test if the particle moves correctly
        self.particle.move()
        self.assertAlmostEqual(self.particle.pos[0], 105, places=1)
        self.assertAlmostEqual(self.particle.pos[1], 105, places=1)

    def test_particle_fade(self):
        # Test if the particle fades over time
        dt = 0.1
        self.particle.fade(dt)
        self.assertLess(self.particle.alpha, 255)

    def test_particle_removal(self):
        # Test if the particle is removed from the group when it fades
        self.particle.alpha = -1
        self.particle.update(0.1)
        self.assertNotIn(self.particle, self.groups)


# Test for Laser class
class TestLaser(unittest.TestCase):
    def setUp(self):
        self.laser_image = pygame.Surface((10, 30))  # Create a mock laser surface
        self.laser = Laser(100, 200, self.laser_image)

    def test_laser_initialization(self):
        # Test if the laser initializes correctly
        self.assertEqual(self.laser.x, 100)
        self.assertEqual(self.laser.y, 200)

    def test_laser_movement(self):
        # Test if the laser moves correctly
        self.laser.move(5)
        self.assertEqual(self.laser.y, 205)

    def test_laser_collision(self):
        # Test laser collision with a mock object
        mock_obj = Mock()
        mock_obj.x, mock_obj.y, mock_obj.mask = 95, 190, pygame.mask.Mask((10, 10))
        self.assertFalse(self.laser.collision(mock_obj))


# Test for Ship class
class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(100, 200, health=50)
        self.ship.ship_img = pygame.Surface((50, 50))
        self.ship.laser_img = pygame.Surface((10, 20))

    def test_ship_initialization(self):
        # Test if the ship initializes with correct health and cooldown counter
        self.assertEqual(self.ship.health, 50)
        self.assertEqual(self.ship.cool_down_counter, 0)

    def test_ship_cooldown(self):
        # Test if the cooldown of the ship works
        self.ship.cool_down_counter = 30
        self.ship.cooldown()
        self.assertEqual(self.ship.cool_down_counter, 0)

    def test_ship_shoot(self):
        # Test if the ship shoots lasers correctly
        self.ship.shoot()
        self.assertEqual(len(self.ship.lasers), 1)


# Test for Player class
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(300, 650, health=100)

    def test_player_initialization(self):
        # Test if the player initializes with correct health and speed boost state
        self.assertEqual(self.player.health, 100)
        self.assertFalse(self.player.speed_boost)

    def test_player_powerup_update(self):
        # Test if the player's powerup state is updated correctly
        self.player.active_powerups["cooldown"] = pygame.time.get_ticks()
        self.player.update_powerups()
        self.assertIn("cooldown", self.player.active_powerups)


# Test for Enemy class
class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.enemy = Enemy(100, 100, "alien1", health=30)

    def test_enemy_initialization(self):
        # Test if the enemy initializes with correct health and position
        self.assertEqual(self.enemy.health, 30)
        self.assertEqual(self.enemy.x, 100)
        self.assertEqual(self.enemy.y, 100)

    def test_enemy_movement(self):
        # Test if the enemy moves correctly
        self.enemy.move(5, 10)
        self.assertEqual(self.enemy.x, 105)
        self.assertEqual(self.enemy.y, 110)


# Test for FloatingText class
class TestFloatingText(unittest.TestCase):
    def setUp(self):
        self.text = FloatingText("Test", (100, 100), color=(255, 0, 0))

    def test_floating_text_initialization(self):
        # Test if the floating text initializes correctly
        self.assertEqual(self.text.text, "Test")
        self.assertEqual(self.text.color, (255, 0, 0))

    def test_floating_text_fade(self):
        # Test if the floating text fades over time
        for _ in range(60):  # Simulate 60 frames of fading
            self.text.update()
        self.assertLess(self.text.alpha, 0)


# Test for Shield class
class TestShield(unittest.TestCase):
    def setUp(self):
        self.shield = Shield(100, 200, "green", health=100)

    def test_shield_initialization(self):
        # Test if the shield initializes correctly with health and color
        self.assertEqual(self.shield.health, 100)
        self.assertEqual(self.shield.color, "green")


# Test for Powerup class
class TestPowerup(unittest.TestCase):
    def setUp(self):
        self.powerup = Powerup(100, 200, "cooldown")

    def test_powerup_initialization(self):
        # Test if the powerup initializes correctly with type and position
        self.assertEqual(self.powerup.type, "cooldown")
        self.assertEqual(self.powerup.x, 100)
        self.assertEqual(self.powerup.y, 200)


if __name__ == "__main__":
    unittest.main()  # Run all tests
