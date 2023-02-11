from fastapi import FastAPI, BackgroundTasks, Response
from fastapi.responses import JSONResponse
import pandas as pd
from backend.directions import direction_main
from backend.charts import create_img
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates")


app = FastAPI()


@app.get("/")
async def root():
    csv_file = "test/sample_addresses.csv"
    df = pd.read_csv(csv_file)
    values = df.values.tolist()
    response = await direction_main(address_pairs=values)
    return JSONResponse(content=response)


@app.get('/')
def get_img(background_tasks: BackgroundTasks):
    csv_file = "test/sample_addresses.csv"
    df = pd.read_csv(csv_file)
    values = df.values.tolist()
    response = await direction_main(address_pairs=values)
    df = pd.DataFrame.from_dict(response)
    img_buf = create_img()
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')