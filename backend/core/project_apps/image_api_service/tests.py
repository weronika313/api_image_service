import datetime
import io
from time import sleep

from PIL import Image as Img_pil
from django.test import TestCase

from project_apps.users.models import CustomUser as User

from project_apps.plans.models import Plan, ThumbnailSize

from project_apps.images.models import Image
from rest_framework.reverse import reverse


def generate_image_file():
    file = io.BytesIO()
    image = Img_pil.new('RGBA', size=(500, 500), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


class ImageViewSetTestCase(TestCase):
    def setUp(self):
        thumbnail_size_small = ThumbnailSize.objects.create(size=200)
        thumbnail_size_big = ThumbnailSize.objects.create(size=400)

        self.basic_plan = Plan.objects.create(name="Basic",
                                              has_access_to_org_img=False,
                                              can_generate_expiring_links=False)

        self.premium_plan = Plan.objects.create(name="Premium",
                                                has_access_to_org_img=True,
                                                can_generate_expiring_links=False
                                                )

        self.enterprise_plan = Plan.objects.create(name="Enterprise",
                                                   has_access_to_org_img=True,
                                                   can_generate_expiring_links=True
                                                   )

        self.basic_plan.available_thumbnail_sizes.add(thumbnail_size_small)
        self.basic_plan.save()

        self.premium_plan.available_thumbnail_sizes.add(thumbnail_size_small, thumbnail_size_big)
        self.premium_plan.save()

        self.enterprise_plan.available_thumbnail_sizes.add(thumbnail_size_small, thumbnail_size_big)
        self.enterprise_plan.save()

        self.username = 'testuser'
        self.password = 'testpass'

        self.user = User.objects.create_user(self.username, password=self.password, plan=self.basic_plan)

    def test_image_upload(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        img_to_upload = generate_image_file()

        input_data = {
            "title": "test",
            "description": "test",
            "image": img_to_upload
        }

        upload_img_url = "/api/v1/images"
        response = self.client.post(upload_img_url, data=input_data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'test')
        self.assertEqual(response.data['owner'], self.user.pk)

    def test_get_expiring_link_without_permission(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        get_expiring_link_url = "/api/v1/images/1/generate_expiring_link"

        input_data = {
            'time_to_expiry': 30
        }
        response = self.client.post(get_expiring_link_url, data=input_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_get_expiring_link(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        # change plan to enterprise to get access to the functionality
        self.user.plan = self.enterprise_plan
        self.user.save()

        img_to_upload = generate_image_file()

        input_data = {
            "title": "test",
            "description": "test",
            "image": img_to_upload
        }

        upload_img_url = "/api/v1/images"
        self.client.post(upload_img_url, data=input_data, format='json')

        get_expiring_link_url = "/api/v1/images/1/generate_expiring_link"

        input_data = {
            'time_to_expiry': 300
        }
        response = self.client.post(get_expiring_link_url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)

        input_data = {
            'time_to_expiry': 30000
        }
        response = self.client.post(get_expiring_link_url, data=input_data, format='json')
        self.assertEqual(response.status_code, 200)

        # expiry time out of range - 299s

        input_data = {
            'time_to_expiry': 299
        }

        response = self.client.post(get_expiring_link_url, data=input_data, format='json')
        self.assertEqual(response.status_code, 400)

        # expiry time out of range - 30 001s

        input_data = {
            'time_to_expiry': 30001
        }

        response = self.client.post(get_expiring_link_url, data=input_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_original_img_link(self):
        logged_in = self.client.login(username=self.username, password=self.password)

        # change plan to premium to get link to original img
        self.user.plan = self.premium_plan
        self.user.save()

        img_to_upload = generate_image_file()

        input_data = {
            "title": "test",
            "description": "test",
            "image": img_to_upload
        }

        upload_img_url = "/api/v1/images"
        response = self.client.post(upload_img_url, data=input_data, format='json')

        image_in_response = True if "image" in response.data else False

        self.assertTrue(image_in_response)


class ExpiringLinkApiViewTestCase(TestCase):
    def setUp(self):
        self.basic_plan = Plan.objects.create(name="Basic",
                                              has_access_to_org_img=False,
                                              can_generate_expiring_links=True)

        self.username = 'testuser'
        self.password = 'testpass'

        self.user = User.objects.create_user(self.username, password=self.password, plan=self.basic_plan)

        img_to_upload = generate_image_file()

        input_data = {
            "title": "test",
            "description": "test",
            "image": img_to_upload
        }

        upload_img_url = "/api/v1/images"
        logged_in = self.client.login(username=self.username, password=self.password)
        self.client.post(upload_img_url, data=input_data, format='json')

    def test_expiring_link(self):
        time = datetime.datetime.now() + datetime.timedelta(seconds=1)

        image = Image.objects.filter(owner = self.user.id).first()
        expiring_link_url = reverse(
            "expiring-link",
            kwargs={"id": image.id, 'expiring_time': time},
        )

        response = self.client.get(expiring_link_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")


