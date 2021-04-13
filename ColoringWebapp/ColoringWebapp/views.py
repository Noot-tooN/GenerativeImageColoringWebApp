from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import base64
from PIL import Image
import io

def home_page(request):
    return render(request, "home.html", {})

@login_required()
def colorization_page(request):
    if request.method == "GET":
        return render(request, "colorization.html", {})
    else:
        image = request.POST.get("image_for_colorization", "")
        if image == "":
            return render(request, "colorization.html", {"colorization_err_status": "Invalid image!"})

        cut_image = image.split(",")
        bajts = base64.b64decode(cut_image[1])

        base_url = "http://185.27.128.249:8080/api/"
        files = {'black-white-photo': bajts}
        data = {"permission_level": request.user.permission_level}

        my_response = requests.post(base_url + "color_image/", files=files, data=data)
        if not my_response.ok:
            return render(request, "colorization.html", {"colorization_err_status": "Failed to upload the image!", "original_image": image})
        
        encoded_image = base64.b64encode(my_response.content)
        encoded_image = "data:image/jpeg;base64," + encoded_image.decode("utf-8")

        converted_image = Image.open(io.BytesIO(my_response.content), "r").convert("L")
        converted_bytes_arr = io.BytesIO()
        converted_image.save(converted_bytes_arr, "JPEG")
        converted_bytes = converted_bytes_arr.getvalue()
        gray_image = base64.b64encode(converted_bytes)
        gray_image = "data:image/jpeg;base64," + gray_image.decode("utf-8")

        return render(request, "colorization.html", {"generated_image": encoded_image, "gray_image": gray_image, "original_image": image})