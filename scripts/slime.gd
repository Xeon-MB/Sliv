extends CharacterBody2D


const SPEED: int = 50
var target = null
var healthy: int = 100
@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var slime: CharacterBody2D = $"."
@onready var takedamage: AudioStreamPlayer2D = $takedamage
const KNOCKBACK_FORCE: int = 50

func _process(delta: float) -> void:
	if healthy <= 0:
		morre()

func _physics_process(delta: float) -> void:
	if target :
		_ataque(delta)

func _ataque(delta: float) -> void:
	var direction = (target.position - position).normalized()
	position += direction * SPEED * delta
	animated_sprite_2d.play("atacking")

	
func leva_dano(damage: int, attacker_position: Vector2) -> void:
	healthy -= damage
	print(healthy)
	takedamage.play()
	var knockback_direction = (position - attacker_position).normalized()
	var target_position = position + knockback_direction * KNOCKBACK_FORCE
	
	var tween = create_tween()
	tween.tween_property(self, "position", target_position, 0.5)

func _on_sight_body_entered(body: Node2D) -> void:
	if body.name == "Player":
		target = body


func _on_sight_body_exited(body: Node2D) -> void:
	if body.name == "Player":
		target = null
		animated_sprite_2d.play("idle")
		
		
func morre() -> void:
	animated_sprite_2d.play("die")
	set_physics_process(false)
	await animated_sprite_2d.animation_finished
	queue_free()
		
