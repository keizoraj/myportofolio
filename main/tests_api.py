import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone

from main.models import Project, Education


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_editor_cannot_create_education(self):
        editor = User.objects.create_user(
            username="editor_test",
            password="test-password"
        )
        editor_group, created = Group.objects.get_or_create(
            name="Editor"
        )
        editor.groups.add(editor_group)
        initial_count = Education.objects.count()

        self.client.force_authenticate(user=editor)

        response = self.client.post(
            reverse("api:education-list"),
            {
                "institution": "Test Editor",
                "degree": "Test",
                "description": "Percobaan",
                "started_at": "2026-11-04T10:00:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Education.objects.count(), initial_count)

    def test_editor_cannot_delete_education(self):
        editor = User.objects.create_user(
            username="editor_test",
            password="test-password"
        )
        editor_group, created = Group.objects.get_or_create(
            name="Editor"
        )
        editor.groups.add(editor_group)

        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=timezone.now(),
        )

        self.client.force_authenticate(user=editor)

        response = self.client.delete(
            reverse("api:education-detail", args=[education.id])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Education.objects.filter(pk=education.id).exists()
        )

    def test_visitor_can_read_education(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=timezone.now(),
        )

        response = self.client.get(reverse("api:education-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse("api:education-detail", args=[education.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_can_read_and_star_education(self):
        user = User.objects.create_user(
            username="normal_user",
            password="test-password",
        )
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=timezone.now(),
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("api:education-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse("api:education-star", args=[education.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

    def test_editor_can_update_education(self):
        editor = User.objects.create_user(
            username="editor_update",
            password="test-password",
        )
        editor_group, created = Group.objects.get_or_create(name="Editor")
        editor.groups.add(editor_group)

        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Deskripsi awal.",
            started_at=timezone.now(),
        )

        self.client.force_authenticate(user=editor)

        detail_url = reverse("api:education-detail", args=[education.id])

        response = self.client.patch(
            detail_url,
            {"description": "Deskripsi diperbarui oleh Editor."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        education.refresh_from_db()
        self.assertEqual(
            education.description,
            "Deskripsi diperbarui oleh Editor.",
        )

    def test_owner_can_create_and_delete_education(self):
        self.client.force_authenticate(user=self.owner)

        list_url = reverse("api:education-list")

        response = self.client.post(
            list_url,
            {
                "institution": "Universitas Indonesia",
                "degree": "S1 Sistem Informasi",
                "description": "Fakultas Ilmu Komputer.",
                "started_at": "2025-08-28T20:37:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        education_id = response.data["id"]
        detail_url = reverse("api:education-detail", args=[education_id])

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=education_id).exists())

    
    def test_education_guest_and_normal_user_cannot_write(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Deskripsi awal.",
            started_at=timezone.now(),
        )

        list_url = reverse("api:education-list")
        detail_url = reverse(
            "api:education-detail",
            args=[education.id],
        )

        payload = {
            "institution": "Pendidikan Baru",
            "degree": "S2",
            "description": "Deskripsi baru.",
            "started_at": timezone.now().isoformat(),
        }

        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)

            response = self.client.post(
                list_url,
                payload,
                format="json",
            )
            self.assertEqual(response.status_code, 403)

            response = self.client.patch(
                detail_url,
                {"description": "Tidak boleh diubah."},
                format="json",
            )
            self.assertEqual(response.status_code, 403)

            response = self.client.delete(detail_url)
            self.assertEqual(response.status_code, 403)

            self.assertEqual(Education.objects.count(), 1)

            education.refresh_from_db()
            self.assertEqual(
                education.description,
                "Deskripsi awal.",
            )

    
    def test_education_validation_and_html_sanitization(self):
        self.client.force_authenticate(user=self.owner)

        list_url = reverse("api:education-list")

        payload = {
            "institution": "Universitas Test",
            "degree": "S1 Testing",
            "description": "Deskripsi aman.",
            "started_at": timezone.now().isoformat(),
        }

        invalid_cases = [
            {"institution": "   "},
            {"institution": "<b></b>"},
            {"degree": "   "},
        ]

        for changes in invalid_cases:
            response = self.client.post(
                list_url,
                {**payload, **changes},
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

        self.assertEqual(Education.objects.count(), 0)

        sanitized_payload = {
            **payload,
            "institution": "<b>Test University</b>",
            "degree": "<i>Bachelor</i>",
            "description": "<p>Safe description</p>",
        }

        response = self.client.post(
            list_url,
            sanitized_payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["institution"],
            "Test University",
        )
        self.assertEqual(
            response.data["degree"],
            "Bachelor",
        )
        self.assertEqual(
            response.data["description"],
            "Safe description",
        )

    
    def test_education_star_requires_login_and_toggles(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Deskripsi pendidikan.",
            started_at=timezone.now(),
        )

        star_url = reverse(
            "api:education-star",
            args=[education.id],
        )

        response = self.client.post(star_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(star_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        self.assertTrue(
            education.starred_by.filter(
                pk=self.visitor.pk
            ).exists()
        )

        response = self.client.post(star_url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

        self.assertFalse(
            education.starred_by.filter(
                pk=self.visitor.pk
            ).exists()
        )

    
    def test_education_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            reverse("api:education-list"),
            {
                "institution": "CSRF Test",
                "degree": "S1 Testing",
                "description": "Percobaan CSRF.",
                "started_at": timezone.now().isoformat(),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(Education.objects.count(), 0)

