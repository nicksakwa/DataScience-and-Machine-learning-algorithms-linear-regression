import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import io
import base64
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    full_health_data = pd.read_csv("data.csv", header=0, sep=",")

    # Correct assignment for x and y
    x = full_health_data["Average_Pulse"]
    y = full_health_data["Calorie_Burnage"]

    # Perform linear regression
    slope, intercept, r, p, std_err = stats.linregress(x, y)

    # Define the regression function
    def myfunc(x_val):
        return slope * x_val + intercept

    # Generate model predictions
    mymodel = list(map(myfunc, x))

    # Create a new plot figure
    plt.figure(figsize=(10, 6)) # Optional: set figure size

    # Create the plot
    plt.scatter(x, y, label='Actual Data')
    plt.plot(x, mymodel, color='red', label='Regression Line')
    plt.ylim(ymin=0, ymax=2000)
    plt.xlim(xmin=0, xmax=200)
    plt.xlabel("Average_Pulse")
    plt.ylabel("Calorie_Burnage")
    plt.title("Linear Regression: Calorie Burnage vs. Average Pulse")
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO object (in-memory)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png') # <--- Save the figure here
    img_buf.seek(0) # Rewind the buffer to the beginning
    plt.close() # Close the plot after saving to free up memory

    # Encode the image to base64
    plot_url = base64.b64encode(img_buf.getvalue()).decode('utf8')

    # Render the HTML template, passing the image data and statistics
    return render_template('index.html', plot_url=plot_url,
                           slope=f"{slope:.2f}",
                           intercept=f"{intercept:.2f}",
                           r_value=f"{r:.2f}", # <--- Added missing comma
                           p_value=f"{p:.3f}",
                           std_err=f"{std_err:.2f}")

if __name__ == '__main__':
    app.run(debug=True)