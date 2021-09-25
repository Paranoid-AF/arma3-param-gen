import pathfinder
import preset_loader
import pyperclip
import param_maker

def send_to_clipboard(content):
  pyperclip.copy(content)


def choose_preset(launcher_path):
  preset_paths = pathfinder.get_preset_paths(launcher_path)
  print("THIS PROGRAM WILL OVERWRITE YOUR CLIPBOARD, MAKE A BACKUP IF NECESSARY.\n")
  print("Found {} modification presets in ArmA 3 Launcher.".format(len(preset_paths)))

  for index, item in enumerate(preset_paths):
    print("{}. {}".format(index + 1, item['id']))

  print("\nChoose a preset to generate parameters with, or use Ctrl + C to exit.")
  selection = -1
  while(selection < 0):
    try:
      selection = int(input("Input corresponding number: "))
      if(selection < 1 or selection > len(preset_paths)):
        raise Exception()
    except Exception:
      selection = -1
      print("Invalid input. Try again!")
    except KeyboardInterrupt:
      quit()
  
  return preset_paths[selection - 1]


def main():
  print("            -== ArmA 3 Launch Parameter Generator ==-")
  launcher_path = pathfinder.get_launcher_path()
  preset_meta = choose_preset(launcher_path)
  preset = preset_loader.load(preset_meta['path'])

  mod_meta = pathfinder.get_all_mods_paths(launcher_path)
  enabled_mod_paths = list()
  for item in preset:
    if item in mod_meta:
      enabled_mod_paths.append(mod_meta[item])
    else:
      print("WARNING: Missing mod: {}".format(item))

  send_to_clipboard(param_maker.make(launcher_path, enabled_mod_paths))
  print("Parameters are copied to your clipboard!")


try:
  main()
except Exception as e:
  print("ERROR: {}".format(e))
  print("Make sure you have started the game via the official ArmA 3 Launcher at least once, then try again.")
