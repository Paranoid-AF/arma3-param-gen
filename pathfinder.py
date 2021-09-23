import os
import json
import re

def get_launcher_path():
  launcher_data_directory = os.path.join(os.getenv("LOCALAPPDATA"), "Arma 3 Launcher")
  if os.path.isdir(launcher_data_directory):
    return launcher_data_directory
  else:
    raise Exception("Launcher data not found!")


def get_workshop_mods_paths(launcher_path):
  steam_file = open(os.path.join(launcher_path, "Steam.json"), mode = "r", encoding="utf-8")
  steam_json = json.load(steam_file)
  steam_file.close()

  paths = dict()

  for item in steam_json["Extensions"]:
    paths[item["Id"]] = item["ExtensionPath"]
  
  return paths


def get_local_mods_paths(launcher_path):
  local_file = open(os.path.join(launcher_path, "Local.json"), mode = "r", encoding="utf-8")
  local_json = json.load(local_file)
  local_file.close()

  paths = dict()

  for item in local_json["knownLocalMods"]:
    item_id = "local:" + os.path.join(item, "").upper()
    paths[item_id] = item

  return paths


def get_all_mods_paths(launcher_path):
  try:
    workshop_mods_paths = get_workshop_mods_paths(launcher_path)
  except Exception:
    workshop_mods_paths = dict()
    print("Warning: No workshop mods found!")
  
  try:
    local_mods_paths = get_local_mods_paths(launcher_path)
  except Exception:
    local_mods_paths = dict()
    print("Warning: No local mods found!")

  return { **workshop_mods_paths, **local_mods_paths }


def get_preset_paths(launcher_path):
  preset_directory = os.path.join(launcher_path, "Presets")
  if os.path.isdir(preset_directory):
    preset_files = os.listdir(preset_directory)
    paths = list()
    for file in preset_files:
      pair = dict()
      pair["path"] = os.path.join(preset_directory, file)
      if file.endswith(".defaultpreset2"):
        pair["id"] = "Default Preset"
        paths = [pair] + paths
      else:
        pair["id"] = re.sub(".preset2$", "", file)
        paths.append(pair)
    return paths
  else:
    raise Exception("No preset found!")


def get_log_path(launcher_path):
  log_path = os.path.join(launcher_path, "Logs", "Launcher.log")
  if os.path.isfile(log_path):
    return log_path
  else:
    raise Exception("Launcher log not found!")
