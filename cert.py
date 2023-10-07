#!/usr/bin/env python

from lib import pdftk, fdf

pdf_fields = pdftk.inspect_pdf_fields("./sample_cert.pdf")

da = [{"name": "siddhant", "reg": 192301}, {"name": "kush", "reg": 390321}]

for data in da:
    fdf_str = fdf.generate_fdf(pdf_fields, data)
    pdftk.fill_form("./sample_cert.pdf", fdf_str, f"{data['name']}.pdf")
