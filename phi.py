import aiohttp
import asyncio
import sys
from PhigrosLibrary import B19Class

async def main(sessionToken):
    async with aiohttp.ClientSession() as client:
        b19Class = B19Class(client)
        b19Class.read_difficulty(r"D:/lin\difficulty.tsv")
        playerId = await b19Class.get_playerId(sessionToken)
        print(playerId)
        summary = await b19Class.get_summary(sessionToken)
        print(summary)
        b19 = await b19Class.get_b19(summary["url"])
    rks = 0
    for song in b19:
        rks += song["rks"]
        print(song)
    print(rks/20)

s = "1uys8oql063ufi2vugsjyiczi"
#s = "6r909yj9mlnvxag4ryeyu6sxd"
if len(sys.argv) == 2:
    s = sys.argv[1]
asyncio.run(main(s))
