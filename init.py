# pip install internetarchive

import os
import json
import internetarchive
from pathlib import Path

masterurls = [
	["world-ends-with-you-the", "nds"],
	["psx-chd-roms-b", "psx"]
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

for u in range(0, len(masterurls)):
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
                        "catagory": [ext],
                        "console": ["3DS"],
                        "last_updated": "Sometime",
                        "title": clean_name,
                        "version": "v1"
                    },
                    "script":[{
                        "file": file.url,
                        "message": "Downloading...",
                        "output": downloadpath+"/"+clean_name,
                        "type": "downloadFile"
                    }]
                })

open("epicgoodies.unistore", "w").write(json.dumps(templatejson, indent="\t"))
