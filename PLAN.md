# 0trace — Product Plan

This document defines the end product vision for **0trace**, a browser-based fictional operating-system/economy simulation game. All hacking, cracking, mining, networking, and security mechanics are **purely fictional game mechanics**. No real system commands, real networking, real cryptocurrency, or real security tools are involved.

---

## Technical Architecture

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (App Router) + React 19 + TypeScript |
| Backend | Django 6.0 + Django REST Framework 3.17 |
| Database | MariaDB (production), SQLite (dev/test) |
| ORM | Django ORM (backend), TypeORM not used in Django backend |
| API | REST API with Swagger/OpenAPI documentation |
| Task Queue | Celery 5.6 + Redis 7 |
| Auth | Session-based, bcrypt password encryption |
| State | Everything stored in database; nothing cached except session cookies |

Frontend and backend interact via a REST API. The backend REST API features Swagger documentation.

---

## User Flow

1. **Landing Page** — Teases gameplay, game principle, tutorials, and manuals on how to play.
2. **Login / Signup** — Users authenticate from the landing page.
3. **Desktop** — After login, users are transferred to their desktop / their in-game machine.

---

## Operating Systems

All operating systems feature:
- A usable interface with an option for launching programs & apps
- A taskbar (or equivalent shell element)
- Windows with a top bar displaying the window title (app/program name)
- Three window buttons: **close**, **maximize/unmaximize**, **minimize**
- Movable windows (drag by top bar) and resizable windows (drag edges/corners)
- Standard shortcuts and keyboard bindings
- Shutdown, restart, and logout functionality (with OS-specific animations on shutdown/restart)

Users choose between different Operating Systems for their machines. From a technical standpoint the OSs are similar — they feature mostly visual differences, additional applications, different terminal command names, and percentage buffs.

All shortcuts, command names, user guides, manuals, FAQ, and "how to" instructions are explained on the website of the company or organization behind each OS.

### FruitOS (Paid — High Price)
- Extremely polished UI, extensive animations, focus on user experience and beauty
- Closed source, only features standard applications (not many extras)
- **-20%** speed for others cracking passwords of users with this OS
- Real-world equivalent: macOS

### DoorsOS (Paid — High Price, Default Free Starter OS)
- Most used OS in the world, standard desktop look and UI
- Common, focused on basic tasks, day-to-day work, office jobs, and personal use
- Basic all-rounder, very bloated
- **-20%** speed on all processing tasks (e.g., password cracking)
- Real-world equivalent: Windows 10
- **Default starter OS** — new users start with this OS for free

### ArcticOS (Free & Open Source)
- **+20%** speed on all processing tasks (e.g., password cracking)
- Excels in server tasks, extremely customizable
- At install, users choose between two Window Managers:
  - **Fruitly** — FruitOS-like look and UI
  - **Carpened** — DoorsOS-like look, slightly more polished and sleeker
- Real-world equivalent: Linux (oriented by Arch Linux)

---

## Software (GUI Applications)

Every OS includes these applications:

### Firewall
Displays the level of the selected firewall and shows all failed attempts to crack the user's password.

### Waterwall
Shows the level of the selected Waterwall and the history of password cracking attempts with their status (ongoing, failed, successful).

### Cracker
Cracks passwords of any IP given, when the user's Waterwall level is higher or equal to the target's Firewall level. Password cracking time is determined by the CPU processing power of the user's machine.

### Miner
Crypto Miner Application for mining Bitcoin / Shitcoin using CPU or GPU processing power (user-configurable). Shows stats about what and how much has been mined.

### Mail
Email application for reading and writing emails to other users.

### Browser
- Users access websites through the Browser — localhost ports for local webservers, or public webservers.
- URL format: `[http/https]://www.<domain>` (e.g., `www.example.com`)
- All sites exist only in-game; no real external websites. All websites are custom creations/recreations.
- Works like a real browser: search/URL bar at the top, defaults to `https` when protocol not specified.
- All websites (pre-defined or user-created) feature real HTML, CSS, and JS shown in the Browser.
- Only pre-defined websites can access database contents or go beyond plain HTML/CSS/JS.

#### Pre-Defined Websites

| Site | URL | Description |
|------|-----|-------------|
| **Searchable** | `searchable.com` | Simple, sleek search engine. Search bar lists existing websites and their descriptions. |
| **Microhard** | `microhard.com` | Website of the company behind DoorsOS. Buy/download DoorsOS, user guides, manuals, terminal commands. Also sells hard drives with DoorsOS pre-installed at near-free prices. |
| **Pear** | `pear.com` | Beautiful, animated website of the company behind FruitOS. Buy/download FruitOS, user guides, manuals, terminal commands. Also sells fast computer chips (P1, P1 Pro, P2…) with CPU and RAM included (no GPU support). |
| **Arctic** | `arctic.org` | Website of the Arctic open-source community behind ArcticOS. Download ArcticOS, user guides, manuals, terminal commands, Window Manager pages (Fruitly, Carpened). Public donator list and donation history for fundraising. |
| **TechHub** | `techhub.com` | Largest hardware retailer. Buy CPUs, GPUs, motherboards, HDDs, SSDs, USB sticks, RAM, PC casings, etc. at reasonable prices. Some hard drives include DoorsOS at a slight price increase. |
| **SecondLife** | `secondlife.com` | Player-to-player marketplace. Users buy and sell software and hardware. Users can only sell hardware parts from their inventory (Resources App). |
| **CryptFront** | `cryptfront.trade` | Crypto trading platform. Buy/sell crypto coins (bought or mined). Features price graphs. Users can create/delete crypto wallets and send coins to other existing wallets. |
| **Domania** | `domania.com` | Buy domains and HTTPS certificates for hosting user-created websites. Domains are linked to the user and their machine. |
| **Deliveries** | `deliveries.com` | Package delivery company for all online shopping. Default delivery: 2 hours. Express Delivery subscription (monthly) reduces delivery to 20 minutes. |

### Webserver Software
Self-hosting websites to display in the Browser. Websites are programmed in real HTML, CSS, and JS. Different names per OS.

### Resources
Manage machine hardware. Features: current equipped hardware view, inventory, and trash section. Only equipped parts are used and provide their processing power.

### Settings
Configure system settings (themes: dark mode / light mode, etc.) and view system information (OS version, user IP, etc.).

### App Store Software
Install and uninstall all applications. The App Store, Settings, and Resources apps cannot be uninstalled. Different names per OS.

### Terminal
Classic terminal application. Design and commands differ between OSs.

- Features all standard commands and commands to show all available commands.
- Commands for creating, editing, and removing files and directories.
- Terminal commands for every GUI Application listed above (except Resources, Browser, and Mail).
- **SSH command** for logging into other machines using IP and password.
- Commands heavily inspired by real-world equivalents:
  - **FruitOS**: macOS/Unix-based commands (e.g., `nano` for file editing, `sudo` for privileges)
  - **DoorsOS**: Windows 10-based commands
  - **ArcticOS**: Linux/Arch Linux/Unix-based commands (e.g., `nano` for file editing, `sudo` for privileges)
- Privilege system: `sudo` for FruitOS and ArcticOS (e.g., `sudo nano /etc/filename` for privileged files/directories).

### Skills
View skills and levels. Level software with XP.

---

## Game Mechanics

### Skill & Software Leveling + XP System

**Skills:**
- Hacking, Mining, etc.
- Higher skill levels increase performance (e.g., faster password cracking).

**Software Leveling:**
- Software can be leveled with XP (e.g., Firewall level upgrades bought with XP).
- **IMPORTANT:** All software (Firewalls, Waterwalls, Crackers, Miners, etc.) are just files selected in their respective apps. Leveling software means leveling the specific files. Users can sell these software files on marketplaces like SecondLife.

**XP Gaining:**
- XP is gained by cracking passwords, mining crypto, etc.

### Money System

- Money is earned by selling crypto coins on trading sites (e.g., CryptFront).
- Money is spent on hardware from retail sites (e.g., TechHub).

### Hardware Trading

- All physical items bought online have a **2-hour delivery time** and are only available in the Resources App inventory after delivery.
- Users can subscribe to an **Express Delivery** subscription (monthly) for **20-minute delivery**.

### Hardware Slots

- When buying new hardware (GPU, CPU, hard drive, RAM), it gets added to the system if the motherboard has free slots.
- If no slot is free, the item can't be bought until the current item is removed from the slot.
- This principle applies to all hardware items.
