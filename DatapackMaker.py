from CommandMaker import CommandMaker
import json
import os

class DatapackMaker:
    def __init__(self, packname, namespace, imagepath, tagname, scoreboardname):
        self.packname = packname
        self.namespace = namespace
        self.imagepath = imagepath
        self.tagname = tagname
        self.scoreboardname = scoreboardname
        self.cm = CommandMaker()

        with open("config.json", "r") as f:
            self.config = json.load(f)

    def setupFolders(self): # because for some reason with open as doesn't do this automatically
        if not os.path.exists(f"{self.packname}"):
            os.mkdir(f"{self.packname}")
        if not os.path.exists(f"{self.packname}\\data\\"):
            os.mkdir(f"{self.packname}\\data")
        if not os.path.exists(f"{self.packname}\\data\\minecraft"):
            os.mkdir(f"{self.packname}\\data\\minecraft")
        if not os.path.exists(f"{self.packname}\\data\\{self.namespace}"):
            os.mkdir(f"{self.packname}\\data\\{self.namespace}")
        if not os.path.exists(f"{self.packname}\\data\\minecraft\\tags"):
            os.mkdir(f"{self.packname}\\data\\minecraft\\tags")
        if not os.path.exists(f"{self.packname}\\data\\{self.namespace}\\function"):
            os.mkdir(f"{self.packname}\\data\\{self.namespace}\\function")
        if not os.path.exists(f"{self.packname}\\data\\minecraft\\tags\\function"):
            os.mkdir(f"{self.packname}\\data\\minecraft\\tags\\function")
        
    def makeDatapack(self, description):

        self.setupFolders()

        # mcmeta file
        with open(f"{self.packname}\\pack.mcmeta", "w") as f:
            f.write(f"""{{
    "pack": {{
        "min_format": 88,
        "max_format": {self.config["max_format"]},
        "description": "Wyrmwings Datapack: {description}"
    }}
}}""")
        
        # load.json
        with open(f"{self.packname}\\data\\minecraft\\tags\\function\\load.json", "w") as f:
            f.write(f"""{{
    "values":[
      "{self.namespace}:load"
    ]
}}""")
        
        # tick.json
        with open(f"{self.packname}\\data\\minecraft\\tags\\function\\tick.json", "w") as f:
            f.write(f"""{{
    "values":[
      "{self.namespace}:tick"
    ]
}}""")
        
        # tick.mcfunction
        cm = CommandMaker()
        cm.imageToCommands(self.imagepath, f"{self.packname}\\data\\{self.namespace}\\function\\tick.mcfunction", self.tagname, self.scoreboardname)

        # load.mcfunction
        with open(f"{self.packname}\\data\\{self.namespace}\\function\\load.mcfunction", "w") as load:
            load.write(f"scoreboard objectives add {self.scoreboardname}-toggle trigger\n") # create triggerable scoreboard
            load.write(f"scoreboard players enable @a {self.scoreboardname}-toggle\n") # enable trigger

dm = DatapackMaker("testpack", "namespacetest", "image.png", "test", "wingtest")
dm.makeDatapack("ShyftSolutions Double S wings")