import json
import requests ,base64
import os
def analyze(image_path):
    print(image_path)
    with open(image_path, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    print("hello")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps( { "img": ["data:image/jpeg;base64,"+ im_b64]})
    print("hello2")
    
    response = requests.post('http://MLSERVICE_IP:5010/analyze', data=payload, headers=headers)
    
    print("hello3")
    
    try:
        data = response.json()
        print(data) 
        return data
    except requests.exceptions.RequestException:
        print(response.text)
        return None

img = 'uploads/2022200819PicsArt_05-02-09.14.10.jpg'
fg = analyze(img)