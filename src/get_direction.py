import aiohttp
import asyncio

google_maps_direction = "https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key={}&mode={}"

async def get_directions():

    async with aiohttp.ClientSession() as session:

        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print(pokemon['name'])

asyncio.run(get_directions())