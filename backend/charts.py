import io
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt


def create_img(df):
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True
    fig = plt.figure()  # make sure to call this, in order to create a new figure
    plt.plot([1, 2])
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close(fig)
    return img_buf