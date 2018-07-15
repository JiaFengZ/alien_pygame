import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf

def run_game():
	pygame.init()
	ai_settings = Settings()
	# 从setting类中读取配置，创建一个游戏窗口，宽1200px 高800px
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	# 设置窗口标题
	pygame.display.set_caption("Alien_Invasion")
	# 创建游戏统计信息实例
	stats = GameStats(ai_settings)
	# 创建飞船
	ship = Ship(ai_settings, screen)
	# 创建外星人
	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)
	# 创建一个用于存储子弹的编组
	bullets = Group()

	while True:
		gf.check_events(ai_settings, screen, ship, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()
