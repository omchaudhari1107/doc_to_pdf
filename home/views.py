from django.http import HttpResponse
from django.shortcuts import render
from docx2pdf import convert
import os
import tempfile
import zipfile
def home(request):
    if request.method == 'POST' and request.FILES.getlist('doc') :
        pdf_files = []  # List to store paths of converted PDF files

        for file in request.FILES.getlist('doc'):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_doc:
                temp_doc.write(file.read())
                temp_doc_path = temp_doc.name

            try:
                convert(temp_doc_path)
                pdf_path = temp_doc_path.replace('.docx', '.pdf')
                pdf_files.append(pdf_path)
            finally:
                os.remove(temp_doc_path)

        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="converted_files.zip"'

        with zipfile.ZipFile(response, 'w') as zip_file:
            for pdf_file in pdf_files:
                zip_file.write(pdf_file, os.path.basename(pdf_file))

        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                os.remove(pdf_file)

        return response
    else:
        HttpResponse('bad request')
    return render(request, 'index.html')
