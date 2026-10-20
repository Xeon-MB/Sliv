extends CharacterBody2D

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
const SPEED = 200.0

func _physics_process(delta: float) -> void:
	process_movement()
	move_and_slide()
	
func process_movement() -> void:
	var direction := Input.get_vector("esquerda", "direita", "cima", "baixo")
	
	velocity = direction * SPEED
	
	process_animation(direction)
	
func process_animation(direction) -> void:
	if velocity != Vector2.ZERO:
		play_animation("walking", direction)
	else:
		play_animation("idle", direction)
	
func play_animation(prefix: String, dir: Vector2) -> void: 
	if dir.x != 0:
		animated_sprite_2d.flip_h= dir.x < 0
		animated_sprite_2d.play(prefix + "_right")
	elif dir.y < 0:
		animated_sprite_2d.play(prefix + "_up")
	elif dir.y > 0:
		animated_sprite_2d.play(prefix + "_front")
	else:
		animated_sprite_2d.play("idle_front")
		
