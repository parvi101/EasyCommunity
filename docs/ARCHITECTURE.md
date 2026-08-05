# Architecture

This controlled MVP is a modular FastAPI application with a responsive installable PWA, a separate SQLite database, configuration files, API boundaries, audit events and product-specific modules. SQLite is suitable only for this local pilot build; PostgreSQL and production identity infrastructure are required before multi-venue or public production use.

## Modules
- UI/PWA
- API
- Product domain services
- Evidence and audit
- Health and freshness
- Configuration and seed data

## Phoenix lessons applied
- No product values embedded in UI logic; seed/config files hold demo content.
- Recommendations are separate from primary records.
- Health states distinguish live and stale information.
- Separate database and build directory.
- Tests and release evidence are included.
- External services are not required to install or run the build.
