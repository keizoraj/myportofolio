import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.forms import ExperienceForm, EducationForm
from main.models import Experience, Project, Education


class MainTest(TestCase):
    def setUp(self):
        self.started_at = timezone.now()

        self.experience = Experience.objects.create(
            title="Product Management Academy Staff",
            description=(
                "Contributing as a staff member in the "
                "Product Management Academy."
            ),
            category="part-time",
            started_at=self.started_at,
        )

    # =========================
    # MAIN PAGE
    # =========================

    def test_main_url_is_accessible(self):
        response = self.client.get(
            reverse("main:show_main")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(
            response,
            self.experience.title
        )
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"'
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get(
            "/halaman-yang-tidak-ada/"
        )

        self.assertEqual(response.status_code, 404)

    # =========================
    # EXPERIENCE
    # =========================

    def test_experience_model(self):
        self.assertEqual(
            str(self.experience),
            "Product Management Academy Staff"
        )
        self.assertEqual(
            self.experience.category,
            "part-time"
        )
        self.assertTrue(
            self.experience.is_ongoing
        )

    def test_experience_page(self):
        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "experience.html"
        )
        self.assertContains(
            response,
            self.experience.title
        )
        self.assertContains(
            response,
            self.experience.description
        )
        self.assertContains(
            response,
            "Part-Time"
        )
        self.assertContains(
            response,
            "Sekarang"
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan."
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        response = self.client.get(
            reverse("main:show_experience")
        )

        self.experience.refresh_from_db()

        self.assertFalse(
            self.experience.is_ongoing
        )

        formatted_date = self.experience.ended_at.strftime(
            "%B %Y"
        )

        self.assertContains(
            response,
            formatted_date
        )
        self.assertNotContains(
            response,
            "Sekarang"
        )

    # =========================
    # EXPERIENCE FORM
    # =========================

    def test_experience_form_is_valid(self):
        form_data = {
            "title": "New Experience",
            "description": "Testing ExperienceForm.",
            "category": "internship",
            "thumbnail": "https://example.com/image.jpg",
            "started_at": "2026-09-01T10:00",
            "ended_at": "",
        }

        form = ExperienceForm(data=form_data)

        self.assertTrue(form.is_valid())

    # =========================
    # EDUCATION MODEL
    # =========================

    def test_education_model(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description=(
                "Fakultas Ilmu Komputer, "
                "Universitas Indonesia."
            ),
            started_at=self.started_at,
        )

        self.assertEqual(
            str(education),
            "S1 Sistem Informasi - Universitas Indonesia"
        )
        self.assertTrue(
            education.is_ongoing
        )

    # =========================
    # EDUCATION PAGE
    # =========================

    def test_education_page(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=self.started_at,
        )

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertTemplateUsed(
            response,
            "education.html"
        )
        self.assertContains(
            response,
            education.institution
        )
        self.assertContains(
            response,
            education.degree
        )
        self.assertContains(
            response,
            education.description
        )
        self.assertContains(
            response,
            "Sekarang"
        )

    def test_empty_education_page(self):
        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertContains(
            response,
            "Belum ada data pendidikan yang ditambahkan."
        )

    # =========================
    # EDUCATION FORM
    # =========================

    def test_education_form_is_valid(self):
        form_data = {
            "institution": "Universitas Indonesia",
            "degree": "S1 Sistem Informasi",
            "description": "Fakultas Ilmu Komputer.",
            "started_at": "2025-09-01T08:00",
            "ended_at": "",
        }

        form = EducationForm(data=form_data)

        self.assertTrue(
            form.is_valid()
        )

    # =========================
    # CREATE EDUCATION
    # =========================

    def test_create_education(self):
        data = {
            "institution": "Universitas Indonesia",
            "degree": "S1 Sistem Informasi",
            "description": "Fakultas Ilmu Komputer.",
            "started_at": "2025-09-01T08:00",
            "ended_at": "",
        }

        response = self.client.post(
            reverse("main:create_education"),
            data
        )

        self.assertRedirects(
            response,
            reverse("main:show_education")
        )

        self.assertTrue(
            Education.objects.filter(
                institution="Universitas Indonesia",
                degree="S1 Sistem Informasi",
            ).exists()
        )

    # =========================
    # UPDATE EDUCATION
    # =========================

    def test_update_education(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=self.started_at,
        )

        data = {
            "institution": "Universitas Indonesia",
            "degree": "S1 Sistem Informasi",
            "description": "Updated education description.",
            "started_at": "2025-09-01T08:00",
            "ended_at": "",
        }

        response = self.client.post(
            reverse(
                "main:update_education",
                args=[education.id]
            ),
            data
        )

        self.assertRedirects(
            response,
            reverse("main:show_education")
        )

        education.refresh_from_db()

        self.assertEqual(
            education.description,
            "Updated education description."
        )

    # =========================
    # DELETE EDUCATION
    # =========================

    def test_delete_education(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=self.started_at,
        )

        education_id = education.id

        response = self.client.post(
            reverse(
                "main:delete_education",
                args=[education_id]
            )
        )

        self.assertRedirects(
            response,
            reverse("main:show_education")
        )

        self.assertFalse(
            Education.objects.filter(
                id=education_id
            ).exists()
        )

    # =========================
    # EDUCATION JSON
    # =========================

    def test_education_json(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=self.started_at,
        )

        response = self.client.get(
            reverse("main:get_education_json")
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            response["Content-Type"],
            "application/json"
        )

        data = json.loads(response.content)

        self.assertEqual(
            len(data),
            1
        )
        self.assertEqual(
            data[0]["model"],
            "main.education"
        )
        self.assertEqual(
            data[0]["fields"]["institution"],
            education.institution
        )
        self.assertEqual(
            data[0]["fields"]["degree"],
            education.degree
        )

    def test_education_page_uses_json_data(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fakultas Ilmu Komputer.",
            started_at=self.started_at,
        )

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        # Data berhasil ditampilkan setelah
        # proses JSON dan deserialization.
        self.assertContains(
            response,
            education.institution
        )
        self.assertContains(
            response,
            education.degree
        )

    # =========================
    # PROJECT
    # =========================

    def test_projects_page_is_accessible(self):
        response = self.client.get(
            reverse("main:show_projects")
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertTemplateUsed(
            response,
            "projects.html"
        )

    def test_project_data_appears_on_page(self):
        project = Project.objects.create(
            title="Greenspark",
            description=(
                "An application dedicated to helping "
                "households manage their wastes."
            ),
            tech_stack="Django, Python, HTML, CSS",
            project_url="https://github.com/example/greenspark",
            project_image_url="https://example.com/greenspark.jpg",
        )

        response = self.client.get(
            reverse("main:show_projects")
        )

        self.assertContains(
            response,
            project.title
        )
        self.assertContains(
            response,
            project.description
        )
        self.assertContains(
            response,
            project.tech_stack
        )

    def test_empty_project_page(self):
        Project.objects.all().delete()

        response = self.client.get(
            reverse("main:show_projects")
        )

        self.assertContains(
            response,
            "Belum ada proyek yang ditambahkan."
        )