import os
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # loop over csv files in 'out' folder and plot them
    for filename in os.listdir("out"):
        if filename.endswith(".csv"):
            # Extract artist name from the filename
            artist = os.path.splitext(filename)[0]

            # Read the CSV file into a DataFrame
            df = pd.read_csv(os.path.join("out", filename))

            # Create a scatter plot of danceability vs. valence
            ax = df.plot(x="danceability", y="valence", kind="scatter")

            # Set x and y axis limits
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            # Add labels to the points using the 'name' column
            for i, point in df.iterrows():
                ax.text(point["danceability"], point["valence"], str(point["name"]))

            # Add a title to the plot
            plt.title(filename)

            # Create 'eda' folder if it doesn't exist
            if not os.path.exists("eda"):
                os.makedirs("eda")

            # Save the plot to the 'eda' folder
            plt.savefig(f"eda/{artist}.png")

            # Close the plot
            plt.close()
