
extends CanvasLayer

func _ready() -> void:
	hide()

func show_screen() -> void:
	show()

func _on_button_pressed() -> void:
	get_tree().reload_current_scene()
