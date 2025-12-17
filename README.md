# TrendScout: E-Commerce Intelligence Collector

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)

## Overview
**TrendScout** is a robust automated data extraction tool designed to harvest real-time competitive intelligence from dynamic e-commerce platforms (specifically **Myntra**). 

Unlike traditional static scrapers, TrendScout leverages **Selenium WebDriver** to simulate human interaction, allowing it to bypass anti-bot detection, handle JavaScript-rendered content, and manage "lazy-loading" assets effectively.

---

## Key Features

* **Dynamic Content Handling:** Capable of scraping single-page applications (SPAs) where data is loaded via JavaScript (React/Angular).
* **User Simulation:** Implements automated scrolling and "Human-like" delays to trigger lazy-loading images and avoid IP bans.
* **Anti-Bot Evasion:** Uses custom User-Agent headers and randomized wait times to mimic a legitimate Chrome browser session.
* **Structured Output:** Transforms unstructured HTML data into a clean, analysis-ready **CSV dataset** containing:
    * Product Brand & Name
    * Price (Discounted & Original)
    * Deep Links (Product URLs)
    * Breadcrumb Navigation paths

---

## Tech Stack

* **Core Logic:** Python
* **Browser Automation:** Selenium WebDriver
* **Driver Management:** `webdriver-manager` (Auto-installs correct Chrome drivers)
* **Data Processing:** Pandas
* **Target Site:** Myntra (Personal Care Category)

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/TrendScout.git](https://github.com/yourusername/TrendScout.git)
cd TrendScout
