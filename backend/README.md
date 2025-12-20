## Installation

1. Create virtual environment:
```bash
python -m venv venv

source venv/bin/activate  # Linux / macOS

# or
venv\Scripts\activate     # Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
   
Create or open the .env file and set the required values


4. Run application
```bash
fastapi dev
```
API will be available at:

```bash
http://127.0.0.1:8000
```