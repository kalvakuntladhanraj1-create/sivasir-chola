from flask import Flask, request, send_file
from docxtpl import DocxTemplate
import os
import uuid

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= TEMPLATE MAP =================
TEMPLATES = {
    "sale": "sale.docx",
    "gift": "gift.docx"
}

# ================= HOME =================
@app.route("/")
def home():
    with open(os.path.join(BASE_DIR, "html", "home.html"), encoding="utf-8") as f:
        return f.read()

# ================= LOAD FORMS =================
@app.route("/<doc_type>")
def load_form(doc_type):
    if doc_type not in TEMPLATES:
        return "Page not found", 404

    file_path = os.path.join(BASE_DIR, "html", f"{doc_type}.html")

    if not os.path.exists(file_path):
        return "HTML not found", 404

    with open(file_path, encoding="utf-8") as f:
        return f.read()

# ================= GENERATE DOC =================
@app.route("/generate/<doc_type>", methods=["POST"])
def generate(doc_type):

    if doc_type not in TEMPLATES:
        return "Invalid document type", 400

    data = request.form.to_dict()

    template_path = os.path.join(BASE_DIR, "templates_docx", TEMPLATES[doc_type])

    if not os.path.exists(template_path):
        return "Template not found", 404

    # unique output file (no overwrite)
    output_path = f"/tmp/{doc_type}_{uuid.uuid4().hex}.docx"

    try:
        doc = DocxTemplate(template_path)
        doc.render(data)
        doc.save(output_path)
    except Exception as e:
        return f"Error: {str(e)}", 500

    return send_file(output_path, as_attachment=True)


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)