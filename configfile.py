import json
import os

class ConfigFile(object):
    def __init__(self, file_path, mode, *args, **kargs):
        self.file_path = file_path
        self.mode = mode
        self.args = args
        self.kargs = kargs
        self.__config = None
        self.__create_or_open()

    def __create_or_open(self):
        try:
            dir = os.path.dirname(self.file_path)
            if  dir != "":
                os.makedirs(dir, exist_ok=True)
        except OSError as e:
            print("Unable to create directories: %s \"%s\"" % (e.strerror, e.filename))
            return False
        
        try:
            f = open(self.file_path, "a+")
            f.close()
            self.__file_obj = open(self.file_path, self.mode, *self.args, **self.kargs)
        except (OSError, IOError) as e:
            print("Unable to open configuration file: %s \"%s\"" % (e.strerror, e.filename))
            return False
        
        try:
            self.__file_obj.seek(0,2)
            if  self.__file_obj.tell() == 0:
                self.__create_initial_config()
            else:
                self.load_config()
        except (OSError, IOError) as e:
            print("The file was somehow closed straight after it was opened or there was some other error. Something is very wrong here as this shouldn't happen.", e)
            return False
        
        return True

    # def __enter(self):
    #     return self.__file_obj

    # def __exit__(self, *args):
    #     if  self.save_config():
    #         self.__file_obj.close()
    #     else:
    #         print("WARNING: Your config file was not saved!")
    
    def __create_initial_config(self):
        self.__config = {
            "last_tab" : "applications",
            "last_bridge" : "default",
            "last_vglcompress" : "default",
            "presets" : []
        }

        self.save_config()
    
    def try_reload_file(self):
        if  self.__file_obj.closed == False:
            self.close()
        if  self.__create_or_open():
            print("Config file reloaded.")
        else:
            print("Unable to reload config file.")

    def load_config(self):
        try:
            self.__file_obj.seek(0)
            self.__config = json.load(self.__file_obj)
            self.__config_available = True
        except ValueError as e:
            print("An error occurred while decoding the config file:", e)
            print("Your config might be corrupted.")
            self.__config = None
            self.__config_available = False
            return False
        except (OSError, IOError) as e:
            print("An error occurred while reading the config from the disk:", e)
            return False

        return True
    
    def save_config(self):
        try:
            json_config = json.dumps(self.__config)
            self.__file_obj.seek(0)
            self.__file_obj.write(json_config)
            self.__file_obj.seek(len(json_config))
            self.__file_obj.truncate()
        except (ValueError, OSError, IOError) as e:
            print("An error occurred while saving the config to the disk:", e)
            return False
        
        return True

    def get_option(self, option):
        if self.__config == None or self.__file_obj.closed:
            print("The config file has been closed or is otherwise unavailable.")
            return False
        else:
            if  option in self.__config:
                return self.__config[option]
            else:
                print("Option does not exist.")
                return None
    
    def set_option(self, option, value):
        if self.__config == None or self.__file_obj.closed:
            print("The config file has been closed or is otherwise unavailable.")
            return False
        else:
            self.__config[option] = value # I should probably do more validation later I guess.
            return True
    
    def close(self, *args):
        if  self.save_config() == False:
            print("WARNING: Your config file was not saved!")

        self.__file_obj.close()
        self.__config == None