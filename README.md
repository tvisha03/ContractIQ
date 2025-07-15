# ContractIQ: Contract Analysis Platform

ContractIQ is a full-stack application for advanced contract analysis, pain point detection, and custom NER (Named Entity Recognition) tailored for legal and HR contracts. It supports PDF and Word uploads, granular clause/risk extraction, and a modern, interactive frontend for reviewing results.

---

## Features

- **PDF/Word Upload:** Upload contracts for instant analysis.
- **Advanced Pain Point Detection:** Context-aware, section-based extraction of legal/HR risks (e.g., notice, non-compete, vacation forfeiture, arbitration, etc.) with risk scoring and explanations.
- **Custom NER:** Extracts granular entities (Employer, Employee, Salary, Notice Period, etc.) using custom rules.
- **Section-aware Analysis:** Pain points are linked to contract sections/clauses for context.
- **Color-coded UI:** High/medium risk areas are highlighted in red/yellow for easy review.
- **Summarization:** Generates a summary of the contract.
- **Modern Frontend:** Built with React, Vite, and Tailwind CSS.

---

## Tech Stack

- **Backend:** Python, FastAPI, spaCy, custom regex/entity rules
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **PDF Extraction:** Custom extractor
- **NER:** spaCy with custom EntityRuler patterns

---

## Installation & Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn
- (Optional) virtualenv or conda for Python

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ContractIQ
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### Environment Variables
- If you use any `.env` files, create them manually (see `.gitignore` for excluded files).

#### Run the Backend
```bash
uvicorn main:app --reload
```
- The backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
cd ../frontend
npm install  # or yarn
```

#### Environment Variables
- Create a `.env` file in `frontend/` with:
  ```
  VITE_API_URL=http://localhost:8000
  ```

#### Run the Frontend
```bash
npm run dev  # or yarn dev
```
- The frontend will be available at `http://localhost:5173`

---

## Usage
1. Start both backend and frontend servers.
2. Open the frontend in your browser.
3. Upload a contract (PDF/Word).
4. View extracted pain points (color-coded), NER entities, and summary.
5. Click on highlights or sidebar items for more details.

---

## Project Structure

```
ContractIQ/
├── backend/
│   ├── main.py
│   ├── services/
│   │   ├── painpoints.py
│   │   ├── ner.py
│   │   ├── ...
│   ├── models/
│   └── uploads/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── index.html
│   └── ...
├── requirements.txt
└── README.md
```

---

## Customization
- **Pain Point Rules:** Edit `backend/services/pain_points_rules.json` to add or modify risk patterns.
- **NER Patterns:** Edit `backend/services/ner.py` to add new entity extraction rules.
- **Styling:** Tweak Tailwind classes in frontend for custom UI.

---

## Security & Notes
- `.env` and other sensitive files are excluded from git (see `.gitignore`).
- Never commit real contracts or sensitive data.
- For production, set up HTTPS and proper CORS.

---

## License
MIT (or your chosen license)

---

## Contact
For questions, open an issue or contact the maintainer.
