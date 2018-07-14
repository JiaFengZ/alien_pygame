import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		# 向右移动飞船
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		# 向左移动飞船
		ship.moving_left = True
	if event.key == pygame.K_SPACE:
		# 创建一颗子弹，加入编组bullets
		fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		
		if event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, screen, ship, bullets)

def update_screen(ai_settings, screen, ship, bullets):
	"""更新屏幕上的图像，并切换到新屏幕"""

	# 每次循环重绘屏幕				
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面绘制子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	# 绘制飞船
	ship.blitme()
	# 让最近绘制屏幕可见
	pygame.display.flip()

def update_bullets(bullets):
	"""更新子弹组的位置，并删除已经消失的子弹"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			print(len(bullets))

def fire_bullet(ai_settings, screen, ship, bullets):
	"""发射子弹"""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)