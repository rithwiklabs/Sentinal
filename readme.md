# 🛡️ Sentinel — Payment Risk Intelligence

<p align="center">

</p>

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  
</p>

Sentinel is a payment risk intelligence platform that helps teams monitor transactions, analyse risk, and make faster, better-informed decisions about payments. It combines a clean fintech-style web dashboard with a backend service that powers the risk logic.

> 👥 **This is a group project.** Sentinel is built and maintained collaboratively by a team. Please read the [Contribution Guidelines](#-contribution-guidelines) before you start working on the repo.

---

## 📑 Table of Contents

- [About the Project](#-about-the-project)
- [Group Project & Team](#-group-project--team)
- [Project Structure](#-project-structure)
- [Views / Pages](#-views--pages)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Run the Views (Frontend)](#2-run-the-views-frontend)
  - [Run the Backend](#3-run-the-backend)
- [Contribution Guidelines](#-contribution-guidelines)
- [License](#-license)

---

## 📖 About the Project

Sentinel gives a single place to:

- Track and review payment **transactions**
- Run **risk analysis** on payments
- View **insights** and trends across activity
- Support **decision-making** (approve / review / block) on risky payments

---

## 👥 Group Project & Team

This project is developed as a **group project**. Every member is expected to contribute through branches and pull requests, and to review each other's work.

| Name            | GitHub                                            |
| --------------- | ------------------------------------------------- |
| M Rithwik Kumar | [@rithwiklabs](https://github.com/rithwiklabs)    |
| R Goutham Naik  | [@crack429078](https://github.com/crack420978)    |
| B Kushal        | [kushalbanda25](https://github.com/kushalbanda25) |
| M Neeraj        | [neeraj647](https://github.com/Neeraj647)         |

> Update this table with everyone on the team.

---

## 📁 Project Structure

```
Sentinal/
├── backend/
│   └── app/                # Backend application code
├── index.html              # Landing page / main dashboard
├── transactions.html       # Transactions view
├── risk-analysis.html      # Risk analysis view
├── insights.html           # Insights view
├── decision.html           # Decision view
├── payment.html            # Payment view
└── README.md
```

---

## 🖥️ Views / Pages

| Page             | File                 | Purpose                                 |
| ---------------- | -------------------- | --------------------------------------- |
| Home / Dashboard | `index.html`         | Entry point and overview of Sentinel    |
| Transactions     | `transactions.html`  | Browse and review payment transactions  |
| Risk Analysis    | `risk-analysis.html` | Analyse the risk level of payments      |
| Insights         | `insights.html`      | Trends and analytics                    |
| Decision         | `decision.html`      | Approve, review or block risky payments |
| Payment          | `payment.html`       | Payment flow / details                  |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- [Git](https://git-scm.com/downloads)
- A modern web browser (Chrome, Edge, Firefox, Safari)
- [Python 3.9+](https://www.python.org/downloads/) — for the backend and for serving the views locally
- _(Optional)_ [VS Code](https://code.visualstudio.com/) with the **Live Server** extension

### 1. Clone the Repository

```bash
git clone https://github.com/rithwiklabs/Sentinal.git
cd Sentinal
```

### 2. Run the Views (Frontend)

The views are plain HTML pages, so there is nothing to build or install. Pick **any one** of the options below.

**Option A — Open directly in the browser (quickest)**

Double-click `index.html`, or run:

```bash
# macOS
open index.html

# Linux
xdg-open index.html

# Windows
start index.html
```

**Option B — Use a local server (recommended)**

Serving the files over HTTP avoids browser restrictions and makes navigation between pages behave like a real site.

```bash
# from the project root
python -m http.server 5500
```

Then open **http://localhost:5500** in your browser.

**Option C — VS Code Live Server**

1. Open the project folder in VS Code.
2. Install the **Live Server** extension.
3. Right-click `index.html` → **Open with Live Server**.

You can now use the sidebar to move between the Dashboard, Transactions, Risk Analysis, Insights, Decision and Payment views.

### 3. Run the Backend

The backend lives in `backend/app`.

```bash
cd backend

# create and activate a virtual environment
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# start the server (FastAPI example)
uvicorn app.main:app --reload
```

The API will be available at **http://127.0.0.1:8000** (interactive docs at `/docs` if you are using FastAPI).

> ⚠️ Adjust the commands above if the backend uses a different framework or entry point.

---

## 🤝 Contribution Guidelines

Since this is a group project, we follow a simple workflow to keep the codebase clean and avoid conflicts. Everyone on the team — and any outside contributor — should follow these steps.

### 1. Get set up

```bash
# fork the repo (outside contributors) or clone it (team members)
git clone https://github.com/rithwiklabs/Sentinal.git
cd Sentinal

# always start from the latest main
git checkout main
git pull origin main
```

### 2. Create a branch

**Never commit directly to `main`.** Create a branch for every feature or fix:

```bash
git checkout -b <type>/<short-description>
```

Branch naming examples:

| Type       | Example                       |
| ---------- | ----------------------------- |
| Feature    | `feature/transactions-filter` |
| Bug fix    | `fix/sidebar-navigation`      |
| Docs       | `docs/update-readme`          |
| Refactor   | `refactor/risk-score-logic`   |
| Style / UI | `style/dashboard-cards`       |

### 3. Make your changes

- Keep changes **focused** — one feature or fix per branch.
- Follow the existing code style and naming conventions.
- Keep the UI consistent with the current theme (colours, spacing, fonts defined in the CSS variables).
- Test your changes locally in the browser (and against the backend, if applicable) before committing.
- Never commit secrets, API keys, `.env` files or personal data.

### 4. Commit your work

Write clear, meaningful commit messages using the [Conventional Commits](https://www.conventionalcommits.org/) style:

```
feat: add filter to transactions table
fix: correct active state in sidebar
docs: add setup instructions to README
style: adjust spacing on dashboard cards
refactor: simplify risk score calculation
```

```bash
git add .
git commit -m "feat: add filter to transactions table"
```

### 5. Push and open a Pull Request

```bash
git push origin <your-branch-name>
```

Then open a **Pull Request** into `main` on GitHub and include:

- A clear title and short description of **what** changed and **why**
- Screenshots or a short recording for any UI changes
- A link to the related issue (e.g. `Closes #12`)

### 6. Code review

- At least **one teammate** must review and approve a PR before it is merged.
- Respond to review comments and push follow-up commits to the same branch.
- The author should not merge their own PR without a review.
- Resolve merge conflicts on your branch before requesting a final review.

### 7. Keep your branch up to date

```bash
git checkout main
git pull origin main
git checkout <your-branch-name>
git merge main
```

### Team etiquette

- 💬 Communicate — tell the team what you're working on so work isn't duplicated.
- 🐛 Use **GitHub Issues** to report bugs, propose features, and assign tasks.
- 🧩 Break big tasks into small PRs that are easy to review.
- 🙌 Be respectful and constructive in reviews and discussions.

### Reporting bugs / requesting features

Open an [issue](https://github.com/rithwiklabs/Sentinal/issues) and include:

- A clear title and description
- Steps to reproduce (for bugs)
- Expected vs. actual behaviour
- Screenshots, if relevant

---

## 📄 License

No license has been added yet. The team should agree on one (for example MIT) and add a `LICENSE` file to the repository.

---

<p align="center">Built with ❤️ by the Sentinel team</p>
