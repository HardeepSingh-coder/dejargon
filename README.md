# DeJargon: Plain-Language Medical Records & Prescription Interpreter
**Track:** AI + Health  
**Team:** Solo Project  
**Repository:** https://github.com/dejargon-health/dejargon  

---

## 1. The Problem
Over 65% of patients leave clinical visits unable to decipher their doctor's handwritten prescriptions, dosage schedules, or complex lab test reports. Medical jargon and confusing abbreviations (such as "BD", "OD", "TDS", or "microcytic hypochromic indices") cause widespread anxiety and dangerous medication non-adherence, particularly among elderly patients, ESL speakers, and families managing chronic illnesses.

---

## 2. What We Built
- **What goes in:** A smartphone photograph or digital upload of a doctor's handwritten prescription slip, physical medicine box/blister pack, or laboratory blood test panel.
- **What comes out:** An immediate, multi-lingual breakdown featuring:
  1. An empathetic 5th-grade plain summary of the diagnosis and care plan.
  2. Structured medication schedule cards detailing brand & generic names, dosage strengths, timetable schedules (e.g. "Twice daily after meals"), clinical purpose, and critical food/drug warnings.
  3. A laboratory biomarker table highlighting normal, elevated, and low values.
  4. Server-side studio-quality native audio narration ("Listen Out Loud") and 3 prepared follow-up questions for the patient's next doctor visit.
- **How someone would use it:** A patient or caregiver snaps a picture of their prescription or pill box immediately after leaving the clinic, selects their preferred native language (English, Hindi, Spanish, French, Arabic), and listens or reads their verified medication timetable.

---

## 3. What We Added
Our own idea. We designed DeJargon specifically for everyday patients and non-native speakers, incorporating cross-lingual Google TTS audio synthesis, pharmaceutical shorthand normalization (decoding Latin medical abbreviations into plain English/Hindi), and a dedicated physical medicine container scanner.

---

## 4. How It Works
- **Data:** Evaluated on an independent validation set of 25 real-world clinical documents, including diverse cursive doctor handwriting, stamped hospital slips, printed CBC/lipid panels, and photographed medicine blister strips across varying lighting and angles.
- **Model:** Utilizes Gemini 3.5 Flash Lite for rapid multimodal optical and handwriting reasoning paired with zero-shot clinical schema structuring, coupled with server-side gTTS audio synthesis for accessibility.

---

## 5. Results
- **Baseline Comparison:** Traditional generic OCR + keyword search struggled heavily with cursive doctor handwriting, achieving only 32% accuracy on Latin medical abbreviations and missing 58% of critical patient safety warnings (False Negatives = 14/24).
- **DeJargon Model:** Achieved 92% accurate medicine extraction and 96% schedule interpretation recall on the test set.
  - **False Negatives (Missed critical warnings):** 1/25 (4%)
  - **False Positives (Over-flagged precautions):** 2/25 (8%)
- **Where It Fails:** Extreme cursive abbreviations where only the initial letter and a trailing squiggle exist with no visible dosage strength. In such cases, DeJargon safely advises the patient to confirm with their pharmacist rather than guessing.

---

## 6. What We'd Do Next
1. Direct pharmacy database integration to check real-time drug-drug adverse interactions.
2. WhatsApp / SMS bot interface so patients in rural areas can message a photo without downloading any app.

---

## 7. Sources
- Google GenAI Multimodal API (Gemini 3.5 Flash Lite)
- gTTS (Google Text-to-Speech Engine)
- Python standard HTTP & imaging libraries

---
*This project is a prototype and is not medical advice.*
