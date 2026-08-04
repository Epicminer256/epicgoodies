# pip install internetarchive

import os
import time
import json
import markdown
import internetarchive
from pathlib import Path
from urllib.parse import quote
from bs4 import BeautifulSoup

masterurls = [

        [
            "Nintendo_DS.unistore",
            [
                ["world-ends-with-you-the", "nds"],
            ]
        ],
        [
            "PSX_And_N64.unistore",
            [
                ["n64-roms_202405", "n64"],
                ["psx_chd_torrent_2_20220105","psx"],
            ]
        ],
        [
            "Gameboy_Roms.unistore",
            [
                # This one is spanish ["gbc_roms_202605", "gbc"],
                ["gbc-roms", "gbc"], # High file size
                ["tsf-2002-gba-roms-collection", "gba"],
                ["gameboy-best-roms", "gb"]
            ]
        ],
        [
            "Nintendo_Console_Roms.unistore",
            [
                ["action-52_202405", "nes"],
                ["MySnesRoms", "smc"]
            ]
        ],
        [
            "Sega_Console_Roms.unistore",
            [
                ["nointro.md", "md"],
            ]
        ]
]

fileTypesAccepted = [
    # i might remove this sometime, but some games are only in zip cause thats what people do
    "zip",
    "7z",

	"3ds",
	"3dsx",
	"cia",
	"nds",
    "n64",
    "z64",
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

def url_to_qr(url):
    return """<img width="300px" src="https://public-api.qr-code-generator.com/v1/create/extended?image_format=PNG&image_width=300&qr_code_text="""+quote(url)+"""&foreground_color=%23000000&background_color=%23FFFFFF&frame_name=no-frame">"""

templatejson = json.loads(open("base.json").read())
templatejson["storeInfo"]["revision"]+=1
open("base.json", "w").write(json.dumps(templatejson, indent="\t"))

print("Working on que, ETA is "+str(len(masterurls)*6)+"seconds")




inject_html = markdown.markdown(open("README.md", "r").read())

for m in range(0, len(masterurls)):
    templatejson = json.loads(open("base.json").read())
    current_unistore = masterurls[m]
    unistore_file = current_unistore[0]

    inject_html += "<div style='display:inline'> <h2>"+unistore_file+"</h2>"+url_to_qr("https://github.com/Epicminer256/epicgoodies/raw/refs/heads/main/"+unistore_file)+"</div>"

    templatejson["storeInfo"]["title"] = unistore_file
    templatejson["storeInfo"]["file"] = unistore_file
    # NOT URL ENCODED FILE
    templatejson["storeInfo"]["url"] = "https://github.com/Epicminer256/epicgoodies/raw/refs/heads/main/"+unistore_file
    current_urls = current_unistore[1]
    print(" ---- Currently making "+unistore_file+" ---- ")
    for u in range(0, len(current_urls)):
        current_masterurl = current_urls[u][0]
        current_filetype = current_urls[u][1]
        print("working on "+current_masterurl)
        item=internetarchive.get_item(current_masterurl)
        downloadpath="sdmc:/roms/"+current_filetype
        files = list(item.get_files())
        print("This URL has "+str(len(files))+" files total")
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
    open(unistore_file, "w").write(json.dumps(templatejson))

original_html = BeautifulSoup(open("index.html", "r").read(), 'lxml')
inject_html = "<main>"+inject_html+"</main>"
inject_html = BeautifulSoup(inject_html, "html.parser")
original_html.find("main").replace_with(inject_html)

open("index.html", "w").write(original_html.prettify())


# open("epicgoodies.unistore", "w").write(json.dumps(templatejson, indent="\t"))
