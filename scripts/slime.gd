extends CharacterBody2D


const SPEED: int = 50
var target = null
var healthy: int = 100
const KNOCKBACK_FORCE: int = 170
var inimigos_mortos: int = 0
var knockback_velocity: Vector2 = Vector2.ZERO
var strenght: int = 10
var target_in_range: bool = false

@onready var animated_sprite_2d: AnimatedSprite2D = $AnimatedSprite2D
@onready var slime: CharacterBody2D = $"."
@onready var takedamage: AudioStreamPlayer2D = $takedamage
@onready var health_bar: Node2D = $HealthBar
@onready var label: Label = get_node_or_null("../../Player/Label")
@onready var attack_speed: Timer = $AttackSpeed

func _process(delta: float) -> void:
	if healthy <= 0:
		morre()

func _physics_process(delta: float) -> void:
	if knockback_velocity.length() > 5:
		velocity = knockback_velocity
		move_and_slide()
		knockback_velocity = knockback_velocity.move_toward(Vector2.ZERO, 250 * delta)
	else:
		knockback_velocity = Vector2.ZERO

		if target:
			var direction = (target.global_position - global_position).normalized()
			velocity = direction * SPEED
		else:
			velocity = Vector2.ZERO

		move_and_slide()

	if target:
		animated_sprite_2d.play("atacking")


func _ataque(delta: float) -> void:
	var direction = (target.global_position - global_position).normalized()

	velocity = direction * SPEED
	move_and_slide()
	
	

	animated_sprite_2d.play("atacking")


	
func leva_dano(damage: int, attacker_position: Vector2) -> void:
	healthy -= damage
	health_bar.update_health(healthy)
	takedamage.play()

	knockback_velocity = (global_position - attacker_position).normalized() * KNOCKBACK_FORCE

func _on_sight_body_entered(body: Node2D) -> void:
	if body.name == "Player":
		target = body


func _on_sight_body_exited(body: Node2D) -> void:
	if body.name == "Player":
		target = null
		animated_sprite_2d.play("idle")
		
		
func morre() -> void:

	set_process(false)
	set_physics_process(false)

	animated_sprite_2d.play("die")
	await animated_sprite_2d.animation_finished


	var player = get_node_or_null("../../Player")

	if player:
		player.inimigos_mortos += 1
	

	if player.label:
		player.label.text = "Pontos: " + str(player.inimigos_mortos)

	if is_instance_valid(player):
		player.fim()
	
	queue_free()
	


func _on_hitbox_body_entered(body: Node2D) -> void:
	if body.name == "Player":
		target_in_range = true
		body.leva_dano(strenght)
		attack_speed.start()

func _on_hitbox_body_exited(body: Node2D) -> void:
	if body.name == "Player":
		target_in_range = false
		attack_speed.stop()

func _on_attack_speed_timeout() -> void:
	if target and target_in_range:
		target.leva_dano(strenght)
