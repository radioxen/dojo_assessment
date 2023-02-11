import aiohttp
import asyncio
from constants import *


google_maps_direction = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}&mode={}&departure_time={}"


async def get_directions(session, item):

    print(item)
    direction_driving = google_maps_direction.format(item[0], item[1], api_key, mode_drive, 1678224600)
    direction_transit = google_maps_direction.format(item[0], item[1], api_key, mode_transit, 1678224600)
    async with session.get(direction_driving) as resp:
        driving = await resp.json()
        by_car = driving["routes"][0]["legs"][0]["duration"]["value"]
    async with session.get(direction_transit) as resp:
        transit = await resp.json()
        by_transit = transit["routes"][0]["legs"][0]["duration"]["value"]

    return {"home": item[0],
            "target": item[1],
            "duration": {
                "driving" : by_car,
            "transit": by_transit,
            "optimum_method" : "driving" if int(by_car) < by_transit else "transit",
            "min_duration" : min(by_car, by_transit),
            }
    }


async def direction_main(address_pairs):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for pair in address_pairs:

            tasks.append(asyncio.ensure_future(get_directions(session, pair)))

        results = await asyncio.gather(*tasks)

    return list(results)