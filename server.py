import os
import sys
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

class DeJargonHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open("/Users/ekam/.gemini/antigravity/scratch/dejargon/index.html", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/logo.svg":
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.end_headers()
            with open("/Users/ekam/.gemini/antigravity/scratch/dejargon/logo.svg", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/dejargon":
            try:
                content_len = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_len)
                body = json.loads(post_body.decode('utf-8'))

                report_text = body.get('report_text', '')
                image_b64 = body.get('image_b64', None)
                target_lang = body.get('language', 'English')
                doc_cat = body.get('doc_category', 'Prescription')

                system_prompt = f"""
                You are DeJargon, a certified clinical interpretation and pharmaceutical OCR engine.
                The patient requested explanations in: {target_lang}.
                Category selected by user: {doc_cat}.

                SPECIAL INSTRUCTION FOR MEDICINE BOX / BOTTLE / BLISTER STRIP:
                - If the user uploaded a photo of a medicine container (box, bottle, syrup, blister foil strip, tube):
                  1. Identify the Exact Brand Name and Generic Salt/Composition (e.g., Crocin 650 -> Paracetamol 650mg).
                  2. Extract manufacturer, strength, and expiry date if visible.
                  3. Clearly state:
                     - What condition this medicine is commonly used to treat.
                     - Standard adult dosage/guidelines.
                     - Critical precautions (e.g., do not take on empty stomach, avoid alcohol, check allergy).
                     - Common side effects in simple language.

                SPECIAL INSTRUCTION FOR DOCTOR PRESCRIPTION SLIPS:
                - Read doctor handwriting and abbreviations (OD, BD, TDS, SOS, HS).
                - Extract every medicine name, dosage, schedule, and purpose.

                SPECIAL INSTRUCTION FOR LAB TESTS:
                - Extract numeric values, standard ranges, and clinical meaning.

                OUTPUT LANGUAGE: Write all explanations, summaries, and questions in natural {target_lang}.
                Do NOT insert repetitive punctuation like commas or asterisks. Write in smooth, spoken sentences.

                You must return a strictly valid JSON object matching this schema:
                {{
                  "plain_summary": "A 2 to 3 sentence clear overview in {target_lang}.",
                  "prescriptions": [
                    {{
                      "medicine_name": "Full Medicine / Brand Name (e.g. Augmentin 625)",
                      "dosage": "Strength & form (e.g. 625mg tablet)",
                      "frequency": "Exact schedule or standard usage in {target_lang}",
                      "purpose": "What this medicine treats in {target_lang}",
                      "instructions": "Key safety warnings, food rules & side effects in {target_lang}"
                    }}
                  ],
                  "biomarkers": [
                    {{
                      "name": "Biomarker name",
                      "value": "Value with units",
                      "normal_range": "Normal range",
                      "status": "Normal or High or Low",
                      "explanation": "What this indicates in {target_lang}"
                    }}
                  ],
                  "questions_for_doctor": [
                    "Question 1 in {target_lang}",
                    "Question 2 in {target_lang}",
                    "Question 3 in {target_lang}"
                  ]
                }}
                
                Respond ONLY with valid JSON. Do not enclose in markdown blocks.
                """

                parts = [{"text": system_prompt}]
                if report_text:
                    parts.append({"text": f"Patient Report Text:\n{report_text}"})
                if image_b64:
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_b64
                        }
                    })

                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={API_KEY}"
                payload = {
                    "contents": [{"parts": parts}],
                    "generationConfig": {
                        "temperature": 0.2,
                        "response_mime_type": "application/json"
                    }
                }

                req = urllib.request.Request(
                    api_url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )

                with urllib.request.urlopen(req, timeout=25) as resp:
                    resp_data = json.loads(resp.read().decode('utf-8'))
                    raw_text = resp_data['candidates'][0]['content']['parts'][0]['text']
                    print(f"\n[DEBUG GEMINI RESPONSE]:\n{raw_text}\n")
                    result_json = json.loads(raw_text)

                # Generate true server-side MP3 voice audio using gTTS (100% reliable across all devices)
                audio_b64 = None
                try:
                    from gtts import gTTS
                    import io
                    gtts_lang_map = {
                        "Hindi": "hi",
                        "English": "en",
                        "Spanish": "es",
                        "French": "fr",
                        "Arabic": "ar"
                    }
                    lang_code = gtts_lang_map.get(target_lang, "en")
                    tts = gTTS(text=result_json.get("plain_summary", ""), lang=lang_code, slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    audio_b64 = base64.b64encode(fp.read()).decode('utf-8')
                except Exception as tts_err:
                    print(f"[gTTS Audio Warning]: {tts_err}")

                result_json["audio_base64"] = audio_b64

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result_json).encode('utf-8'))

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

def run_server(port=8080):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, DeJargonHandler)
    print(f"DeJargon Server running at http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
