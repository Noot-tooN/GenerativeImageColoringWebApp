from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import base64
from PIL import Image
import io

def home_page(request):
    return render(request, "home.html", {"carousel_items": [
        {"bw_image": "cherry_tree_bw.jpeg", "image": "cherry_tree.jpeg", "original_link": "https://treesunlimitednj.com/wp-content/uploads/planting-cherry-tree.jpg"},
        {"bw_image": "doggy_bw.jpeg", "image": "doggy.jpeg", "original_link": "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F28%2F2020%2F10%2F13%2Fcorgi-dog-POPDOGNAME1020.jpg"},
        {"bw_image": "horsey_bw.jpeg", "image": "horsey.jpeg", "original_link": "https://www.lifepixel.com/wp-content/uploads/2017/08/Grayscale-Conversion-Lightroom.jpg"},
        {"bw_image": "woman_field_bw.jpeg", "image": "woman_field.jpeg", "original_link": "https://images.unsplash.com/photo-1561709316-d1bc557d47de?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Nnx8d29tYW4lMjBpbiUyMGZsb3dlciUyMGZpZWxkfGVufDB8fDB8&ixlib=rb-1.2.1&w=1000&q=80"},
        {"bw_image": "venice_bw.jpeg", "image": "venice.jpeg", "original_link": "https://thumbs.dreamstime.com/b/canal-de-venise-et-gondole-bateaux-du-pont-rialto-en-noir-blanc-111434192.jpg"},
        {"bw_image": "doggy2_bw.jpeg", "image": "doggy2.jpeg", "original_link": "https://www.maxpixel.net/static/photo/1x/Animal-Pet-Grayscale-Dog-5423577.jpg"},
        {"bw_image": "tree_bw.jpeg", "image": "tree.jpeg", "original_link": "https://res.cloudinary.com/jerrick/image/upload/c_scale,q_auto/5e2e0380084ba2001cc211d2.jpg"},
    ]})

@login_required()
def colorization_page(request):
    if request.method == "GET":
        return render(request, "colorization.html", {})
    else:
        image = request.POST.get("image_for_colorization", "")
        if image == "":
            return render(request, "colorization.html", {"colorization_err_status": "Invalid image!"})

        picture_width = ""
        picture_height = ""
        picture_dimensions = request.POST.get("picture_dimensions", "")
        if picture_dimensions:
            picture_width = picture_dimensions.split("x")[0]
            picture_height = picture_dimensions.split("x")[1]
        
        selected_permission_level = request.POST.get("network_select", "")

        cut_image = image.split(",")
        bajts = base64.b64decode(cut_image[1])

        base_url = "http://185.27.128.249:8080/api/"
        files = {'black-white-photo': bajts}
        # data = {"permission_level": request.user.permission_level}
        data = {"permission_level": int(selected_permission_level)}

        my_response = requests.post(base_url + "color_image/", files=files, data=data)
        if not my_response.ok:
            return render(request, "colorization.html", {"colorization_err_status": "Failed to upload the image!", "original_image": image, "picture_dimensions": picture_dimensions})
        
        encoded_image = base64.b64encode(my_response.content)
        encoded_image = "data:image/jpeg;base64," + encoded_image.decode("utf-8")

        converted_image = Image.open(io.BytesIO(my_response.content), "r").convert("L")
        converted_bytes_arr = io.BytesIO()
        converted_image.save(converted_bytes_arr, "JPEG")
        converted_bytes = converted_bytes_arr.getvalue()
        gray_image = base64.b64encode(converted_bytes)
        gray_image = "data:image/jpeg;base64," + gray_image.decode("utf-8")

        return render(request, "colorization.html", {"generated_image": encoded_image, "gray_image": gray_image, "original_image": image,
                        "picture_width": picture_width, "picture_height": picture_height, "picture_dimensions": picture_dimensions})