# Metropolis Metro Signaling --- Line G Interlocking System

[![CentraleSupélec](https://img.shields.io/badge/CentraleSupélec-EI%202026-B11116?style=flat-square)](https://www.centralesupelec.fr/)
[![Prover iLock](https://img.shields.io/badge/Prover-iLock%20%7C%20Studio-0A2540?style=flat-square)](https://www.prover.com/)
[![Formal Verification](https://img.shields.io/badge/Safety-SIL%204%20%2F%20EN%2050128-success?style=flat-square)]()
[![Specification Language](https://img.shields.io/badge/Language-PiSPEC%203.0-blue?style=flat-square)]()
[![Simulation](https://img.shields.io/badge/Simulation-MQTT%20Distributed-orange?style=flat-square)]()

Engineering team project for the modernization of the **Metropolis Metro signaling network**, conducted in partnership with **CentraleSupélec** and **Prover Technology**. 

**Engineering Group 7** is responsible for the design, formal safety verification, and distributed simulation of **Line G**, connecting *Parc des Expositions* to *Technopôle* across five computer-based interlocking stations.

---

## 📌 Table of Contents
- [Executive Overview](#-executive-overview)
- [Line G Infrastructure](#-line-g-infrastructure)
- [System Architecture (SDA Paradigm)](#-system-architecture-sda-paradigm)
- [Engineering Backlog & Implementations](#-engineering-backlog--implementations)
- [Formal Safety Verification (GSS)](#-formal-safety-verification-gss)
- [Testing & Distributed Simulation (GTS & MQTT)](#-testing--distributed-simulation-gts--mqtt)
- [Project Structure](#-project-structure)
- [Toolchain & Setup](#-toolchain--setup)
- [Team Members & Role Distribution](#-team-members--role-distribution)
- [References & Norms](#-references--norms)

---

## 🏙️ Executive Overview

The transport authority, the City of Metropolis Mobility and Transport Department (*Direction de la Mobilité et des Transports*), is replacing its 40-year-old electro-mechanical relay interlockings across all 8 lines with modern Computer-Based Interlockings (CBI). 

To ensure provable zero-defect safety under strict CENELEC EN 50128 standards, the authority adopted Prover's **Signaling Design Automation (SDA)** methodology. This project delivers:
1. **Specific Applications (SA)**: Complete interlocking station models drawn from track schematics.
2. **Generic Application (GA)**: Scalable railway logic, safety properties, and test suites written in **PiSPEC**.
3. **Formal Verification**: Mathematical model checking (100% PROVED) via Prover PSL.
4. **Interactive Simulation**: Full-line multi-station MQTT train simulation across physical borders.

---

## 🗺️ Line G Infrastructure

Line G runs west-to-east ($W \to E$) along a double-track corridor (Track 2 Eastbound on top, Track 1 Westbound on bottom), serving five interlocking installations:

| # | Station Name | Project Code | Station Type | Switches | Signals | Interchanges |
|---|--------------|--------------|--------------|:--------:|:-------:|:------------:|
| 1 | **Parc des Expositions** | `G-PEX` | Terminus (5 platform tracks, dead-end buffers) | 5 | 15 | --- |
| 2 | **Emerson** | `G-EME` | Double crossover + siding track ($P_6$) | 5 | 18 | Line H |
| 3 | **Abrial** | `G-ABR` | 4-track passing station + 2 dead-end sidings ($P_9, P_{10}$) | 6 | 20 | --- |
| 4 | **Clarke** | `G-CLA` | Scissors crossover + siding track ($P_{11}$) | 5 | 15 | Line D |
| 5 | **Technopôle** | `G-TEC` | Fan-shaped terminus (5 platform tracks) | 5 | 22 | Line C |
| **Total** | | | **5 Interlocking Stations** | **26** | **90** | |

---

## ⚙️ System Architecture (SDA Paradigm)

The project decouples generic signaling rules from local station geography:

```
+--------------------------------------------------------------------------+
|                        Generic Application (GA)                          |
|  - Object Model (OM): Signals, Switches, Route Sections, Routes, Blocks  |
|  - Generic Design (GDS): Interlocking logic, Line Block, Manual Release  |
|  - Generic Safety (GSS): Mathematical safety invariants (PiSPEC)         |
|  - Generic Tests (GTS): Regression test suites                           |
+--------------------------------------------------------------------------+
                                     |
                                     v  [Instantiation]
+--------------------------------------------------------------------------+
|                    Specific Applications (SA: Line G)                    |
|  - Railyard Layouts: G-PEX, G-EME, G-ABR, G-CLA, G-TEC                  |
|  - Topologic Tables: t_path_*, t_area_*, t_track_number (LCF)           |
+--------------------------------------------------------------------------+
                  |                                      |
                  v                                      v
   +------------------------------+       +------------------------------+
   |   Prover iLock Verifier      |       |    Prover iLock Simulator    |
   |   Formal Model Checking      |       |    Distributed MQTT Broker   |
   |   (Mathematical Proofs)      |       |    (Full-Line Simulation)    |
   +------------------------------+       +------------------------------+
```

---

## 📋 Engineering Backlog & Implementations

All engineering tasks from the Metropolis Backlog (MPS) were resolved:

- **MPS-1 (Creating a New Interlocking):**
  - Drew and compiled layouts for all five Line G stations in Prover iLock Layout Editor (L-Phase).
  - Validated transitions to Tool Phase (T-Phase) with complete topological attribute checks.
- **MPS-4 (Formalizing Safety Requirements):**
  - Formalized requirements `GSS_02`, `GSS_08`, `GSS_09`, and `GSS_10` using universal/existential quantifiers and the temporal operator `PRE`.
- **MPS-13 (Adding Test Cases):**
  - Authored Test Case 2 (`GTS_SWITCH.tm`) verifying that occupied track circuits lock switches against manual throw requests.
- **MPS-16 (Line Block Interface):**
  - Enhanced `GSS_06` to mandate line input clearance for exit signals.
  - Implemented exit signal logic in GDS (`EXIT_SIGNAL.tm`) and safety requirements `EXIT_1` and `EXIT_2`.
  - Added Test Case 3 (`GTS_ROUTE.tm`) validating route locking inhibition when `LineInput` is false.
- **MPS-21 (Manual Route Release):**
  - Extended Object Model (`ROUTE.tm`) with `RequestManualRelease` and a 30-second delay countdown timer.
  - Updated GDS route and route section equations to immediately revoke signal proceed aspects and simultaneously release route sections upon timer expiration.
  - Authored Test Case 4 validating approach locking timing and simultaneous unlocking.
- **MPS-27 & MPS-28 (Interactive Line Simulation):**
  - Configured distributed MQTT simulation over `localhost:1883`, synchronizing border handoffs ($SeG1/2\text{-}XXX\text{-}E \leftrightarrow SeG1/2\text{-}XXX\text{-}W$) and shared boundary track circuits ($VG1/2\text{-}XXX$).

---

## 🛡️ Formal Safety Verification (GSS)

All 12 formal safety properties achieved mathematical proof (**100% PROVED**) with the Prover iLock Verifier across all five stations of Line G:

| Formal Requirement | Description | Verification Status |
|:-------------------|:------------|:-------------------:|
| `GSS_01` | Signal proceed aspect implies a unique, set route | **PROVED** |
| `GSS_02` | Route sections sharing track circuits cannot be locked concurrently | **PROVED** |
| `GSS_03` | All switches in a cleared route match required correspondence positions | **PROVED** |
| `GSS_04` | All track circuits within a cleared route are clear of occupancy | **PROVED** |
| `GSS_05` | Flank protection is established and protective for all switches in the route | **PROVED** |
| `GSS_06` | Route end protection: buffer stop, line block clear, proceeding signal, or front protection | **PROVED** |
| `GSS_07` | Switches cannot move if locked in a route section or serving as protective objects | **PROVED** |
| `GSS_08` | Route sections can only become ready to release if occupied by a train | **PROVED** |
| `GSS_09` | Route sections must be locked to be ready to release | **PROVED** |
| `GSS_10` | Route section release requires track clearance and previous-cycle release readiness | **PROVED** |
| `EXIT_1` | Exit signal `LineOutput` is only asserted when unreserved and uncommanded | **PROVED** |
| `EXIT_2` | Exit signal can only clear to proceed if end-locked, line input is true, and line is vacant | **PROVED** |

---

## 🚆 Testing & Distributed Simulation (GTS & MQTT)

```
[G-PEX] <--- SeG1/2-PEX ---> [G-EME] <--- SeG1/2-EME ---> [G-ABR] <--- SeG1/2-ABR ---> [G-CLA] <--- SeG1/2-CLA ---> [G-TEC]
   |                           |                           |                           |                           |
   +---------------------------+---------------------------+---------------------------+---------------------------+
                                                           |
                                           +-------------------------------+
                                           | Local MQTT Broker (localhost) |
                                           +-------------------------------+
```

The interactive simulation verifies end-to-end line operation:
- Trains spawn on terminus platform tracks, acquire cleared routes, traverse intermediate crossovers, and transfer cleanly across boundary blocks.
- Border signal status ($SeG1/2\text{-}XXX\text{-}E/W$) and boundary track circuits ($VG1/2\text{-}XXX$) synchronize in real-time over MQTT topics.

---

## 📂 Project Structure

```text
metropolis-metro-signaling/
├── README.md                           # Project documentation and specifications
├── .gitignore                          # Clean build exclusions (LaTeX, binaries, logs)
├── deliverables/
│   ├── members.txt                     # Team members and detailed engineering roles
│   ├── report/
│   │   ├── report.tex                  # Comprehensive LaTeX project report
│   │   ├── ref.bib                     # Academic and technical bibliography
│   │   ├── logo/
│   │   │   ├── LogoCS.pdf              # CentraleSupélec institutional logo
│   │   │   └── LogoProver.pdf          # Prover Technology brand vector logo
│   │   └── img/                        # Visual assets and schematics
│   └── slides/                         # Final defense presentation materials
├── docs/                               # System documentation and city technical dossiers
│   ├── Metropolis-Renovation-reseau-metro.pdf
│   ├── Metropolis-Backlog-MPS.pdf
│   ├── presentation-intro.pdf
│   ├── prover-intro.pdf
│   ├── om.pdf, gss.pdf, gts.pdf
├── packages/
│   ├── Metropolis_GA/                  # Generic Application package
│   │   ├── OM/                         # Object Model (.tm files)
│   │   ├── GDS/                        # Generic Design Specification equations
│   │   ├── GSS/                        # Generic Safety Specification rules
│   │   ├── GTS/                        # Generic Test Specification testcases
│   │   └── scripting/                  # Python simulation & MQTT configuration
│   └── [Prover toolchain libraries]    # Supporting LCF, SEIF, and integration packages
└── projects/                           # Specific Applications (Line G)
    ├── G-PEX/                          # Parc des Expositions Interlocking Project
    ├── G-EME/                          # Emerson Interlocking Project
    ├── G-ABR/                          # Abrial Interlocking Project
    ├── G-CLA/                          # Clarke Interlocking Project
    └── G-TEC/                          # Technopôle Interlocking Project
```

---

## 🛠️ Toolchain & Setup

- **Prover iLock (v5.29+)**: For station layout editing, topological compilation, and interactive simulation.
- **Prover PSL & Verifier**: For automated SIL 4 formal verification and inductive invariant proofs.
- **Prover Studio**: Visual Studio Code extension for PiSPEC generic specification development.
- **Local MQTT Broker**: Eclipse Mosquitto or embedded Prover MQTT broker listening on `localhost:1883`.
- **LaTeX Environment**: TeX Live / Overleaf with `pdflatex` and `biber` to compile `deliverables/report/report.tex`.

---

## 👥 Team Members & Role Distribution

*Sorted in alphabetical order by surname:*

### **Tiago Closs**
* **Role:** Station Modeling (SA), Line Simulation & Safety Formalization
* Modeled interlocking stations `G-EME` (Emerson) and `G-PEX` (Parc des Expositions).
* Formalized safety requirement `GSS_10` (route section release condition with `PRE` operator) in PiSPEC.
* Configured and executed the multi-station interactive simulation over MQTT (MPS-27, MPS-28).
* Contributed to formal verification, technical reporting, and presentation.

### **Gabriel da Costa**
* **Role:** Station Modeling (SA), Generic Design & Testing
* Modeled interlocking stations `G-CLA` (Clarke) and `G-TEC` (Technopôle).
* Extended the Object Model (OM) and Generic Design (GDS) for manual route release (MPS-21, MPS-22, MPS-24).
* Implemented GTS test cases for switch throwing (Test Case 2), line block (Test Case 3), and manual release (Test Case 4).
* Formalized requirement `GSS_09` and corrected definitions for `GSS_01`, `GSS_03`, and `GSS_07`.
* Configured and executed the multi-station interactive simulation over MQTT (MPS-27, MPS-28).
* Contributed to technical reporting and presentation.

### **Pedro Lubaszewski Lima**
* **Role:** Project Architecture, Station Modeling (SA) & Safety Verification
* Managed repository architecture, development workflow, and technical documentation.
* Modeled interlocking station `G-ABR` (Abrial).
* Formalized and strengthened requirements `GSS_06`, `GSS_08`, `EXIT_1`, and `EXIT_2` in PiSPEC.
* Debugged and verified the generic design and line block interface in Prover iLock (MPS-18, MPS-20).
* Contributed to technical reporting and presentation.

### **Sebastián Pari Medina**
* **Role:** Safety Specification (GSS) & Model Checking
* Formalized safety requirements `GSS_02` (mutual exclusion of shared tracks) and `EXIT_1` / `EXIT_2` in PiSPEC.
* Performed formal verification and counterexample analysis using Prover iLock Verifier.
* Contributed to formal verification, technical reporting, and presentation.

---

## 📚 References & Norms

1. **CENELEC EN 50128:2011** --- *Railway applications: Communication, signalling and processing systems --- Software for railway control and protection systems.*
2. **Prover Technology** --- *Prover iLock Documentation: PiSPEC Language Reference Manual*, Stockholm, 2026.
3. **Prover Technology** --- *Signaling Design Automation (SDA): From Specification to Verified Interlocking*, 2026.
4. **Ville de Metropolis, DMT** --- *Programme Renouvellement Signalisation: Dossier Technique*, Réf. DMT/RS/2026-11, 2026.
5. **E. M. Clarke, E. A. Emerson, and J. Sifakis** --- *Model Checking: Algorithmic Verification and Debugging*, Communications of the ACM, 52(11):74–84, 2009.
