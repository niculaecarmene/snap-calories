# SnapCalories 🍽️

> WhatsApp-based nutrition tracking powered by AI vision. Know what's on your plate in seconds.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Overview

**SnapCalories** removes the friction from food tracking. Simply send a photo of your meal to our WhatsApp bot and instantly receive a detailed nutritional breakdown including:

- 🔥 Calories
- 💪 Macronutrients (Protein, Carbs, Fat, Fiber)
- 🥗 Micronutrients (Vitamins & Minerals)
- 📊 Confidence Score

**No typing. No searching. No manual entry. Just snap and know.**

## ✨ Features

### MVP v1.0

- ✅ **WhatsApp Integration** - Works directly in WhatsApp (no app download)
- ✅ **AI Vision Analysis** - Powered by Hugging Face food recognition
- ✅ **USDA Nutrition Data** - Accurate nutrition information
- ✅ **Instant Results** - < 8 second response time
- ✅ **Privacy First** - Images deleted immediately after processing (GDPR compliant)
- ✅ **Free to Use** - Built on 100% free APIs

### Coming Soon

- 📱 Daily tracking and history
- 👤 User profiles and goals
- 📈 Weekly nutrition reports
- 🏋️ Fitness app integrations

## 🏗️ Architecture

```
┌─────────────┐
│  WhatsApp   │
│    User     │
└──────┬──────┘
       │ Photo
       ▼
┌─────────────────────────────────────┐
│     WhatsApp Cloud API (Meta)       │
└──────────────┬──────────────────────┘
               │ Webhook
               ▼
┌─────────────────────────────────────┐
│       FastAPI Backend (Python)       │
│  ┌──────────────────────────────┐   │
│  │   Vision Service (HF)        │   │
│  │   Nutrition Service (USDA)   │   │
│  │   Calculator Engine          │   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │ Formatted Response
               ▼
┌─────────────────────────────────────┐
│    WhatsApp User (Nutrition Info)   │
└─────────────────────────────────────┘
```

### Technology Stack

- **Backend**: Python 3.11+ with FastAPI
- **AI Vision**: Hugging Face Inference API (free)
- **Nutrition Data**: USDA FoodData Central API (free)
- **Messaging**: WhatsApp Cloud API (Meta)
- **Image Processing**: Pillow (PIL)
- **Testing**: Pytest with async support

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- WhatsApp Business Account
- USDA API Key (free)
- Hugging Face Token (optional, for rate limit increases)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/snap-calories.git
cd snap-calories
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your API credentials
```

Required environment variables:
```bash
# WhatsApp Cloud API
WHATSAPP_API_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_chosen_verify_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_id

# USDA FoodData Central
USDA_API_KEY=your_usda_api_key

# Optional
HUGGING_FACE_TOKEN=your_hf_token
```

5. **Run the application**

```bash
# Development mode
uvicorn app.main:app --reload --port 8000

# Or using Python directly
python app/main.py
```

The API will be available at `http://localhost:8000`

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🔧 Configuration

### Getting API Keys

#### 1. WhatsApp Cloud API

1. Create a Meta Developer account at https://developers.facebook.com
2. Create a new app and add WhatsApp product
3. Get your:
   - Access Token
   - Phone Number ID
   - Business Account ID
4. Choose a verify token (any string you want)

#### 2. USDA FoodData Central API

1. Visit https://fdc.nal.usda.gov/api-key-signup.html
2. Sign up for a free API key (no credit card required)
3. Copy your API key

#### 3. Hugging Face (Optional)

1. Create account at https://huggingface.co
2. Go to Settings → Access Tokens
3. Create a new read token

### WhatsApp Webhook Setup

For local development, use ngrok to expose your local server:

```bash
# Install ngrok
brew install ngrok  # On macOS

# Start ngrok
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

Then configure your WhatsApp webhook:

1. Go to WhatsApp → Configuration in Meta Developer portal
2. Set webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
3. Set verify token: (the one you chose in .env)
4. Subscribe to `messages` webhook field

## 🧪 Testing

### Run all tests

```bash
pytest tests/ -v
```

### Run with coverage

```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Run specific test file

```bash
pytest tests/unit/test_calculator.py -v
```

### Test categories

- **Unit Tests**: `tests/unit/` - Test individual functions and classes
- **Integration Tests**: `tests/integration/` - Test API endpoints and services

## 📊 API Endpoints

### Health Check

```http
GET /health
```

Returns service status and version.

### Root

```http
GET /
```

Returns API information.

### Webhook Verification

```http
GET /webhook?hub.mode=subscribe&hub.verify_token=TOKEN&hub.challenge=CHALLENGE
```

WhatsApp webhook verification endpoint.

### Receive Messages

```http
POST /webhook
```

Receives WhatsApp messages and processes meal photos.

## 📱 Usage

### For Users

1. **Add the WhatsApp Bot** (once deployed)
2. **Take a photo** of your meal
3. **Send it** to the bot
4. **Receive** instant nutrition breakdown

### Example Response

```
🍽 Meal Analysis – SnapCalories

Estimated Calories: 645 kcal

Macros:
• Protein: 42.0g
• Carbohydrates: 58.0g
• Fat: 28.0g
• Fiber: 9.0g

Vitamins:
• Vitamin A: 35% DV
• Vitamin C: 42% DV
• Vitamin B12: 60% DV

Minerals:
• Iron: 22% DV
• Magnesium: 18% DV
• Potassium: 25% DV

Confidence: 78%

This is an AI estimate. For medical nutrition advice, consult a healthcare professional.
```

## 🏭 Deployment

### Docker (Recommended)

```dockerfile
# Dockerfile included in repository
docker build -t snapcalories .
docker run -p 8000:8000 --env-file .env snapcalories
```

### Cloud Platforms

- **AWS**: Lambda + API Gateway (serverless)
- **Google Cloud**: Cloud Run
- **Heroku**: `Procfile` included
- **DigitalOcean**: App Platform

See `CLAUDE.md` for detailed deployment instructions.

## 🔒 Security & Privacy

### GDPR Compliance

- ✅ Images deleted immediately after processing
- ✅ No personal data stored
- ✅ Stateless processing (MVP)
- ✅ Webhook signature validation

### Security Features

- API token authentication
- Webhook signature verification
- Input validation with Pydantic
- Rate limiting (recommended for production)
- HTTPS only communications

## 🗺️ Roadmap

### Phase 1: MVP ✅ (Current)

- [x] WhatsApp integration
- [x] AI vision analysis
- [x] USDA nutrition lookup
- [x] Instant results
- [x] Basic testing

### Phase 2: User Profiles (Next)

- [ ] User accounts
- [ ] Daily tracking
- [ ] Meal history
- [ ] Calorie goals
- [ ] Weekly reports

### Phase 3: Advanced Features

- [ ] Barcode scanning
- [ ] Recipe suggestions
- [ ] Fitness app integrations
- [ ] Coach dashboard
- [ ] Subscription tiers

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** - Free food recognition API
- **USDA** - Free nutrition database
- **FastAPI** - Modern Python web framework
- **Meta** - WhatsApp Cloud API

## 📞 Support

- **Documentation**: See `CLAUDE.md` for detailed specs
- **Issues**: https://github.com/yourusername/snap-calories/issues
- **Discussions**: https://github.com/yourusername/snap-calories/discussions

## ⚠️ Disclaimer

SnapCalories provides AI-estimated nutrition information for general wellness purposes only. This is **not medical advice**. For personalized nutrition guidance or medical concerns, please consult a registered dietitian or healthcare professional.

---

**Built with ❤️ using Claude Code**

🚀 [Get Started](#quick-start) | 📖 [Documentation](CLAUDE.md) | 🐛 [Report Bug](issues)
