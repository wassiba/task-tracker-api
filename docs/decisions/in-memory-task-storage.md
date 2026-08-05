# Decision: Use an In-Memory Dictionary as the Task Storage Layer

## 1. Context
The Task Tracker API is the implementation project used throughout the AI Assisted Coding course. It combines a FastAPI and Pydantic backend with a standalone JavaScript Kanban frontend. During the course, I extended and verified the application’s CRUD operations, status-transition rules, due dates, overdue detection, search and filtering, drag-and-drop interaction, automated tests, continuous integration, Docker configuration, documentation, and AI-assisted review. The backend remains authoritative for stored task data and status changes.
The application currently stores its tasks in a module-level Python dictionary in `app/storage.py`. It has no database or file-based persistence, so all task data is lost when the API process exits. The automated tests also use this storage implementation and call `storage._reset()` before and after each test to provide an isolated starting state.
I accepted this design because the course deliberately limited the project’s infrastructure so that I could focus on AI-assisted coding methodology and engineering verification rather than database administration. I therefore did not formally compare storage alternatives when the application was first developed. Although the README and `CLAUDE.md` document the in-memory store and its limitations, the reasoning behind accepting it was not previously recorded as a dedicated decision. I am writing this note now to make that rationale explicit and to identify the conditions under which persistent storage should be reconsidered.

## 2. Decision
For the current course project, I will retain the module-level in-memory dictionary in `app/storage.py` as the Task Tracker API’s storage layer. The application will continue to create, retrieve, filter, update, and delete tasks through the existing storage functions, without adding a database or file-based persistence.
This decision applies only to the Task Tracker in its present role as an AI-assisted coding course project. It does not represent a recommended storage architecture for a production or multi-user application. Introducing persistent storage will remain a separate future decision requiring its own requirements, design, implementation, migration, and verification work.

## 3. Alternatives Considered
I did not formally evaluate alternative storage technologies when the Task Tracker’s storage layer was established. The in-memory dictionary was already part of the course project’s simplified scope, and I accepted it without comparing or prototyping other approaches. The following alternatives are therefore retrospective options for a future version, not solutions that I evaluated and rejected at the time.

### SQLite

SQLite could provide persistence for a small, locally operated version of the Task Tracker without requiring a separate database server. It would introduce relational tables, migrations, and database integration while keeping installation and operation relatively simple. Its suitability would need to be reconsidered if the application later required several concurrent users or multiple deployed API instances.

### PostgreSQL

PostgreSQL would be a stronger candidate for a deployed, multi-user application. It could provide shared persistent storage, transactions, indexing, concurrency support, and a clearer path to multiple API workers or containers. It would also require additional configuration, credentials, migrations, database administration, integration testing, backups, and deployment planning.

I would evaluate these alternatives only when persistent data becomes a verified requirement. The choice should depend on the application’s expected users, deployment model, data volume, concurrency needs, and operational responsibilities rather than on which database is considered more advanced.

## 4. Trade-offs
Using an in-memory dictionary allowed me to focus on the AI-assisted engineering workflow instead of database administration. I did not need to configure a database server, manage credentials, design tables, write migrations, or maintain separate development and test databases. This kept the storage implementation small and transparent, making it easier to inspect Claude’s claims against the actual code.
The design also simplified testing and learning. The test fixture can call `storage._reset()` before and after every test, giving each of the 37 tests a clean and predictable starting point. This helped me concentrate on the application’s CRUD operations, validation, status-transition rules, filtering, overdue behavior, frontend integration, CI, Docker, documentation, and AI-assisted review. For the course’s intended scope, this simplicity was a genuine advantage.
The main cost is that every task disappears when the API process or container restarts. That would be unacceptable in a real task-management application because users must be able to rely on their work remaining available across sessions, updates, and service interruptions. The dictionary is also private to one Python process, so multiple workers or container instances would not automatically share the same task state. A real multi-user application would therefore need shared persistent storage. Despite these limitations, the dictionary was the right temporary choice for this course because it supported the required learning objectives without introducing database complexity before it was needed.
I would do this differently by documenting the storage decision at the beginning of the project and defining a small repository interface, while still using the in-memory dictionary during the early course stages.

## 5. Consequences

- The Task Tracker can demonstrate its complete verified feature set—including task creation, editing, deletion, filtering, overdue identification, status-transition enforcement, and the Kanban interface—while the API process remains running.
- All task data is lost whenever the API process stops, restarts, or is replaced by a new container. The application therefore cannot yet serve as a dependable task-management tool for users who expect their work to remain available across sessions.
- Automated tests remain fast and isolated because the existing fixture calls `storage._reset()` before and after each of the 37 tests. If a database is introduced, the project will need a new isolation strategy, such as transaction rollback, temporary databases, or controlled fixture data.
- The module-level dictionary belongs to one Python process. Because each operating-system process has its own memory, multiple API workers or container instances would be expected to maintain separate task state rather than share one authoritative data source. This is an architectural inference from the current implementation; the repository does not configure or test multiple workers or replicas. The present implementation should therefore continue to run as a single application instance unless the storage architecture is changed.
- Introducing persistence later will require more than replacing one dictionary. The project will need a deliberate storage boundary, database models, migrations, configuration, integration tests, and a migration plan while preserving the existing FastAPI routes, Pydantic validation, business rules, and verified API behavior.
- This decision does not add authentication, authorization, database persistence, deployment, or production-readiness claims. Those capabilities remain outside the current course-project scope and require separate decisions and verification.

## 6. Open Questions

- Should the first persistent version use SQLite for a simple local application, or PostgreSQL to support a deployed multi-user application?
- Where should I introduce a repository boundary so that the existing FastAPI routes, Pydantic models, and business rules can remain stable when the dictionary is replaced?
- How should the current test suite be divided between fast isolated tests and database integration tests, and how should database state be reset safely between tests?
- At what point should authentication, authorization, and per-user task ownership be introduced?
- If users have already created tasks before persistence is added, how should that existing data be migrated without changing the verified API behavior?
- Should the overdue rule become exclusively backend-authoritative so that the frontend no longer maintains a separate implementation that must be kept synchronized?
