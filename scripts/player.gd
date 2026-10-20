extends CharacterBody2D

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
const SPEED = 200.0

func _physics_process(delta: float) -> void:
	process_movement()
	move_and_slide()
	
func process_movement() -> void:
	var direction := Input.get_vector("esquerda", "direita", "cima", "baixo")
	
	velocity = direction * SPEED
	
	play_animation(direction)
	
func play_animation(dir: Vector2) -> void: 
	if dir.x != 0:
		animated_sprite_2d.flip_h= dir.x < 0
		animated_sprite_2d.play("walking right")
	elif dir.y < 0:
		animated_sprite_2d.play("walking up")
	elif dir.y > 0:
		animated_sprite_2d.play("walking front")
	else:
		animated_sprite_2d.play("idle front")
		
