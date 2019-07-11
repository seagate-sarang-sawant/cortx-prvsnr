import sys
# How to test:
# $ salt-call saltutil.clear_cache
# $ salt-call saltutil.sync_modules
# $ salt-call eosconfig.update "/opt/seagate/s3/conf/s3config.yaml" s3server


# def update(name: str, ref_pillar: str, type: str=None, backup: bool=True) -> bool:
def update(name, ref_pillar, type=None, backup=True):
  """Update component config file.

  Args :
    name: Destination path of component config file to be updated
    ref_pillar: Reference section from pillar data for a component to be updated
    type: Type of config file YAML/INI
    backup: Backup config file before modification as bool (Default: True)
  """
  # print("Name: {0}".format(name))
  # print("Pillar ref: {0}".format(ref_pillar))

  pillar_data = _read_pillar(ref_pillar)
  # print("Pillar data: {0}".format(pillar_data))

  config_data = None
  if type and 'YAML' in type.upper():
    config_data = _read_yaml(name)
  elif type and 'INI' in type.upper():
    config_data = _read_ini(name)
  else:
    config_data = _read_config_file(name)

  print("Config data: {0}".format(config_data))

  return True if config_data else False


# def _read_config_file(config_filename: str) -> dict:
def _read_config_file(config_filename):
  config_data = None

  try:
    config_data = _read_yaml(config_filename)
  except Exception as e:
    # print(e)
    try:
      config_data = _read_ini(config_filename)
    except Exception as e:
      # print(e)
      print("Unexpected file format encountered.")

  return config_data


# def _read_yaml(config_filename: str) -> dict:
def _read_yaml(config_filename):
  import yaml
  print("Attempting YAML format")

  try:
    with open(config_filename, 'r') as fd:
      yaml_to_dict = yaml.safe_load(fd)
      print(yaml_to_dict)
      return yaml_to_dict
  except yaml.YAMLError as ex:
    # print(ex)
    msg = """
    ==================================================
    ERROR: Provided input config file not in YAML format.
    Unable to read/update provided config file.
    ==================================================
    """
    raise Exception(msg)


# def _read_ini(config_filename: str) -> dict:
def _read_ini(config_filename):
  print("Attempting INI format")

  if "2." in sys.version:
    from ConfigParser import ConfigParser, ParsingError, MissingSectionHeaderError
  else:
    from configparser import ConfigParser, ParsingError, MissingSectionHeaderError

  ini_to_dict = None
  parser = ConfigParser()
  try:
    ini_to_dict = parser.read(config_filename)._sections
    print("INI file read as: {0}".format(ini_to_dict))

  except MissingSectionHeaderError:
    print("ERROR: INI file {0} has no section header".format(config_filename))
    with open(config_filename, 'r') as fd:
        ini_to_dict = parser.read_string("[top]\n" + fd.read())._section
        print("INI file read as: {0}".format(ini_to_dict))

  except ParsingError as ex:
    print(ex.message)
    msg = """
    ==================================================
    ERROR: Provided input config file not in INI format.
    Unable to read/update provided config file.
    ==================================================
    """
    raise Exception(msg)

  return ini_to_dict


# def _read_pillar(ref_component_pillar: str) -> dict:
def _read_pillar(ref_component_pillar):
  return __pillar__[ref_component_pillar]
