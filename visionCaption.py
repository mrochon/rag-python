import os
import dotenv
import requests
import json

dotenv.load_dotenv('.env', verbose=True, override=True)

VISION_URL = os.environ["VISION_URL"]
VISION_API_KEY = os.environ["VISION_API_KEY"]

images = [
    "https://i.etsystatic.com/51286668/r/il/27eaed/6014488641/il_1588xN.6014488641_bybu.jpg",
    "https://mobileimages.lowes.com/productimages/cf75cdca-e41f-42f6-857f-aa49a5b10675/12161585.jpg",
    "https://cdnimg.webstaurantstore.com/images/products/large/758110/2572441.jpg",
    "https://cdnimg.webstaurantstore.com/images/products/large/568760/2638325.jpg",
]
def get_size(obj):
    box = obj["boundingBox"]
    # giving confidence score a bit of a boost
    return box['w'] * box['h'] * (obj['confidence'] + 1)

# &visualFeatures=brands seems to be only in 3.2, not 4.0; use training to add brands?
# url = "https://eastus.api.cognitive.microsoft.com/vision/v3.2/analyze?visualFeatures=brands"
url = f"{VISION_URL}/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=denseCaptions"
for image in images:
    image_params = {
        "url": image
    }
    response = requests.post(url=url, json=image_params, headers={"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": VISION_API_KEY})
    objects = response.json()
    sorted_objects = sorted(objects["denseCaptionsResult"]["values"], key=get_size, reverse=True)
    print(f"Image: {image}")
    for obj in sorted_objects:
        print(get_size(obj), obj['text'])
    print()