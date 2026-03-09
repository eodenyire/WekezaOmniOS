# API UI Assets

This folder contains browser UI pages served by the FastAPI routes.

## Purpose

UI files here provide operator and developer-facing web experiences on top of the API.

## Files

- `console.html`
- `developer.html`

## Pages

### `console.html`

Teleport Console for runtime operations:

- node registration and refresh
- target selection
- teleport trigger actions
- bridge parameter handling from developer deploy flow

### `developer.html`

Integrated Developer IDE page:

- workspace file browser
- file read/write/create operations
- run/compile panel for multiple languages
- deploy action with production link and console handoff

## Design Notes

- Served via route modules in `api/routes/`.
- Keep API calls relative (e.g., `/developer/...`, `/teleport/...`) to work in local and proxied setups.
- Avoid embedding backend secrets in static UI files.

## Extension Guidance

When updating UI pages:

1. keep controls aligned with the active API endpoints
2. include clear status/output feedback for users
3. preserve mobile responsiveness
4. validate flow against actual route responses
