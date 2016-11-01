#!/usr/bin/python3

import os, glob

def genapplist():
    apps = []

    desktopfiledir = "/usr/share/applications"

    for filename in glob.glob(os.path.join(desktopfiledir, "*.desktop")):
        f = open(filename, "r")
        name = ""
        execpath = ""
        execargs = ""
        cat = ""
        icon = ""

        for i in f.read().splitlines():
            string = i.split("=",1)

            if (string[0] == "Name") and (name == ""):
                name = string[1].replace("(", "[").replace(")", "]")
            elif ((string[0] == "Exec") or (string[0] == "TryExec")) and (execpath == ""):
                execline = string[1].replace(" %u", "").replace(" %U", "").replace(" %f", "").replace(" %F", "")
                execspl = execline.split(' ', 1)
                execpath = execspl[0]
                if len(execspl) > 1:
                    execargs = execspl[1]
            elif (string[0] == "Categories") and (cat == ""):
                cat = string[1]
            elif (string[0] == "Icon") and (icon == ""):
                icon = string[1]

            #print("{}\n\tCategories: {}\n\tExec: {}\n".format(name, cat, execpath))
            #print("[exec] ({}) {{{}}}".format(name, execpath))

        if cat == "":
            f.close()
            continue

        #rawlist.write(name + " | " + cat + " | " + execpath + "\n")

        #maincats = ["AudioVideo", "Multimedia", "Development", "Education", "Game", "Graphics", "Network", "Office", "Science", "Settings", "System", "Utility"]

        maincats = ["Game", "Games"]

        cat = cat.split(";")
        for i in cat:
            if i in maincats:
                apps.append((name, execpath, execargs, icon))
                #print(icon)
                #print("Found application: {} [{}] [{}] ({} {})".format(name, icon, i, execpath, execargs))

        f.close()
    return apps
