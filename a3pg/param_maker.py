import re
import pathfinder
import ctypes
import os
import subprocess
from baseconv import BaseConverter

COMPRESS_BASE = "0123456789abcdefghijklmnopqrstuvwxyz"
COMMAND_LINE_MAX_LENGTH = 7
LINKING_DIRECTORY_NAME = "A3PG"
ANSWER_YES = "Y"
ANSWER_NO = "N"

DEFAULT_LINK_DIR = ""
DEFAULT_COUNTER = 0

link_directory = DEFAULT_LINK_DIR
counter = DEFAULT_COUNTER
base_converter = BaseConverter(COMPRESS_BASE)

def find_link_directory():
  global link_directory
  if link_directory == "":
    # Link from system drive, with current working directory's drive as fallback.
    target_drive = os.path.splitdrive(os.getcwd())[0]
    knrl_dll = ctypes.windll.LoadLibrary("kernel32.dll")
    windows_directory = ctypes.create_unicode_buffer(1024)
    if knrl_dll.GetWindowsDirectoryW(windows_directory, 1024) != 0:
      target_drive = os.path.splitdrive(windows_directory.value)[0]
    root_directory = os.path.join(target_drive, os.sep, LINKING_DIRECTORY_NAME)
    
    if not os.path.isdir(root_directory):
      os.mkdir(root_directory) # Create link folder if not exists.
      knrl_dll.SetFileAttributesW(root_directory, 0x02) # Hide the folder.

    # Find a directory for current linking session.
    current_name_idx = -1
    dir_list = os.listdir(root_directory)
    dir_list.sort()
    for idx in range(len(dir_list) - 1, -1, -1):
      dir_name = dir_list[idx]
      try:
        dir_idx = int(base_converter.decode(dir_name))
        current_name_idx = dir_idx
        break
      except ValueError:
        pass
    
    current_name_idx += 1
    current_name = base_converter.encode(current_name_idx)

    link_directory = os.path.join(root_directory, current_name)
    if not os.path.isdir(link_directory):
      os.mkdir(link_directory)
  
  return link_directory


def read_additional_params(launcher_path):
  log_path = pathfinder.get_log_path(launcher_path)
  log_file = open(log_path, "r", encoding="utf-8")

  raw_param = ""
  for line in log_file.readlines():
    if line.find("GameExecutor:                    parameters:   ") > 0:
      raw_param = re.sub("^.+GameExecutor:                    parameters:   ", "", line)
      raw_param = re.sub(' "-mod=.*$', '', raw_param)
  return raw_param.strip()


def join_mod_paths(mod_list):
  return '"-mod={}"'.format(";".join(mod_list))


def make_link(original):
  global counter
  link_name = base_converter.encode(counter)
  # Do not compress name if mod.cpp is missing, to preserve mod names.
  if (not os.path.exists(os.path.join(original, "mod.cpp"))) or (not os.path.exists(os.path.join(original, "meta.cpp"))):
    link_name = os.path.basename(original)
  else:
    counter += 1

  root_dir = find_link_directory()
  link_path = os.path.join(root_dir, link_name)
  subprocess.check_call('mklink /J "%s" "%s"' % (link_path, original), shell=True, stdout=subprocess.DEVNULL)
  return link_path


def shorten_mod_paths(mod_list):
  answer = ""
  while answer.upper() not in [ANSWER_YES.upper(), ANSWER_NO.upper()]:
    try:
      answer = input("Parameters are too long! Would you like to shorten it? ({} / {}): ".format(ANSWER_YES.upper(), ANSWER_NO.lower()))
    except KeyboardInterrupt:
      answer = ""
      quit()

  if answer.upper() == ANSWER_YES.upper():
    shortened_paths = list()
    print("Creating symbolic links, this may take a while.")
    for path in mod_list:
      shortened_paths.append(make_link(path))
    return shortened_paths

  return mod_list


def make(launcher_path, mod_list):
  global link_directory
  global counter

  link_directory = DEFAULT_LINK_DIR
  counter = DEFAULT_COUNTER

  param_others = read_additional_params(launcher_path)
  params = param_others + " " + join_mod_paths(mod_list)

  if len(params) > COMMAND_LINE_MAX_LENGTH:
    mod_list = shorten_mod_paths(mod_list)
    params = param_others + " " + join_mod_paths(mod_list)

  return params
