from django.shortcuts import redirect, render, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django import forms
from django.core.files.uploadedfile import UploadedFile

from web.settings import BASE_DIR

TEMPLATE_URL = BASE_DIR / "template.pdf"


class UploadFileForm(forms.Form):
    pdf_template = forms.FileField(
        label="PDF Template",
        allow_empty_file=False,
        required=True,
        widget=forms.FileInput(attrs={"accept": ".pdf"}),
    )


def index(request):
    upload_form = UploadFileForm()
    return render(request, "certs/index.html", {"form": upload_form})


def create(request):
    if not request.method == "POST":
        return redirect(reverse("certs:index"))

    form = UploadFileForm(request.POST, request.FILES)

    if not form.is_valid():
        return HttpResponseBadRequest(b"Invalid form")

    file: UploadedFile | None = form.cleaned_data.get("pdf_template")

    assert file is not None

    if not file.content_type == "application/pdf":
        return HttpResponseBadRequest(b"Only pdf files are allowed")

    with open(TEMPLATE_URL, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return redirect(reverse("certs:fill"))


def fill(request):
    return render(request, "certs/fill.html", {"pdf_url": TEMPLATE_URL})
