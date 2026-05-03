# 🏦 Student Bank Portal

A desktop banking simulation application built with Python and Tkinter, designed for students to manage a virtual bank account through a clean, modern UI.

> **Project by Bazif & Sawaira** — CS/Programming course project

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation & Running](#installation--running)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Authors](#authors)

---

## Overview

Student Bank Portal is a fully local desktop application that simulates basic banking operations. It allows students to create personal accounts using their Student ID, log in securely, and perform deposits and withdrawals — all tracked in a live transaction history. No internet connection or database is required; all data lives in memory during the session.

---

## Features

- **Account Creation** — Register with your full name, a unique Student ID, and a password. Duplicate Student IDs are rejected to ensure one account per student.
- **Secure Login** — Authenticate using your auto-generated account number and password.
- **Dashboard** — View your available balance and masked account number at a glance.
- **Deposit & Withdraw** — Perform transactions through a clean modal dialog with real-time balance updates.
- **Transaction History** — The dashboard logs your 8 most recent deposits and withdrawals with color-coded indicators.
- **Input Placeholders** — Create Account fields show example formatting (`John Doe`, `202xx-12345`) to guide users.
- **Modern Dark UI** — A polished dark-gold theme built entirely with Tkinter — no external UI libraries needed.

---

## Requirements

- Python **3.10 or higher** (uses `X | Y` union type hints)
- No third-party packages — only Python standard library modules:
  - `tkinter`
  - `random`
  - `string`

To check your Python version:

```bash
python --version
```

---

## Installation & Running

1. **Clone the repository**

```bash
git clone https://github.com/your-username/student-bank-portal.git
cd student-bank-portal
```

2. **Run the application**

```bash
python cpps_project.py
```

> On some Linux systems, Tkinter may need to be installed separately:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## How to Use

### Creating an Account
1. Launch the app and click **Create Account**
2. Enter your full name, Student ID, and choose a password
3. Click **Create Account** — a unique 10-digit account number will be generated and displayed
4. **Save your account number** — you'll need it to log in

### Logging In
1. From the home screen, click **Login**
2. Enter your account number and password
3. Click **Login** to access your dashboard

### Making Transactions
- Click **↓ Deposit** to add funds
- Click **↑ Withdraw** to withdraw funds (insufficient balance is blocked)
- All transactions appear instantly in the **Recent Activity** log

---

## Project Structure

```
student-bank-portal/
│
├── cpps_project.py      # Main application — all logic and UI in one file
└── README.md            # This file
```

### Code Architecture

| Class | Responsibility |
|---|---|
| `Account` | Data model storing owner info, balance, and transaction history |
| `BankApp` | Core application — manages all screens, UI helpers, and business logic |

Key methods inside `BankApp`:

| Method | Description |
|---|---|
| `show_home()` | Landing screen with Create Account / Login buttons |
| `show_create_account()` | Registration form with duplicate Student ID validation |
| `show_login()` | Login form with account number + password authentication |
| `show_dashboard()` | Main user screen showing balance, actions, and transaction log |
| `show_deposit()` / `show_withdraw()` | Transaction modal dialogs |
| `_entry()` | Reusable styled input field with placeholder and focus effects |

---

## Authors

**Bazif** & **Sawaira**
Computer Programming / CS Course Project

---

> *Data is stored in memory only and does not persist between sessions. Closing the application resets all accounts.*
