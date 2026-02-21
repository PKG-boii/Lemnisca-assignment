# utils.py
from pypdf import PdfReader

def load_pdf(path: str) -> dict:
    reader = PdfReader(path)

    text = []
    for page in reader.pages:
        if page.extract_text():
            text.append(page.extract_text())

    return {
        "text": "\n".join(text),
        "page_count": len(reader.pages)
    }



def detect_doc_category(filename: str, page_count: int, preview_text: str) -> str:
    name = filename.lower()
    text = preview_text.lower()

    # 1️⃣ Filename-based rules (highest priority)
    if any(k in name for k in ["faq", "shortcuts", "sla", "pricing", "matrix"]):
        return "REFERENCE"

    if any(k in name for k in ["guide", "tutorial", "getting_started"]):
        return "GUIDE"

    if any(k in name for k in ["policy", "handbook", "privacy", "code_of_conduct"]):
        return "POLICY"

    if any(k in name for k in ["api", "webhook", "architecture", "deployment", "infrastructure"]):
        return "TECHNICAL"

    if any(k in name for k in ["standup", "retro", "notes"]):
        return "INTERNAL_NOTES"

    if any(k in name for k in ["roadmap", "release"]):
        return "ROADMAP_RELEASES"

    # 2️⃣ Page-count fallback
    if page_count == 1:
        return "REFERENCE"

    if page_count >= 6:
        return "POLICY"

    # 3️⃣ Content keyword fallback
    if "endpoint" in text or "authorization:" in text:
        return "TECHNICAL"

    if "step 1:" in text or "navigate to" in text:
        return "GUIDE"

    if "yesterday:" in text and "today:" in text:
        return "INTERNAL_NOTES"

    # Safe default
    return "GUIDE"
