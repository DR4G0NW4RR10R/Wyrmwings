from PIL import Image as PIL_Image
from math import ceil

class CommandMaker:

    def __init__(self):
        self.Z_OFFSET = -0.2

    def imageToCommands(self, im_name, filepath, tagname, scoreboardname):

        im = PIL_Image.open(im_name)

        size = im.size
        middle_x = size[0] / 2
        middle_y = size[1] / 2

        with open(filepath, "w") as tick:
            tick.write(f"tag @a[scores={{{scoreboardname}-toggle=1..}}, tag={tagname}] add {tagname}-inp\n") # add transition tag to tagged players who trigger
            tick.write(f"tag @a[scores={{{scoreboardname}-toggle=1..}}, tag=!{tagname}] add {tagname}\n") # add tag to untagged players who triggered
            tick.write(f"tag @a[scores={{{scoreboardname}-toggle=1..}}, tag={tagname}-inp] remove {tagname}\n") # untag transitioning players
            tick.write(f"tag @a[scores={{{scoreboardname}-toggle=1..}}, tag={tagname}-inp] remove {tagname}-inp\n") # remove transition tag
            tick.write(f"scoreboard players reset @a[scores={{{scoreboardname}-toggle=1..}}] {scoreboardname}-toggle\n") # reset trigger
            tick.write(f"scoreboard players enable @a {scoreboardname}-toggle\n") # enable trigger for all players


            for y in range(im.size[1]):
                for x in range(im.size[0]):
                    dx = ceil(x - middle_x)/10
                    dy = ceil(y - middle_y)/10
                    dy *= -1

                    p = im.getpixel((x,y))

                    skip = False
                    
                    try:
                        skip = (p[3] != 255) # type: ignore
                    except:
                        skip = False

                    if skip == False: # type: ignore
                        # print(f"execute at @a[tag=test] positioned ^ ^ ^{Z_OFFSET} positioned ~ ~1.6 ~ run particle dust{{color:[{p[0]/255},{p[1]/255},{p[2]/255}],scale:0.5}} ~{dx} ~{dy} ~ 0 0 0 0 1")
                        tick.write(f"execute at @a[tag={tagname}] positioned ~ ~1 ~ run particle dust{{color:[{p[0]/255},{p[1]/255},{p[2]/255}],scale:0.6}} ^{dx} ^{dy} ^{self.Z_OFFSET} 0 0 0 0 1\n") # type: ignore
        
        return
