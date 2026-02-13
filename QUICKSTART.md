# SnapCalories Quick Start Guide

Get up and running in 5 minutes! ⚡

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] WhatsApp Business Account created
- [ ] USDA API key obtained (free)
- [ ] Internet connection

## Step-by-Step Setup

### 1. Install Dependencies (2 minutes)

```bash
# Run the automated setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys (1 minute)

Edit `.env` file with your credentials:

```bash
# Required
WHATSAPP_API_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=any_string_you_choose
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_id
USDA_API_KEY=your_usda_key

# Optional
HUGGING_FACE_TOKEN=your_hf_token
```

**Where to get API keys:**

1. **WhatsApp**: https://developers.facebook.com → Create App → Add WhatsApp
2. **USDA**: https://fdc.nal.usda.gov/api-key-signup.html
3. **Hugging Face** (optional): https://huggingface.co/settings/tokens

### 3. Start the Server (30 seconds)

```bash
uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/docs to see the API!

### 4. Expose Locally with ngrok (1 minute)

```bash
# Install ngrok (if not installed)
# macOS: brew install ngrok
# Windows: Download from ngrok.com

# Start ngrok
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

### 5. Configure WhatsApp Webhook (1 minute)

1. Go to WhatsApp → Configuration in Meta Developer Console
2. Set Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
3. Set Verify Token: (same as in your .env)
4. Subscribe to "messages" field
5. Click "Verify and Save"

## Test Your Setup

### Test 1: Health Check ✅

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-13T...",
  "service": "SnapCalories",
  "version": "1.0.0"
}
```

### Test 2: Webhook Verification ✅

The WhatsApp setup will automatically test this when you click "Verify and Save"

### Test 3: Send a Meal Photo 📸

1. Open WhatsApp on your phone
2. Send a message to your WhatsApp Business number
3. Send a photo of a meal
4. Wait ~5-8 seconds
5. Receive nutrition breakdown!

## Troubleshooting

### Issue: "Module not found"
**Solution**: Activate virtual environment
```bash
source venv/bin/activate
```

### Issue: "Webhook verification failed"
**Solution**: Check that `WHATSAPP_VERIFY_TOKEN` in .env matches webhook config

### Issue: "No response from bot"
**Solution**:
1. Check server logs for errors
2. Verify ngrok is running
3. Check WhatsApp webhook subscriptions

### Issue: "Invalid image"
**Solution**: Ensure photo is:
- JPG or PNG format
- Under 10MB
- At least 200x200 pixels

## Development Tips

### View API Documentation
http://localhost:8000/docs - Interactive Swagger UI

### Run Tests
```bash
pytest tests/ -v
```

### View Logs
All logs appear in terminal where uvicorn is running

### Hot Reload
The `--reload` flag auto-restarts server when code changes

## Next Steps

Once everything works:

1. ✅ Test with different meal photos
2. ✅ Review accuracy of results
3. ✅ Adjust portion estimation logic if needed
4. ✅ Deploy to production (see README.md)
5. ✅ Share with users!

## Common Commands

```bash
# Start server
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v --cov=app

# Format code
black app/ tests/

# Check types
mypy app/

# Build Docker image
docker build -t snapcalories .

# Run Docker container
docker run -p 8000:8000 --env-file .env snapcalories
```

## Support

- 📖 Full Documentation: See README.md
- 🐛 Issues: Check logs and .env configuration
- 💬 Questions: See CLAUDE.md for detailed specs

---

**Ready to track meals? Send your first photo! 🍽️📸**
