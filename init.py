# pip install internetarchive

import os
import time
import json
import internetarchive
from pathlib import Path

masterurls = [
	["world-ends-with-you-the", "nds"],
    ["n64-roms_202405", "n64"],
    ["psx_chd_torrent_2_20220105","psx"],
    ["gbc_roms_202605", "gbc"]
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

print("Working on que, ETA is "+str(len(masterurls)*6)+"seconds")

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
