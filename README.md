# 📊 AI-Powered Natural Language to SQL Query Navigator

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![LLM Engine](https://img.shields.io/badge/LLM-Gemini%201.5%20Flash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1.svg)](https://www.mysql.com/)

An end-to-end LLM application that bridges the gap between non-technical users and relational database systems. The application securely translates unstructured natural language questions into structurally sound SQL syntax, sanitizes execution strings, manages state across web page lifecycles, and pulls live records via an encrypted hybrid network bridge.

---

## 🏗️ System Architecture & Engineering Data Flow
'''text
The application decouples user interactions from raw data layers by implementing a strictly managed 4-stage pipeline:

┌──────────────┐      Natural Language      ┌───────────────────────┐
│              │ ─────────────────────────> │   Gemini 2.5 Flash    │
│  Streamlit   │                            └───────────────────────┘
│  Frontend    │                                        │ Generates Raw SQL
│              │      Rendered Data Table               ▼
│  Dashboard   │ <───────────────────────── ┌───────────────────────┐
└──────────────┘                            │  AI Query Sanitizer   │
       ▲                                    └───────────────────────┘
       │                                                │ Sanitized SQL
       │ Routed through Tunnel                          ▼
┌───────────────────────────────────────────────────────────────────┐
│                    Secure SSH Reverse Proxy Tunnel                │
└───────────────────────────────────────────────────────────────────┘
                                | Exposed Local Port (3306)
                                ▼
                    ┌───────────────────────┐
                    │  Local MySQL Server   │
                    │      (test_db)        │
                    └───────────────────────┘
Presentation Layer: A responsive web UI built with Streamlit captures intent strings and coordinates UI state.
Cognitive Translation Layer: Prompts are appended with schema definitions and executed securely via Google's modern google-genai SDK.
Execution Sanitizer & Engine: Raw LLM outputs are processed to scrub Markdown backticks (```sql), preventing processing errors prior to local delivery.
Hybrid Network Proxy: Streamlit Cloud routes standard TCP database drivers through an encrypted reverse forwarding SSH connection, mapping the cloud execution container directly to the targeted execution port.
'''
---

## 🚀 Key Engineering Highlights (Interviewer Focus)

Next-Gen SDK Migration: Abandoned legacy, deprecated generative libraries in favor of the production-ready google-genai framework, resolving critical security token mismatch barriers.

UI State Persistence: Used st.session_state containers to cache generated database commands across server thread interactions, eliminating user session data clearing during manual table reads.

Deterministic Output Sanitization: Created a targeted parsing filter that catches and strips structural string modifiers (like markdown wraps) before payloads interact with connection strings.

Database Target Redundancy: Implemented structural view mirroring (CREATE VIEW employee AS SELECT * FROM employees;) directly inside the schema definition to guarantee structural execution resilience against linguistic variations (singular/plural names) output by the model.

---

## ⚙️ Development, Setup, & Local Configuration

1. Environment & Package Setup
Clone the repository and install the production-level system dependencies:

git clone [https://github.com/YOUR_GITHUB_USERNAME/SQL-Query-Genrator.git](https://github.com/YOUR_GITHUB_USERNAME/SQL-Query-Genrator.git)
cd SQL-Query-Genrator
pip install -r requirements.txt

2. Local Database Initialization
Launch your MySQL Command Line Client or Workbench instance and execute the baseline setup script:

-- Create Target Logical Container
CREATE DATABASE test_db;
USE test_db;

-- Establish Structural Table 
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- Seed Baseline Reporting Rows
INSERT INTO employees (id, name) VALUES 
(1, 'Alice'),
(2, 'Bob'),
(3, 'Charlie');

-- Create Fault-Tolerant Mapping Mirror View
CREATE VIEW employee AS SELECT * FROM employees;

3. Application Security Setup
To safeguard environment keys locally, create a structured credential configuration file at .streamlit/secrets.toml:

GEMINI_API_KEY = "YOUR_SECURE_AQ_API_KEY"

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "test_db"
MYSQL_USER = "YOUR_DB_USER"
MYSQL_PASSWORD = "YOUR_DB_PASSWORD"

To run the platform locally:
streamlit run ui.py

---

## 🌐 Hybrid Production Cloud Deployment Strategy

To enable a live application instance running within Streamlit Cloud to seamlessly connect to a sandboxed local database without altering physical router rules or configuring public firewalls:

1. Instantiate the Secure TCP Relay:
Leverage the host system's native SSH engine to route traffic out via port 443, creating an encrypted, zero-install reverse communications bridge:
ssh -p 443 -R0:127.0.0.1:3306 tcp@free.pinggy.io

2. Synchronize Cloud Environment Variables:
Capture the dynamic public server link and port identifier provided by the active SSH bridge shell and save them securely into the Streamlit Cloud Dashboard Secrets Console:
GEMINI_API_KEY = "YOUR_SECURE_AQ_API_KEY"

MYSQL_HOST = "badpr-xxx-xxx-xxx.run.pinggy-free.link" # Update dynamically from terminal
MYSQL_PORT = 35089                                  # Update dynamically from terminal
MYSQL_DATABASE = "test_db"
MYSQL_USER = "YOUR_DB_USER"
MYSQL_PASSWORD = "YOUR_DB_PASSWORD"

---

## 🧠 Technical Challenges Overcome & Root Cause Analysis
🧱 The Environment Grouping Conflict (TOML Parsing)
Problem: The application threw persistent st.secrets key errors when shifting codebases between automated execution modules.

Root Cause: Standard TOML specifications isolate subsequent structural parameters when structured header arrays (e.g., [connections.mysql]) are defined. This prevents programmatic direct lookup queries from mapping key paths accurately.

Resolution: Re-architected configuration structures down to explicit flat property definitions, bypassing structural grouping blockages entirely.

---

## 🌐 Cloud Container Isolation Barriers (Hybrid Network Routing)
Problem: Live code deployments threw database socket timeout warnings when addressing server targets locally.

Root Cause: Deployed cloud clusters run within isolated remote virtualized sandboxes and have no visibility over a standard user computer's looped local runtime network layer (127.0.0.1).

Resolution: Implemented a secure reverse SSH network tunnel to act as an external transport framework, allowing the isolated cloud runtime environment to query local storage resources safely.

---
