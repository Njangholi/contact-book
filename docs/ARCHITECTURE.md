# Contact Book – Project Architecture

## Overview
This project follows a **Clean Architecture-inspired layered design** to ensure:
- High maintainability
- Separation of concerns
- Easy scalability
- Testability

The goal is to keep business logic independent from UI frameworks and database technologies. Although the application is relatively small, the architecture is intentionally designed to resemble real-world production systems.

---

## Folder Structure Explanation

src/

├── app.py               # Streamlit entry point (UI composition)  
├── main.py              # CLI entry point  
├── UI/                  # Presentation layer (Streamlit pages)  
│   ├── add_contact.py  
│   ├── edit_contact.py  
│   ├── show_contact.py  
│   ├── home.py  
│   └── router.py  
├── services/            # Business logic (Service layer)  
│    └── contact_service.py  
├── crud/                # Data access layer  
│   └── contacts.py  
├── database/            # Persistence layer  
│   ├── db.py  
│   └── models.py  
├── utils/               # Cross-cutting utilities  
│   └── validation.py  
└── tests/               # Unit tests  

## 🎯 Layer Responsibilities

### 1️⃣ UI Layer (Streamlit)
**Responsibility:** Presentation and user interaction

- Handles user interaction
- Displays forms, messages, and data
- Does NOT contain business rules
- Calls service functions only

> This makes it easy to swap Streamlit with another UI framework in the future.

`src/UI/`
Each file represents a UI responsibility: //TODO update at the end
- `new_contact.py`: Add contact UI
- `show_contact.py`: Display contacts
- `update.py`: Update contact UI

`src/app.py`
Main Streamlit entry point.  
Responsible for:
- Layout
- Navigation
- Calling UI modules

`src/main.py`
CLI or alternative execution entry point. //TODO update at the end

### 2️⃣ Service Layer
**Responsibility:** Business logic and application rules

- Central place for application rules
- Coordinates validation, duplication checks, and workflows
- Raises meaningful domain-level exceptions
- Orchestrates between CRUD and utils
- Completely independent of Streamlit

`src/services/`

- Validate input
- Normalize data
- Enforce business constraints (e.g. unique email)
- Duplicate checks for phone/email
- Decide what should happen — not how it is displayed
- Call CRUD functions to persist or fetch data

### 3️⃣ CRUD Layer
**Responsibility:** Data access and persistence

- Performs direct database operations
- Contains no validation or business logic
- Talks only to SQLAlchemy models
> This keeps database logic simple and replaceable.
`src/crud/`
- `contacts.py`: CRUD operations for Contact entity
- Create a contact
- Update a contact
- Delete a contact
- Fetch contacts

### 4️⃣ Database Layer
**Responsibility:** Database schema and connection management (Infrastructure layer)

- Defines persistence schema using SQLAlchemy ORM
- Responsible only for structure and relationships
- No application logic

`src/database/`
Contains database configuration and ORM models.

- `db.py`: SQLAlchemy engine and session management
- `models.py`: Database schema definitions

### 5️⃣ Utils Layer
**Responsibility:** Shared utilities and helpers
- Contains reusable, cross-cutting logic and stateless functions
- Used by multiple layers
- Independent of UI and database
`src/utils/`
Includes:
- Input validation functions
- Data normalization functions
- formatters

### 6️⃣ Tests Layer //TODO update at the end
**Responsibility:** Unit tests for all layers
- Contains unit tests for service, CRUD, and utils layers
- Mocks UI and database interactions
`src/tests/`
- Tests business logic in `services/`
- Tests data access in `crud/`
- Tests utility functions in `utils/`

## Why This Architecture?
✅ Scales naturally with project growth
- UI can change (Streamlit → Web / Mobile) without touching logic
- Database can change (SQLite → PostgreSQL) without touching UI
✅ Clear separation of concerns
- Each layer has a single responsibility
- Business rules are testable independently
- Codebase remains readable as it grows
✅ Testability
- Business logic can be unit tested without UI or DB dependencies
- Mocks can be used for CRUD and utils during testing
✅ Real-world applicability
- Mimics production-ready architectures
- Prepares for future complexity without premature optimization
✅ Flexibility
- Easy to add new features by extending existing layers
✅ Maintainability
- Isolated changes reduce risk of bugs
- Easier onboarding for new developers
✅ Modularity
- Each layer can be developed and maintained independently
✅ Technology agnostic
- Business logic is not tied to specific frameworks or libraries
- Facilitates future migrations or integrations

## 🚀 Future Improvements
- Alembic migrations
- PostgreSQL support
- REST API layer (FastAPI)
- Authentication & authorization
- Advanced search and filtering

## Final Notes
This architecture intentionally avoids over-engineering while keeping
the project production-ready.
