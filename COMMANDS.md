# SnapCalories - Command Reference Card

Quick reference for common operations.

## 🚀 Setup & Installation

```bash
# Automated setup
./setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## ▶️ Running the Application

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Using Python directly
python app/main.py

# Using Docker
docker build -t snapcalories .
docker run -p 8000:8000 --env-file .env snapcalories
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_calculator.py -v

# Run unit tests only
pytest tests/unit/ -v

# Run integration tests only
pytest tests/integration/ -v

# Run in watch mode (requires pytest-watch)
pytest-watch
```

## 🔍 Code Quality

```bash
# Format code with Black
black app/ tests/

# Check formatting
black app/ tests/ --check

# Lint with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/

# Sort imports
isort app/ tests/
```

## 🔧 Development Tools

```bash
# Verify setup
python3 verify_setup.py

# Start ngrok for local testing
ngrok http 8000

# Check Python syntax
python3 -m py_compile app/**/*.py

# Count lines of code
find app -name "*.py" | xargs wc -l
```

## 📊 API & Documentation

```bash
# View API docs
open http://localhost:8000/docs        # Swagger UI
open http://localhost:8000/redoc       # ReDoc

# Health check
curl http://localhost:8000/health

# Test webhook verification
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=TEST"
```

## 🐳 Docker Commands

```bash
# Build image
docker build -t snapcalories .

# Run container
docker run -p 8000:8000 --env-file .env snapcalories

# Run in background
docker run -d -p 8000:8000 --env-file .env --name snapcal snapcalories

# View logs
docker logs snapcal

# Stop container
docker stop snapcal

# Remove container
docker rm snapcal

# Shell into container
docker exec -it snapcal /bin/bash
```

## 🔐 Environment Management

```bash
# Create .env from template
cp .env.example .env

# Check required variables
grep "^[A-Z]" .env

# Validate .env (requires python-dotenv)
python -c "from dotenv import load_dotenv; load_dotenv(); print('✅ .env loaded')"
```

## 📝 Git Commands

```bash
# Initial commit
git init
git add .
git commit -m "Initial commit: SnapCalories MVP"

# Create develop branch
git checkout -b develop

# Check status
git status

# View changes
git diff
```

## 🐛 Debugging

```bash
# View logs in real-time
tail -f logs/app.log

# Check port 8000 is available
lsof -i :8000

# Kill process on port 8000
kill $(lsof -t -i:8000)

# Python debug mode
python -m pdb app/main.py

# Test specific function
python -c "from app.services.calculator import nutrition_calculator; print(nutrition_calculator)"
```

## 📦 Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt

# Update dependencies
pip list --outdated
pip install --upgrade <package>

# Generate requirements
pip freeze > requirements.txt

# Check for security issues
pip-audit
```

## 🌐 Deployment

```bash
# AWS Lambda (using Zappa)
zappa init
zappa deploy production

# Heroku
heroku create snapcalories
git push heroku main

# Google Cloud Run
gcloud run deploy snapcalories --source .

# DigitalOcean App Platform
doctl apps create --spec .do/app.yaml
```

## 🔄 WhatsApp Setup

```bash
# 1. Start local server
uvicorn app.main:app --reload

# 2. Start ngrok in another terminal
ngrok http 8000

# 3. Copy ngrok URL and configure in Meta Developer Console
# Webhook URL: https://YOUR-NGROK-URL.ngrok.io/webhook

# 4. Test webhook
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 📊 Performance Monitoring

```bash
# Profile Python code
python -m cProfile -o profile.stats app/main.py

# View profile results
python -m pstats profile.stats

# Memory profiling
python -m memory_profiler app/main.py

# Load testing with locust
locust -f tests/load_test.py --host=http://localhost:8000
```

## 🗂️ File Operations

```bash
# View project structure
tree -I '__pycache__|venv|.git'

# Count files
find . -name "*.py" | wc -l

# Find TODO comments
grep -r "TODO" app/

# Search for pattern
grep -r "class.*Service" app/
```

## 📚 Documentation

```bash
# Generate API docs
python -m pdoc --html app/ -o docs/

# View README
cat README.md

# View quick start
cat QUICKSTART.md

# View implementation summary
cat IMPLEMENTATION_SUMMARY.md
```

## 🆘 Troubleshooting

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# Clear temp images
rm -rf temp_images/*

# Reset virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"

# Verify imports
python -c "from app.main import app; print('✅ Import successful')"
```

---

## 💡 Quick Tips

1. **Always activate venv first**: `source venv/bin/activate`
2. **Use --reload for development**: `uvicorn app.main:app --reload`
3. **Check logs for errors**: Watch terminal output
4. **Use ngrok for WhatsApp testing**: Exposes local server
5. **Run tests before committing**: `pytest tests/ -v`
6. **Keep .env secure**: Never commit .env file

---

**More help?**
- 📖 Full docs: `README.md`
- 🚀 Quick start: `QUICKSTART.md`
- 🔍 Verify setup: `python3 verify_setup.py`
