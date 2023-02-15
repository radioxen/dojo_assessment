import aiohttp
import asyncio
from backend.constants import *


google_maps_direction = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}&mode={}&departure_time={}"


async def get_directions(session, item):

    direction_driving = google_maps_direction.format(
        item[1], item[2], api_key, mode_drive, 1678224600
    )
    direction_transit = google_maps_direction.format(
        item[1], item[2], api_key, mode_transit, 1678224600
    )
    async with session.get(direction_driving) as resp:
        driving = await resp.json()
    async with session.get(direction_transit) as resp:
        transit = await resp.json()

    duration_car = (
        int(driving["routes"][0]["legs"][0]["duration"]["value"])
        if driving["status"] == "OK"
        else float("+inf")
    )
    duration_transit = (
        int(transit["routes"][0]["legs"][0]["duration"]["value"])
        if transit["status"] == "OK"
        else float("+inf")
    )
    best_mode = "driving" if duration_car < duration_transit else "transit"
    distance = int(driving["routes"][0]["legs"][0]["distance"]["value"])

    return {
        "trip_id": "trip_" + str(item[0]) + " : " + str(round(distance / 1000, 1)),
        "home": item[1],
        "target": item[2],
        "distance": distance,
        "driving": (duration_car//60) + round((duration_car % 60)/60),
        "transit": (duration_transit//60) + round((duration_transit % 60)/60),
        "best_mode": best_mode,
        "min_duration": min(duration_car, duration_transit),
    }


async def direction_main(address_pairs):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for pair in address_pairs:

            tasks.append(asyncio.ensure_future(get_directions(session, pair)))

        results = await asyncio.gather(*tasks)

    return list(results)
