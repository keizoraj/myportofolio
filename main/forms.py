from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput
from main.models import Project, Experience, Education
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Experience",
            "description": "Deskripsi Experience",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Product Management Academy Staff",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 4,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.jpg",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "description",
            "started_at",
            "ended_at",
        ]

        labels = {
            "institution": "Nama Institusi",
            "degree": "Jenjang / Program Studi",
            "description": "Deskripsi Pendidikan",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "S1 Sistem Informasi",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pendidikanmu",
                    "rows": 4,
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

    def clean_institution(self):
        institution = strip_tags(
            self.cleaned_data["institution"]
        ).strip()

        if not institution:
            raise ValidationError(
                "Nama institusi tidak boleh hanya berisi tag HTML."
            )

        return institution

    def clean_degree(self):
        degree = strip_tags(
            self.cleaned_data["degree"]
        ).strip()

        if not degree:
            raise ValidationError(
                "Jenjang / program studi tidak boleh hanya berisi tag HTML."
            )

        return degree

    def clean_description(self):
        return strip_tags(
            self.cleaned_data["description"]
        ).strip()