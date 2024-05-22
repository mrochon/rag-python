import os
import dotenv
import requests
import json

dotenv.load_dotenv('.env', verbose=True, override=True)

VISION_URL = os.environ["VISION_URL"]
VISION_API_KEY = os.environ["VISION_API_KEY"]

images = [
    'file:./data/screwdriver.png',
    'file:./data/list.png',
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
n = 1
for image in images:
    if image.startswith('file:'):
        with open(image[5:], 'rb') as f:
            data = f.read()
        response = requests.post(url=url, data=data, headers={"Content-Type": "application/octet-stream", "Ocp-Apim-Subscription-Key": VISION_API_KEY})
    else:
        image_params = {
            "url": image
        }
        response = requests.post(url=url, json=image_params, headers={"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": VISION_API_KEY})
    objects = response.json()
    sorted_objects = sorted(objects["denseCaptionsResult"]["values"], key=get_size, reverse=True)
    print(f"[Image {n}]({image})")
    n += 1
    highest_confidence = get_size(sorted_objects[0])
    for obj in sorted_objects:
        confidence = get_size(obj)
        if confidence < highest_confidence / 2:
            print("- Low confidence, stopping")
            break
        #highest_confidence = confidence
        print(f"- {int(get_size(obj))} - {obj['text']}")
    print()