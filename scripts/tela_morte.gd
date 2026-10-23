
extends CanvasLayer
@onready var descr: Label = $CenterContainer/VBoxContainer/descr


func _ready() -> void:
	hide()

func show_screen(inimigos_mortos: int) -> void:
	descr.text = "Você Matou " + str(inimigos_mortos) + " Inimigos"
	show()

func _on_button_pressed() -> void:
	get_tree().reload_current_scene()
