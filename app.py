from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("business_kpi.csv")

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)

