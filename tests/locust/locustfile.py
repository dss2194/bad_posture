from locust import HttpUser, task
import io
from PIL import Image


def create_img():

    img = Image.new("RGB", (200,200))

    buf = io.BytesIO()
    img.save(buf, format="JPEG")

    return buf.getvalue()


class PoseUser(HttpUser):

    @task
    def process_image(self):

        img = create_img()

        self.client.post(
            "/api/process-image",
            files={"file": ("img.jpg", img)}
        )