# Portfolio Case Study: Dida Boža — AI-Assisted Content & Analytics Pipeline

> **TL;DR** — A Python-based workflow for preparing Instagram content for Dida Boža, a Croatian food brand. The project combines prompt preparation for AI-assisted copywriting, local carousel image generation, CSV-based social media analytics, period comparisons, weekly reports, and a dashboard. It includes automated tests and can run its core workflow without paid API calls.

---

## 1. The Problem

Small brands need a consistent social media presence, but preparing content involves several separate tasks:

1. **Content planning:** developing ideas and writing captions that match the brand's tone.
2. **Visual production:** preparing branded images and carousel posts.
3. **Performance tracking:** organizing engagement metrics and identifying patterns.
4. **Iteration:** using performance data to inform future content decisions.

For a small food brand such as **Dida Boža**, these tasks can take time and require several different tools.

**My goal** was to build a reproducible Python workflow that brings content preparation and basic performance analysis together in one project.

The workflow is designed to:
- Prepare structured prompts for AI-assisted content creation.
- Generate carousel slides locally.
- Analyze social media metrics from CSV files.
- Compare reporting periods and generate summaries.
- Keep the workflow usable without paid API calls.

---

## 2. Architecture

```text
                 USER
                  |
          +-------+--------+
          |                |
      CLI workflow    Streamlit interface
      (run_all.py)      (app.py)
          |
          v
   CONTENT PREPARATION
   generate_content.py
   - Brand voice examples
   - Prompt preparation
   - Manual ChatGPT workflow
          |
          v
   VISUAL CONTENT
   make_carousel.py
   - Pillow-based image generation
   - Four carousel slides
   - Canva editing instructions
          |
          v
   ANALYTICS
   analyze_metrics.py
   compare_metrics.py
   weekly_report.py
   create_dashboard.py
          |
          v
   OUTPUT
   - Analysis reports
   - Period comparisons
   - Weekly summary
   - Dashboard visualization
```

**Key design decision: local-first execution.**

The core command-line workflow can prepare prompts, create carousel slides, and process example metrics without requiring a paid OpenAI API call.

AI-assisted copywriting is performed through a manual ChatGPT step: the user opens the generated prompt, submits it to ChatGPT, and can save the resulting content locally.

---

## 3. What Was Built

### Core components

| File | Purpose | Technology |
|---|---|---|
| `generate_content.py` | Prepares content prompts and supports saving generated content | Python |
| `make_carousel.py` | Generates four carousel slides | Pillow |
| `run_all.py` | Coordinates the multi-step local workflow | Python |
| `analyze_metrics.py` | Analyzes social media metrics | Python, CSV |
| `compare_metrics.py` | Compares two reporting periods | Python |
| `weekly_report.py` | Generates a weekly performance report | Python |
| `create_dashboard.py` | Creates a metrics dashboard | Matplotlib |
| `app.py` | Streamlit application entry point | Streamlit |
| `tests/` | Automated tests for content and analytics functionality | pytest |

### Supporting files

- `brand_voice_examples.txt` — brand voice reference material.
- `metrics_template.csv` — template for recording social media performance.
- `metrics_demo.csv` — example metrics.
- `metrics_demo_old.csv` and `metrics_demo_new.csv` — sample datasets for period comparisons.
- `output/` — generated reports, prompts, and visualizations (local output directory).

---

## 4. Automated vs. Manual

An important part of this project is distinguishing implemented automation from manual work.

| Step | Status | Explanation |
|---|---|---|
| Prompt preparation | Automated | Python prepares a structured prompt |
| AI copywriting | Manual AI-assisted step | The prompt is submitted to ChatGPT by the user |
| Saving generated content | Supported | Generated content can be saved locally |
| Carousel generation | Automated | Pillow creates four slides |
| Canva refinement | Manual | Final visual adjustments can be made in Canva |
| Metrics processing | Automated | CSV data is processed locally |
| Period comparison | Automated | The project calculates changes between datasets |
| Weekly reporting | Automated | A report is generated from the available data |
| Dashboard creation | Automated | Metrics are visualized locally |
| Final content approval | Manual | Human review is required before publication |

**Honest assessment:** this is a hybrid automation workflow. It automates repeatable preparation and analysis tasks while retaining human control over AI-generated copy, visual branding, and final publication.

The project does not claim that the entire social media publishing process is autonomous.

---

## 5. Results

### Technical results

- **21 automated tests passed** in the latest local test run.
- Python source files passed compilation checks.
- `pip check` reported no broken package requirements.
- The complete local pipeline ran successfully.
- The metrics dashboard was generated as a PNG image.
- The staged Git changes passed the API-key pattern check.
- The project was committed and pushed to GitHub.

### Example analytics

The included old and new demo datasets contain simulated data, not actual Instagram Insights.

The example comparison showed:

| Metric | Previous period | New period | Change |
|---|---:|---:|---:|
| Average likes | 121.67 | 153.33 | +26.03% |
| Average comments | 17.33 | 25.00 | +44.23% |
| Average saves | 34.33 | 46.67 | +35.92% |
| Average reach | 3,366.67 | 3,933.33 | +16.83% |
| Engagement rate | 5.19% | 5.79% | +0.60 pp |

These figures demonstrate the analytics workflow using sample data. They should not be interpreted as measured growth for Dida Boža.

---

## 6. Technologies Used

- **Python 3.11** — primary programming language.
- **Pandas** — data handling dependency.
- **Pillow** — local image and carousel generation.
- **Matplotlib** — dashboard visualization.
- **Streamlit** — application interface.
- **pytest** — automated testing.
- **CSV** — metrics input and example datasets.
- **Git and GitHub** — version control and project hosting.

The verified local workflow does not require paid OpenAI API calls. ChatGPT is used manually for the AI-assisted content step.

---

## 7. What I Learned

1. **Automation should solve a complete workflow.** Individual scripts become more useful when they work together through a single pipeline.

2. **Human-in-the-loop design matters.** AI can help prepare content, but brand-sensitive material still benefits from human review.

3. **Analytics need transparent data sources.** Simulated datasets are useful for testing calculations and reports, but they must never be presented as real business performance.

4. **Testing improves reliability.** Automated tests help verify content-generation and analytics functionality before changes are published.

5. **Local-first design reduces barriers.** A useful demonstration should be reproducible without requiring paid API access.

---

## 8. Repository

**GitHub:**  
https://github.com/1244Matt1244/dida-boza-ai-recept

**Author:** Matej Martinović

**Project type:** Educational and professional portfolio project.

---

## 9. How to Reproduce

Clone the repository:

```bash
git clone https://github.com/1244Matt1244/dida-boza-ai-recept.git
cd dida-boza-ai-recept
```

Create and activate a virtual environment (Windows Git Bash):

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the complete local workflow:

```bash
python run_all.py
```

Prepare a prompt without API calls:

```bash
python generate_content.py --dry-run
```

Run the tests:

```bash
python -m pytest tests/ -v
```

Compile Python files:

```bash
python -m compileall -q .
```

Check installed dependencies:

```bash
python -m pip check
```

Generated files are saved in the project's local output directory.

---

## 10. What's Next

- Verify and complete the Streamlit application's dependencies and functionality.
- Add continuous integration with GitHub Actions.
- Connect real Instagram Insights data where account permissions allow.
- Add A/B testing for content and prompt variations.
- Expand the workflow with additional content formats.
- Support English and German content generation.

---

*Case study last updated: November 2026.*