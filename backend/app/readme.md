# *Sentinel*

**Sentinel — Payment Risk Intelligence.** A browser-based fintech dashboard for monitoring transactions, scoring payment risk, and surfacing fraud insights, backed by a Python application layer.

![HTML5](https://img.shields.io/badge/for-the-badge?style=for-the-badge&logo=html5&logoColor=white&label=HTML5&color=E34F26)
![CSS3](https://img.shields.io/badge/for-the-badge?style=for-the-badge&logo=css3&logoColor=white&label=CSS3&color=1572B6)
![JavaScript](https://img.shields.io/badge/for-the-badge?style=for-the-badge&logo=javascript&logoColor=black&label=JavaScript&color=F7DF1E)
![Python](https://img.shields.io/badge/for-the-badge?style=for-the-badge&logo=python&logoColor=white&label=Python&color=3776AB)

---

## Features

- Real-time payment risk dashboard with at-a-glance stats
- Dedicated transaction monitoring view
- Risk analysis screen for scoring and flagging suspicious activity
- Insights view for trends and aggregated fraud signals
- Payment review workflow
- Decisioning screen for approve / hold / decline actions
- Responsive, sidebar-driven single-app layout
- Backend application layer (`backend/app/`) powering the risk logic behind the UI

---

## Project Structure

```
Sentinal/
│
├── index.html            # Main dashboard (Sentinel overview)
├── transactions.html      # Transaction monitoring view
├── risk-analysis.html     # Risk scoring / analysis view
├── insights.html           # Aggregated insights and trends
├── payment.html            # Payment review view
├── decision.html            # Decisioning (approve / hold / decline) view
│
└── backend/
    └── app/                # Backend application code powering risk logic
```

---

## File Description

| File / Folder         | Description                                              |
| ---------------------- | --------------------------------------------------------- |
| `index.html`            | Main dashboard — overview, stats, and navigation          |
| `transactions.html`     | View and monitor incoming transactions                    |
| `risk-analysis.html`    | Risk scoring and analysis interface                       |
| `insights.html`         | Aggregated insights and fraud trend visualizations         |
| `payment.html`          | Payment review interface                                  |
| `decision.html`         | Final decisioning screen (approve / hold / decline)        |
| `backend/app/`          | Backend application layer serving/supporting the risk data |

---

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python (backend, under `backend/app/`)

---

## Getting Started

1. Clone the repository.

```
git clone https://github.com/rithwiklabs/Sentinal.git
```

2. Navigate to the project directory.

```
cd Sentinal
```

3. Open `index.html` in your preferred web browser to explore the frontend.

4. To run the backend, set up your Python environment inside `backend/app/` and install any required dependencies before starting the service.

---

## Future Enhancements

- Live backend API integration for all dashboard views
- Authentication and role-based access
- Configurable risk-scoring rules
- Exportable reports (CSV / PDF)
- Dark mode
- Automated test coverage for the backend

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository.
2. **Create a branch** for your change:
   ```
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**, keeping commits focused and descriptive.
4. **Test locally** — open the affected `.html` page(s) in a browser and/or run the backend from `backend/app/` to confirm nothing breaks.
5. **Commit and push**:
   ```
   git commit -m "Add: short description of your change"
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** against `main`, describing what you changed and why.

### Guidelines

- Keep the existing MVC-style separation between UI (`.html` pages) and backend logic (`backend/app/`).
- Match the existing code style and naming conventions.
- Prefer small, focused PRs over large ones — easier to review and merge.
- For bigger changes (new features, architecture changes), open an issue first to discuss the approach.
- Report bugs or suggest features via [GitHub Issues](https://github.com/rithwiklabs/Sentinal/issues).

---

## License

This project is created for **educational and learning purposes**.