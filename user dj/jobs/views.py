import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse


def home(request):
    """
    Renders the home page and processes form submission.
    """
    if request.method == "POST":
        # Read CSV file (assumed to be in the main project folder)
        csv_path = os.path.join(settings.BASE_DIR, "weather_data.csv")

        # Check if CSV exists
        if not os.path.exists(csv_path):
            return render(request, "jobs/home.html", {"error": "Weather data file not found."})

        # Redirect to results page
        return redirect("results")  # ✅ Ensure this matches `urls.py`

    return render(request, "jobs/home.html")


def results(request):
    """
    Renders the results page with weather visualizations from the CSV file.
    """
    csv_path = os.path.join(settings.BASE_DIR, "weather_data.csv")

    try:
        # Load CSV
        df = pd.read_csv(csv_path, nrows=1000)  # Load only 1000 rows

        # 🔹 Ensure correct columns exist
        required_columns = ["TMP", "WND", "SLP"]
        missing_columns = [
            col for col in required_columns if col not in df.columns]

        if missing_columns:
            return render(request, "jobs/results.html", {"error": f"Missing columns: {', '.join(missing_columns)}"})

        # 🔹 Convert index to datetime if applicable
        if "DATE" in df.columns:
            df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
            df.set_index("DATE", inplace=True)

        # 🔹 Generate graphs
        charts = {
            "temperature_chart": plot_chart(df, "TMP", "Temperature (°C)"),
            "wind_chart": plot_chart(df, "WND", "Wind Speed (km/h)"),
            "pressure_chart": plot_chart(df, "SLP", "Pressure (hPa)"),
        }

        return render(request, "jobs/results.html", {"charts": charts})

    except Exception as e:
        return render(request, "jobs/results.html", {"error": str(e)})


def plot_chart(df, column, title):
    """
    Generates a line chart for the given column and returns a base64 image string.
    """
    plt.figure(figsize=(7, 4))
    sns.lineplot(data=df, x=df.index, y=column, marker="o")
    plt.title(title)
    plt.xlabel("Date" if "DATE" in df.columns else "Time")
    plt.ylabel(column)
    plt.grid()

    # Convert plot to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return f"data:image/png;base64,{image_base64}"


def process_data(request):
    """
    Processes weather data from CSV and returns JSON response.
    """
    if request.method == "POST":
        try:
            csv_path = os.path.join(settings.BASE_DIR, "weather_data.csv")
            df = pd.read_csv(csv_path)

            return JsonResponse({"data": df.to_dict(orient="records")})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
