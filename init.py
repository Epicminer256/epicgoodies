# pip install internetarchive

import os
import time
import json
import internetarchive
from pathlib import Path

masterurls = [
	["world-ends-with-you-the", "nds"],
    ["blockbuster-competition-2-nba-jam-judge-dredd-jue", "md"],
    ["MySnesRoms", "smc"],
    ["tsf-2002-gba-roms-collection", "gba"],
    ["n64-roms_202405", "n64"],
	["psx-chd-roms-a", "psx"],
	["psx-chd-roms-b", "psx"],
	["psx-chd-roms-c", "psx"],
	["psx-chd-roms-d", "psx"],
	["psx-chd-roms-e", "psx"],
	["psx-chd-roms-f", "psx"],
	["psx-chd-roms-g", "psx"],
	["psx-chd-roms-h", "psx"],
	["psx-chd-roms-i", "psx"],
	["psx-chd-roms-j", "psx"],
	["psx-chd-roms-k", "psx"],
	["psx-chd-roms-l", "psx"],
	["psx-chd-roms-m", "psx"],
	["psx-chd-roms-n", "psx"],
	["psx-chd-roms-o", "psx"],
	["psx-chd-roms-p", "psx"],
	["psx-chd-roms-q", "psx"],
	["psx-chd-roms-r", "psx"],
	["psx-chd-roms-s", "psx"],
	["psx-chd-roms-t", "psx"],
	["psx-chd-roms-u", "psx"],
	["psx-chd-roms-v", "psx"],
	["psx-chd-roms-w", "psx"],
	["psx-chd-roms-x", "psx"],
	["psx-chd-roms-y", "psx"],
	["psx-chd-roms-z", "psx"]
]

fileTypesAccepted = [
	"3ds",
	"3dsx",
	"cia",
	"nds",
	"gb",
	"gbc",
	"gba",
	"nes",
	"fds",
	"sfc",
	"smc",

	"md",
	"gen",
	"bin",
	"smd",
	"sms",
	"gg",

	"pce",

	"ngp",
	"ngc",

	"ws",
	"wsc",

	"a26",

	"iso",
	"chd",
	"ccd",
	"img",
	"mdf",
]

templatejson = json.loads(open("base.json").read())
templatejson["storeInfo"]["revision"]+=1
open("base.json", "w").write(json.dumps(templatejson))

print("Working on que, ETA is "+len(masterurls)*10+"seconds")

for u in range(0, len(masterurls)):
    print("working on "+masterurls[u][0])
    item=internetarchive.get_item(masterurls[u][0])
    downloadpath="sdmc:/roms/"+masterurls[u][1]
    files = item.get_files()
    for file in files:
        clean_name = os.path.basename(file.name)
        for ext in fileTypesAccepted:
            if Path(file.name).suffix.lower() == "."+ext:
                templatejson["storeContent"].append({
                    "info": {
                        "author": "epicminer256",
                        "console": [ext],
                        "last_updated": "Sometime",
                        "title": clean_name,
                        "version": "v1"
                    },
                    "Download File":[{
                        "file": file.url,
                        "message": "Downloading...",
                        "output": downloadpath+"/"+clean_name,
                        "type": "downloadFile"
                    }]
                })
    print("sleeping for 5 seconds...")
    time.sleep(5)
    print("continuing")

# open("epicgoodies.unistore", "w").write(json.dumps(templatejson, indent="\t"))
open("epicgoodies.unistore", "w").write(json.dumps(templatejson))
