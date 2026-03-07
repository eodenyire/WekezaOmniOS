---
# 🧪 WekezaOmniOS Teleportation Tests

This folder contains the automated testing suite for Phase 1 of the **Universal Application Teleportation (UAT)** engine. Following **Rule 8: Everything Must Be Testable**, this suite provides the "safety net" required to ensure process integrity during capture, transfer, and restoration.

## 🎯 Purpose

* **Validation:** Ensures that Phase 1 mock and initial logic behave as expected.
* **Integrity:** Guarantees that the teleportation system never corrupts a process state during the snapshot cycle.
* **Living Documentation:** Provides developers with clear examples of how each module is intended to function.
---

## 📜 Engineering Rules

* **Rule 8 Compliance:** No logic enters the `universal-teleportation` core without a corresponding test case.
* **Framework:** Built on `pytest` for clean, scalable, and modular testing.
* **Isolation:** Tests utilize mock PIDs and temporary directories to ensure the host system remains unaffected during validation.
---

## 🛠️ Coverage Areas

The test suite is divided into three primary pillars:

1. **State Capture (`test_capture.py`)**
* Verifies `CaptureManager` initialization.
* Validates process metadata retrieval (name, status, PID).
* Ensures capture directories are created correctly.


2. **Snapshot Engine (`test_snapshot.py`)**
* Verifies the creation of `.tar.gz` packages.
* Ensures metadata is correctly bundled within the snapshot.
* Validates archive integrity.


3. **Process Restore (`test_restore.py`)**
* Verifies `RestoreManager` initialization.
* Tests "Snapshot Not Found" error handling.
* Simulates environment rehydration and process resumption.
---

## 🚀 Example Usage

To run the full suite and see the detailed output, execute the following from the root directory:

```bash
# Run all tests with verbose output
pytest -v

```
---

## 🔗 Integration & Validation Flow

The testing suite acts as the final gatekeeper in the teleportation pipeline:

```text
Capture Logic ⮕ Snapshot Packaging ⮕ Local Storage ⮕ Reconstruction ⮕ [ TEST VALIDATION ]

```
* **Phase 1:** Uses placeholder PIDs and mock data to simulate successful cycles.
* **Future Phases:** Will incorporate real-time **CRIU** dump validation and network latency testing for the transfer layer.
---

## 📂 Folder Structure

```text
tests/
├── README.md           # Documentation for the test suite
├── test_capture.py     # Logic for state capture validation
├── test_snapshot.py    # Logic for snapshot packaging validation
└── test_restore.py     # Logic for process reconstruction validation

```
---
