<div align="center">
  <img src="assets\banner.jpg" alt="Monty Hall Problem" width="100%" height="300px"/>
</div>

# 📇 Contact Book

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-100%25_passing-brightgreen?logo=pytest)
![Status](https://img.shields.io/badge/Project-Completed-success)
</div>

A professional **Contact Book** application built with **Python**, **SQLite**, **SQLAlchemy**, and **Streamlit**.
This project is designed as a **portfolio-ready application**, focusing on clean architecture, data validation, testability, and good engineering practices.

Includes:
- CRUD operations for contacts
- Contact categorization
- Email normalization and validation
- Persistent storage with SQLite
- Modular architecture with services and repositories
- Ready for linting, testing, and CI integration


## 📌 Table of Contents

- [🌐 Live Demo](#-live-demo)
- [🚀 Features](#-features)
- [🖼️ Screenshot](#️-screenshot)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏗️ Project Architecture](#️-project-architecture)
- [🚀 Getting Started](#-getting-started)
- [🧪 Testing](#-testing)
- [🔍 Code Quality & Security Checks](#-code-quality--security-checks)
- [🎯 Design Decisions](#-design-decisions)
- [🚀 Demo & Deployment Details](#-demo--deployment-details)
- [🧠 Key Engineering Insights](#-key-engineering-insights)
- [📌 Future Improvements](#-future-improvements)
- [👤 Author](#-author)
- [🤝 Contributing](#-contributing)
- [📞 Contact](#-contact)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)


## 🌐 Live Demo
You can try the app directly here: 
 <a href="https://contact-book-njangholi.streamlit.app/" target="_blank">👉 Live on Streamlit Cloud</a>

> ⚠️ **Demo Note**  
> This application is deployed on **Streamlit Cloud**, which uses **ephemeral storage**.  
> Sample contacts are automatically loaded for demonstration purposes.  
> Any data you add may be reset when the app restarts.

## ✨ Features

* Create, view, update, and delete contacts (CRUD)
* Categorize contacts (e.g. Family, Friends, Work)
* Real-time search and filtering
* Email normalization and validation
* Persistent storage using SQLite
* Clean and simple Streamlit UI
* Modular and scalable architecture
* Ready for linting, testing, and CI tools


## 🖼️ Screenshot


<div align="center">
  <div style="text-align: center; max-width: 300px;">
    <img src="assets\home.jpg" alt="Home view" style="width: 100%; border-radius: 8px;" />
    <p style="margin-top: 8px; font-size: 0.9em; color: #555;">Home view of Contact Book</p>
  </div>
  <div style="text-align: center; max-width: 300px;">
    <img src="assets\add.jpg" alt="Add contact" style="width: 100%; border-radius: 8px;" />
    <p style="margin-top: 8px; font-size: 0.9em; color: #555;">Add Contact view</p>
  </div>
  <div style="text-align: center; max-width: 300px;">
    <img src="assets\view.jpg" alt="View contact" style="width: 100%; border-radius: 8px;" />
    <p style="margin-top: 8px; font-size: 0.9em; color: #555;">Contact View</p>
  </div>
</div>



## 🛠️ Tech Stack
| Layer | Technology | 
|-------|-------------|
| Frontend / UI | [Streamlit](https://streamlit.io) |
| Backend Logic | Python 3.11+ |
| Database | [SQLite](https://www.sqlite.org/index.html) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Data Validation | Custom validation service |
| Testing | Pytest |
| Code quality & security checks | Pylint/Ruff/Bandit |
| CI / Automation | GitHub Actions |
| Styling | Custom CSS (Glassmorphism) |


---
## 🏗️ Project Architecture

The project follows a **layered architecture** to keep concerns separated and the codebase maintainable:

```
contact-book/
│
├── src/
│   ├── database/      # Database engine and session handling
│   ├── models/        # SQLAlchemy ORM models
│   ├── crud/          # Data access layer (repositories)
│   ├── services/      # Business logic (validation, normalization, etc.)
│   ├── CLI/           # Command-line interface 
│   ├── utils/         # Utility functions (e.g. validation helpers)
│   ├── ui/            # Streamlit pages and routing
│   └── run.py         # Application entry point
│
├── tests/             # Unit tests and integration tests
│   ├── unit/          # Unit tests for services and utils
│   └── integration/   # Integration tests for end-to-end scenarios
├── docs/              # Project documentation
├── .github/           # GitHub Actions CI workflows
├── .bandit.yml        # Security scan configuration
├── check.ps1          # Local quality checks (lint, type check, security)
├── requirements.txt   # Python dependencies
├── pyproject.toml     # Project metadata and tool configurations
└── README.md          # Project documentation
```

---


## 🚀 Getting Started
## ⚙️ Installation
### 1. Clone the repository

```bash
git clone https://github.com/njangholi/contact-book.git
cd contact-book
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
## ▶️ Run the Application
### Web Interface
To run the Streamlit app:
```bash
streamlit run src/run.py
```  

Then open your web browser and navigate to `http://localhost:8501` to access the app.  

---
### Terminal Version
To run contact book in the terminal:
```bash
python src/CLI/main.py
```
Then follow the on-screen prompts to manage your contacts.

Example terminal output:
```
 Contact Book CLI

1️⃣  List all contacts
2️⃣  Add new contact
3️⃣  Search contacts
4️⃣  Edit contact
5️⃣  Delete contact
6️⃣  Exit

Choose an option [1/2/3/4/5/6]: 
```
**Note:** The terminal version is a simplified interface for quick access without the web UI. For first time run, the database needs to be initialized according to the instructions on the CLI screen.


## 🧪 Testing

Run all tests using:

```bash
pytest
```
For detailed output, use:
```bash
python -m pytest --html=report.html
```
Note: `pytest-html` needs to be installed.

# ⚙️ Development

## 🔍 Code Quality & Security Checks

This project includes a local code quality runner script to ensure
consistent formatting, linting, type checking, and security analysis
before committing code.

All checks are aligned with the project's CI pipeline and can be run
locally using PowerShell.

### Available Checks

The script runs the following tools in order:

1. **Formatting**
   - `isort`
   - `black`

2. **Linting**
   - `ruff`
   - `pylint`

3. **Type Checking**
   - `mypy`

4. **Security Analysis**
   - `bandit`

---

### Usage

Run all checks on the entire project:

```powershell
.\check.ps1
```

Run checks only on the source code:
```powershell
.\check.ps1 -Target src/
```
Run linting only on the tests directory:
```powershell
.\check.ps1 tests/ -SkipFormat -SkipType -SkipSecurity
```
Run all checks without stopping on the first failure:
```powershell
.\check.ps1 -Target . -ContinueOnError
```
Run only formatting and security checks:
```powershell
.\check.ps1 -SkipLint -SkipType
```

**Notes**

- The script is intended for local development and pre-commit validation.

- CI pipelines should always be considered the final source of truth.

- PowerShell is required to run this script.

- These packages need to be installed: `pip install -q isort black ruff pylint mypy bandit`


## 🎯 Design Decisions

* **Layered architecture** was chosen to keep UI, business logic, and data access independent.
* **Services layer** handles validation and normalization to avoid logic duplication.
* **Repositories** abstract database operations for easier testing and future database changes.
* **Streamlit** was selected for rapid UI development and simplicity.  
📚 *Full Documentation** → [Architecture Design](docs/ARCHITECTURE.md)

## 🚀 Demo & Deployment Details

This application is deployed on **Streamlit Cloud**, which runs apps in an **ephemeral container** environment.

### Automatic Database Bootstrap

When the application starts, it automatically ensures that the database and required tables exist:

* If the SQLite database file does not exist, it is created automatically
* If required tables (e.g. `contacts`) are missing, they are created using SQLAlchemy metadata
* No manual initialization or CLI command is required for the live demo

This behavior guarantees that the application always starts in a usable state on Streamlit Cloud.

### Demo Seed Data

After the database schema is ensured, the application attempts to load **demo seed data**:

* Seed data is inserted **only if the database is empty**
* The operation is idempotent (safe to run multiple times)
* Existing user data is never deleted or overwritten

This allows reviewers to immediately explore the app without manual data entry, while keeping the demo safe and predictable.

### Important Notes

* Streamlit Cloud uses **non-persistent storage**
* Data may be reset when the app restarts, sleeps, or is redeployed
* Demo seed data will be reloaded automatically if the database is recreated

This design choice is intentional and reflects a common production-ready pattern for cloud-hosted demo applications.


## 🧠 Key Engineering Insights

* **Handled ephemeral cloud environments with automatic bootstrapping**  
  <u>Situation:</u> Streamlit Cloud does not persist local files between restarts.  
  <u>Task:</u> Ensure the application always starts in a usable state without manual setup.  
  <u>Action:</u> Implemented automatic database and schema initialization to support deployment on Streamlit Cloud, which uses non-persistent local storage.  
  <u>Result:</u> The live demo reliably starts without errors or user intervention.  
  👉 [Database bootstrap logic](src/database/init.py)


* **Designed idempotent initialization and seeding logic**  
  <u>Situation:</u> Streamlit apps may rerun multiple times during a single session.  
  <u>Task:</u> Prevent duplicated demo data or destructive side effects.  
  <u>Action:</u> Made both database initialization and seed loading idempotent.  
  <u>Result:</u> Safe reruns and predictable behavior across restarts.  
  👉 [Demo seed implementation](src/database/seed.py)

* **Preserved architectural boundaries during data seeding**  
  <u>Situation:</u> Seed data often bypasses business rules when written directly to the database.  
  <u>Task:</u> Keep validation and normalization consistent across the app.  
  <u>Action:</u> Routed seed logic through the service layer instead of direct ORM access.  
  <u>Result:</u> A cleaner architecture and production-like behavior even in demo mode.  
  👉 [Service layer example](src/services)

* **Treated demo UX as part of system design**  
  <u>Situation:</u> Empty or reset demos confuse reviewers and reduce perceived quality.  
  <u>Task:</u> Make the demo intuitive and immediately explorable.  
  <u>Action:</u> Added automatic demo data loading and clear documentation in the [README](#-demo--deployment-details).  
  <u>Result:</u> Improved reviewer experience and clearer communication of system constraints.

## 📌 Future Improvements
| Priority | Feature                                | Description                                                                                     | Status          |
|---------|----------------------------------------|-------------------------------------------------------------------------------------------------|-----------------|
| High    | Authentication & User Accounts        | Add user login and registration to manage personal contact books.                               | ⚙️ Design phase         |
| Medium  | Export Contacts (CSV / JSON)          | Allow users to export their contacts in common formats for backup or sharing.               | ⏳ Planned         |
| Low     | Advanced Analytics Dashboard          | Provide insights on contact categories, frequency of interactions, etc.                            | ⏳ Planned         |
| Low     | API Layer (FastAPI Integration)       | Expose CRUD operations via a RESTful API for external integrations.                             | ⏳ Planned         |
| Low     | Cloud Database Support                | Enable switching to cloud databases like PostgreSQL or MySQL for scalability.                      | ⏳ Planned         |

---

## 👤 Author

**Narges Jangholi**  

AI & Computational Neuroscience Engineer | Machine Learning & Applied Math Enthusiast
[GitHub](https://github.com/Njangholi) |
[LinkedIn](https://www.linkedin.com/in/narges-jangholi/)

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## 📞 Contact
For any inquiries or feedback, please reach out to [jangholi83@gmail.com](mailto:jangholi83@gmail.com).


## 📄 License

This project is for educational and portfolio purposes.

## 🙏 Acknowledgements
Thanks to the open-source community for the tools and libraries that made this project possible!

**Made with ❤️ using Python + Streamlit**
