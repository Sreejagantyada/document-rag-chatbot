# 1️⃣ Base image (Linux + Python)
FROM python:3.11-slim

# 2️⃣ Set working directory inside container
WORKDIR /app

# 3️⃣ Copy dependency list first (important for caching)
COPY requirements.txt .

# 4️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy project files
COPY . .

# 6️⃣ Expose FastAPI port
EXPOSE 8000

# 7️⃣ Start FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
