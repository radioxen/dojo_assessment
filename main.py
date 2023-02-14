from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
import pandas as pd
from io import BytesIO
from backend.directions import direction_main
from backend.charts import create_img


app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def main():
    """
    receives an input csv file, containing home and target address:
        - 2 columns, headers are mendatory, first column is home address and second column should be the target.
        - there is no restriction for both addresses as long as they are valid.
        - overseas travel is not implemented.
    :return: a chart, illustrating travel time of driving versus public transit for all trips.
    """
    content = """
        <body>
        <form action="/chart" enctype="multipart/form-data" method="post">
        <input name="file" type="file" single>
        <input type="submit">
        </body>
        """
    return HTMLResponse(content=content)


@app.post("/chart")
async def get_chart(file: UploadFile):
    """

    :param file: csv file for iinpu with the iinstructed format : headers, 2 columns with 1st home and 2nd target addresses,
    :return: a bar plot with units and legend, demonstrating travel time for 2 modes of transit.
    """
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    file.file.close()
    df.reset_index(inplace=True)
    values = df.values.tolist()
    response = await direction_main(address_pairs=values)
    df = pd.DataFrame.from_dict(response)
    chart = create_img(df)

    buffer = BytesIO()
    chart.savefig(buffer, format="png")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
