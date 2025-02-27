from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Location
import subprocess
import json

# Create your views here.
def autocomplete(request):
    query = request.GET.get("q", "").strip()

    if query:
        results = list(Location.objects.filter(
            Q(city__icontains=query) |
            Q(country__icontains=query)|
            Q(iso3__icontains=query)
        ).values("id", "city", "country", "iso3")[:10])

        print("Results found:", results)

        return JsonResponse(results, safe=False)
    
    return JsonResponse([], safe=False)

def autocomplete_form(request):
    return render(request, 'index.html')


def process_location(request):
    location = request.GET.get("location", "").strip()

    if not location:
        return JsonResponse({"error": "No location provided"}, status=400)

    try:
        result = subprocess.run(
            ["python3", "scripts/haversine.py", location],
            capture_output=True, text=True, check=True
        )

        output_json = result.stdout.strip()

        # ✅ Convert script output from JSON to Python dictionary
        data = json.loads(output_json)

        return JsonResponse(data)

    except subprocess.CalledProcessError as e:
        return JsonResponse({"error": f"Script error: {e}"}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid response from script"}, status=500)


# def process_location(request):
#     location = request.GET.get("location", "").strip()
    
#     if not location:
#         return JsonResponse({"error": "No location provided"}, status=400)
    
#     print(f"Processing location: {location}")

#     try:
#         # Run your script (replace with actual command)
#         result = subprocess.run(["python3", "scripts/haversine.py", location], capture_output=True, text=True)
#         output = result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"

#         return JsonResponse({"result": output})

#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)