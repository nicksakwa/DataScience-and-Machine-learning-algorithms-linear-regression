import sys
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import io
import base64
from flask import Flask, render_template
app =Flask(__name__)

@app.route('/')
def index():


full_health_data=pd.read_csv("data.csv", header=0, sep=",")
y=full_health_data["Average_Pulse"]
x=full_health_data["Calorie_Burnage"]

slope, intercept, r, p, std_err=stats.linregress(x,y)
def myfunc(x_val):
    return slope*x_val + intercept
mymodel=list(map(myfunc,x))
plt.scatter(x,y)
plt.plot(x,mymodel)
plt.ylim(ymin=0, ymax=2000)
plt.xlim(xmin=0, xmax=200)
plt.xlabel("Average_Pulse")
plt.ylabel("Calorie_Burnage")
plt.title("Linear Regression: Calorie Burnage vs. Average Pulse")
plt.legend()
plt.grid(True)
img_buf=io.BytesIO()
plt.close()

plot_url=base64.b64encode(img_buf.getvalue()).decode('utf8')

return render_template('index.html', plot_url=plot_url,
                       slope=f"{slope:2f}",
                       intercept=f"{intercept:.2f}"
                       r_value=f"{r:2f}"
                       p_value=f"{p:3f}",
                       std_err=f"{std_err:.2f}")

if __name__== '__main__':
    app.run(debug=True)

