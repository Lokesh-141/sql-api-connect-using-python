# sql-api-connect-using-python  

# College Info API Integration  

This project integrates data from an API (generated via Google Apps Script from a Kaggle dataset) into a Microsoft SQL Server database. It automates the extraction and storage of Indian engineering college information.


## 📂 Project Structure

```

📁 college-info-api
├── colleges.py          # Python script to fetch API data and insert into SQL Server
├── README.md            # Project documentation

````

## 📌 Features

- Converts a Kaggle dataset into a REST API using Google Apps Script.
- Fetches data from the API.
- Inserts data into SQL Server (`college_api` database) without duplications.
- Creates table `college_info` if not already existing.

## 🛠️ Prerequisites

- Python 3.8+
- SQL Server (local or remote)
- Required Python packages: `requests`, `pyodbc`

Install dependencies:

```bash
pip install requests pyodbc
````

## 🗃️ Database Schema

**Database**: `college_api`
**Table**: `college_info`

| Column  | Type         | Description                |
| ------- | ------------ | -------------------------- |
| id      | VARCHAR(5)   | Primary key, college ID    |
| college | VARCHAR(80)  | Name of the college        |
| city    | VARCHAR(255) | City where the college is  |
| state   | VARCHAR(50)  | State where the college is |

## 🔌 API Source

* The data originates from a Kaggle dataset: [Engineering Colleges in India](https://www.kaggle.com/datasets/shrirangmhalgi/engineering-colleges-in-india)
* A Google Apps Script web app publishes this data as a JSON API.

## ✅ Functionality

* Automatically checks for duplicate `id` values before inserting.
* Ensures data persistence without overwriting existing rows.
* Efficient API-to-DB transfer for clean automation.

## 📄 License

This project is licensed under the MIT License.
