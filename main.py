import dearpygui.dearpygui as gui


def main():
  gui.create_context()
  gui.create_viewport(title="COP3530 Project 3")
  gui.setup_dearpygui()

  with gui.window(tag="Primary"):
    gui.add_text("Project 3")

  gui.show_viewport()
  gui.set_primary_window("Primary", True)
  gui.start_dearpygui()
  gui.destroy_context()


if __name__ == "__main__":
  main()