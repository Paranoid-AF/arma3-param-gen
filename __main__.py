import re
import pathfinder
import preset_loader
import pyperclip

# As this script is Windows-only in the first place, this doesn't seem to matter anyways.
def send_to_clipboard(content):
  pyperclip.copy(content)

def choose_preset(launcher_path):
  preset_paths = pathfinder.get_preset_paths(launcher_path)
  print("THIS PROGRAM WILL OVERWRITE YOUR CLIPBOARD, MAKE A BACKUP IF NECESSARY.\n")
  print("Found {} modification presets in ArmA 3 Launcher.".format(len(preset_paths)))

  for index, item in enumerate(preset_paths):
    print("{}. {}".format(index + 1, item['id']))

  print("\nChoose a preset to generate parameters with.")
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

def read_additional_params(launcher_path):
  log_path = pathfinder.get_log_path(launcher_path)
  log_file = open(log_path, "r", encoding="utf-8")

  raw_param = ""
  for line in log_file.readlines():
    if line.find("GameExecutor:                    parameters:   ") > 0:
      raw_param = re.sub("^.+GameExecutor:                    parameters:   ", "", line)
      raw_param = re.sub(' "-mod=.*$', '', raw_param)
  return raw_param.strip()

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
      print("Warning: Missing mod: {}".format(item))
  
  param_others = read_additional_params(launcher_path)
  param_mod = '"-mod={}"'.format(";".join(enabled_mod_paths))

  send_to_clipboard(param_others + " " + param_mod)
  print("Params are copied to your clipboard!")


try:
  main()
except Exception as e:
  print("ERROR: {}".format(e))
  print("Make sure you have started the game via the official ArmA 3 Launcher at least once, then try again.")
