extends Node2D

@onready var health_bar: Sprite2D = $Health
@onready var default_width = health_bar.region_rect.size.x
@onready var default_height = health_bar.region_rect.size.y

func update_health(new_healt: int) -> void:
	
	var new_width = (new_healt / 100.0) * default_width
	health_bar.region_rect = Rect2(0, 0,new_width, default_height) 
