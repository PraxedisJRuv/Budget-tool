# Budget Tool
Allows to record financial data regarding income, expenses, buys, so you can have a complete record unified in a single dashboard amd database.

## Features
- Record a buy (expense record, buy record, item record, product types)
- Track expenses (Record, view history, search by concept)
- Record Income (multiple sources, search and manage)
- Track Debt (log money borrowed, borrower info, interest rates, total debt)
- Dashboard with metrics, calculations, recent activity and quick overview.

## Tech Stack
| Layer        | Technology              |
|-------------|--------------------------|
| API    | Fastapi, pydantic |
| Database | SQLite, SQLmodel, SQLalchemy |
| Data         | Pandas |
| Visualization| Streamlit, plotly, CSS |

## Installation

1. git clone https://github.com/PraxedisJRuv/Budget-tool.git

2. Create a virtual environment    
    ```bash
        python -m venv venv
        venv\Scripts\activate
    ```

3. Install dependencies
    ```bash
        pip install requirements.txt
    ```

## Usage

1. Locate yourself in the functional prototype
    ```bash
        cd prototype
    ```

2. Start  the engine (API and Backend)
    ```bash
        fastapi run app.py
    ```

3. Run the frontend application
    ```bash
        streamlit run streamlit_app.py
    ```

4. Access http://localhost:8501

## Project Structure

```
Budget-tool/
├── deprecated_version/        #ignore it, it has didactic purpose only
├── Important notes/            
├── prototype/
│   ├── app.py                 # FastAPI backend
│   ├── models.py              # Data models
│   ├── utils.py               # Database and API utilities
│   ├── streamlit_app.py       # Streamlit frontend
│   └── database.db            # SQLite data
├── .gitattributes
├── .gitignore
├──  LICENSE
├── README.md
├── requirements.txt
└── 
```
