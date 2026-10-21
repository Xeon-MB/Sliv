extends CharacterBody2D

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
const SPEED = 100.0
var atacking = false
@onready var swing_sword: AudioStreamPlayer2D = $SwingSword
var hitbox_offset: Vector2
@onready var hitbox: Area2D = $hitbox
var last_direction := Vector2.DOWN
var strenght: int = 20

func _ready() -> void:
	hitbox_offset = hitbox.position
	update_hitbox_offset()

func _physics_process(delta: float) -> void:
	hitbox.monitoring = false
	
	
	if Input.is_action_just_pressed("ataque") and not atacking:
		ataque()
	if atacking:
		velocity = Vector2.ZERO
		return
	if not atacking:
		process_movement()

	move_and_slide()
	
func process_movement() -> void:
	var direction := Input.get_vector("esquerda", "direita", "cima", "baixo")
	
	velocity = direction * SPEED

	if direction != Vector2.ZERO:
		last_direction = direction
	
	update_hitbox_offset()
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
		
func ataque() -> void:
	atacking = true 
	hitbox.monitoring = true

	update_hitbox_offset()
	swing_sword.play()
	play_animation("atacking", last_direction)
	await animated_sprite_2d.animation_finished

	atacking = false
	
	
func update_hitbox_offset() -> void:
	var x := hitbox_offset.x
	var y := hitbox_offset.y		
	
	match last_direction:
		Vector2.LEFT:
			hitbox.position = Vector2(-x, y)
		Vector2.RIGHT:
			hitbox.position = Vector2(x, y)
		Vector2.UP:
			hitbox.position = Vector2(y, -x)
		Vector2.DOWN:
			hitbox.position = Vector2(-y , x)


func _on_hitbox_body_entered(body: Node2D) -> void:
	if atacking and body.name.begins_with("Slime"):
		body.leva_dano(strenght, position)
		
