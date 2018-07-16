class Settings():
	"""存储外星人入侵的所有设置的类"""

	def __init__(self):
		"""初始化游戏的设置"""
		# 屏幕可见
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		# 飞船		
		self.ship_limit = 1

		# 子弹设置		
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 10

		# 外星人设置		
		self.fleet_drop_speed = 10
		

		# 以什么样的速度加快游戏节奏
		self.speedup_scale = 1.2
		# 外星人点数提高速度
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""随游戏进行变化的设置"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 1
		self.alien_speed_factor = 1
		self.fleet_direction = 1
		# 计分
		self.alien_points = 50

	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
