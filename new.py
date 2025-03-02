import requests

latitude = 28.6139  # Example Latitude (New Delhi)
longitude = 77.2090  # Example Longitude (New Delhi)
radius = 5000  # 5km radius

overpass_url = "http://overpass-api.de/api/interpreter"
query = f"""
[out:json];
node["amenity"="restaurant"](around:{radius},{latitude},{longitude});
out;
"""

response = requests.get(overpass_url, params={"data": query})
data = response.json()

# Extract restaurant names
restaurants = []
for element in data.get("elements", []):
    name = element.get("tags", {}).get("name", "Unnamed Restaurant")
    restaurants.append(name)

# Print the top 5 restaurants
print("Top 5 Restaurants Near You:")
for i, restaurant in enumerate(restaurants[:5], start=1):
    print(f"{i}. {restaurant}")
