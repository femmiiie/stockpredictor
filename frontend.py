import dearpygui.dearpygui as gui

def render_front():
  gui.create_context()
  gui.create_viewport(title="COP3530 Project 3")
  gui.setup_dearpygui()

  with gui.font_registry():
    default_font = gui.add_font("Arimo\Arimo-VariableFont_wght.ttf", 20)

  with gui.window(tag="Primary"):
    gui.bind_font(default_font)
    gui.get_viewport_client_height()
    gui.add_button(label="Predict!", width=100, height=40)

  gui.show_viewport()
  gui.set_primary_window("Primary", True)
  gui.start_dearpygui()
  gui.destroy_context()