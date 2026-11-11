# Data & AI with Gemini | Sharjah Workshop

**Three-day, hands-on AI workshop · 2–4 November 2026**  
**Website (https://decoding-data-science.github.io/sharjah/)**

https://decoding-data-science.github.io/sharjah/prompt-engineering-guide.html#five

https://decoding-data-science.github.io/sharjah/rag_play_lab.html

**Individual assessments**

https://forms.gle/SLs9ksmtvqWjK6276

**Team Assessments**

https://forms.gle/rVEAjVAQd4uNjPE48

A practical introduction to **data analytics, generative AI, document understanding, and AI-assisted workflows** using **Google Colab and the Gemini API**. The exercises follow a fictional airport operations case study known as **“The Friday Problem.”**

> **Workshop safety:** All sample data and policies are fictional. Do not upload real passenger, employee, organizational, or otherwise confidential information to AI tools. Store API keys in Google Colab Secrets—not in code or this repository.

## Learning journey

| Day | Focus | Outcomes |
| --- | --- | --- |
| **Day 1 — Explore & Ask** | Data understanding, document understanding, models, system prompts, and context | Explore airport data and ask better grounded questions. |
| **Day 2 — Build the Analyst** | AI-assisted analysis and practical notebooks | Apply the tools to structured and unstructured workshop materials. |
| **Day 3 — Put It Together** | Integrated workflow and practice | Combine the skills into an end-to-end use case. |

## Get started

1. Read the [participant handbook](handouts/Participant_Handbook.pdf) and [workshop handout](handouts/Workshop_Handout.pdf).
2. Open the [workshop website](docs/index.html) for the daily agenda, setup, exercises, and downloads.
3. Prepare a Google account and open [Google Colab](https://colab.research.google.com/).
4. Obtain any required Gemini API access through [Google AI Studio](https://aistudio.google.com/) and keep credentials in **Colab Secrets**.
5. Work through the Day 1 notebooks in numerical order. Open each `.ipynb` in Colab and follow its setup cells.
6. Use the fictional [airport data](data/) and [document register](data/documents/Document_Register.md) for exercises.

## Restore the airport database

The synthetic SQLite database is included as eight compressed parts under [data/database/](data/database/). After cloning or downloading the repository, restore the original `airport_ops.db` by running:

```bash
python data/database/restore_database.py
```

The script checks the database integrity before writing it. The [Excel workbook with 11 worksheets](data/Airport_Copilot_Workbook.xlsx) is available directly, without any restoration step. See the [database README](data/database/README.md) for details.

## Repository structure

```text
sharjah/
├── README.md                         # Start here
├── .gitignore
├── docs/                             # GitHub Pages-ready workshop website
│   ├── index.html
│   ├── setup.html
│   ├── day-1.html
│   ├── day-2.html
│   ├── day-3.html
│   ├── exercises.html
│   ├── downloads.html
│   ├── assets/
│   └── downloads/                   # Participant downloads released for Day 1
├── notebooks/                        # Day 1 Colab notebooks and Python helpers
│   ├── D1_01_Data_Understanding.ipynb
│   ├── D1_02_Documents_Understanding.ipynb
│   ├── D1_03_Models_System_Prompt_Context.ipynb
│   ├── workshop_helpers.py
│   └── workshop_agent.py
├── data/
│   ├── database/
│   │   ├── airport_ops.db                # Rebuild with restore_database.py
│   │   └── Data_Dictionary.md
│   └── documents/                   # Fictional policy documents in TXT/PDF
├── slides/                           # Day 1 presentations
├── handouts/                         # Participant PDFs
├── release_later/                    # Day 2/3 material: publish on schedule
├── source/                           # Workshop content-generation scripts
└── index_single_file.html           # Portable, single-file version of the site
```

**Note:** The folder tree describes the full workshop distribution. If some assets are not yet available in GitHub, use the original workshop bundle until they are published.

## Workshop resources

| Resource | Location |
| --- | --- |
| Website and day-by-day guidance | [docs/](docs/) |
| Colab notebooks | [notebooks/](notebooks/) |
| Synthetic database and dictionary | [data/database/](data/database/) |
| Fictional policies and document register | [data/documents/](data/documents/) |
| Presentation slides | [slides/](slides/) |
| Participant handbook and handout | [handouts/](handouts/) |
| Day 2 and 3 release materials | [release_later/](release_later/) |
| Site and resource generator scripts | [source/](source/) |

## Publish the workshop website

The prepared website uses plain HTML, CSS, and JavaScript—**no site build is required**.

1. In **GitHub → Settings → Pages**, choose **Deploy from a branch**.
2. Choose branch **main** and folder **/docs**.
3. Save. Once the site is deployed, visit **https://decoding-data-science.github.io/sharjah/**.

**Release policy:** The Day 2 and Day 3 participant assets live in `release_later/`. Copy each day's intended materials into `docs/downloads/` only when that day's release is approved. Avoid publishing facilitator solutions or answer keys.

## Good practices

- Use only the **synthetic** airport database and fictional policy documents provided.
- Confirm the **effective/current** document version; some included policies are clearly marked **DRAFT** or **SUPERSEDED** for learning purposes.
- Never commit API keys, service-account credentials, or private data.
- Review model names, pricing, quota limits, and access requirements before running the examples.
- Keep the workshop's public participant materials separate from facilitator-only resources.

## About

Created by **[Decoding Data Science](https://decodingdatascience.com)** for hands-on AI education and practical enterprise use cases.

**Educational use:** The exercises and airport scenario are fictional demonstrations, not operational aviation guidance.
