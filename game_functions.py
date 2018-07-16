import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

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

	if event.key == pygame.K_q:
		sys.exit()

def check_keyup_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

		if event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		
		if event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, screen, ship, bullets)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_click and not stats.game_active:
		# 重置游戏参数
		ai_settings.initialize_dynamic_settings()
		# 光标不可见
		pygame.mouse.set_visible(False)
		# 重置游戏
		stats.reset_stats()
		stats.game_active = True

		aliens.empty()
		bullets.empty()

		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""

	# 每次循环重绘屏幕				
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面绘制子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	# 绘制飞船
	ship.blitme()
	# 绘制外星人
	aliens.draw(screen)
	# 显示得分
	sb.show_score()
	# 如果游戏处于非活动状态，就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()
	# 让最近绘制屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""更新子弹组的位置，并删除已经消失的子弹"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			print(len(bullets))
	# 检查是否有子弹击中外星人
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
	collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collision:
		for aliens in collision.values():			
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		# 删除现有子弹并新建一群外星人，进入下一关
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""发射子弹"""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_aliens_y(ai_settings, ship.rect.height, alien.rect.height)	

	# 创建第一行外星人
	for row_number in range(number_rows):		
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_aliens_y(ai_settings, ship_height, alien_height):
	"""计算外星人行数"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, number_rows):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_rows
	aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""响应飞船被外星人碰撞"""
	if stats.ships_left > 0:
		stats.ships_left -= 1

		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建新一群外星人
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		# 暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottoms(ai_settings, stats, screen, ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	# 对编组aliens调用update方法，将自动对编组中每一个外星人调用update
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	# 检查外星人和飞船碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		print("ship hit!!")
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	check_aliens_bottoms(ai_settings, stats, screen, ship, aliens, bullets)

def check_high_score(stats, sb):   
 	"""检查是否诞生了新的最高得分"""   
 	if stats.score > stats.high_score:    
 		stats.high_score = stats.score          
 		sb.prep_high_score()
