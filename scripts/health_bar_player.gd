extends Node2D

@onready var health_player: Sprite2D = $HealthPlayer

@onready var default_width: float = health_player.region_rect.size.x
@onready var default_height: float = health_player.region_rect.size.y

func update_health_player(new_health: int) -> void:
	var new_width = (float(new_health) / 100.0) * default_width

	health_player.region_rect = Rect2(
		0, 0, new_width, default_height
	)
