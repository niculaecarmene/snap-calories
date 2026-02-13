# SnapCalories - AI-Powered Meal Nutrition Tracker

## 🎯 Project Vision

**SnapCalories** is a WhatsApp-based nutrition tracking application that allows users to instantly receive nutritional breakdowns of their meals by simply sending a photo.

**Core Promise:**
> "Know what's on your plate in seconds."

## 👤 Target Users

### Primary
- Health-conscious individuals
- Busy professionals
- Gym members
- Weight loss users
- Women 35–45 tracking hormones/metabolism

### Secondary
- Nutrition coaches
- Personal trainers
- Online wellness communities

## 💡 Problem Statement

Users want to track food but:
- Logging manually is time-consuming
- Apps require typing/searching foods
- Portion estimation is difficult
- Most users quit tracking after 2–3 weeks

**SnapCalories removes friction:** Photo → instant analysis → zero typing.

## 🏗 Technical Architecture

### Technology Stack

#### Backend
- **Framework:** Python FastAPI (async, high-performance)
- **Language:** Python 3.11+
- **API Gateway:** FastAPI with automatic OpenAPI documentation

#### AI/ML Components
- **Vision Model:** OpenAI Vision API (GPT-4 Vision) for food recognition
- **Image Processing:** Computer Vision for portion estimation

#### Data Layer
- **Database:** PostgreSQL (for future user profiles and meal history)
- **Nutrition Data:** USDA FoodData Central API

#### Messaging Platform
- **Integration:** WhatsApp Cloud API (Meta)
- **Protocol:** Webhook-based message handling

#### Deployment
- **Cloud Provider:** AWS / GCP serverless
- **Architecture:** Event-driven, serverless functions
- **Scalability:** Auto-scaling based on demand

### System Components

1. **WhatsApp Business API** - Message receiver and sender
2. **Backend API** - FastAPI service for request orchestration
3. **Image Processing AI** - OpenAI Vision model for food detection
4. **Nutrition Database API** - USDA FoodData Central integration
5. **Calculation Engine** - Macro and micronutrient computation
6. **Response Formatter** - WhatsApp message formatter

## 🛠 Recommended Agent Skills

The following agent skills from the skills.sh ecosystem are recommended for this project. Install them to enhance development capabilities.

### WhatsApp Integration Skills

**Primary Skills:**
- `gokapso/agent-skills@integrate-whatsapp` - WhatsApp integration patterns and setup
  ```bash
  npx skills add gokapso/agent-skills@integrate-whatsapp
  ```

- `gokapso/agent-skills@whatsapp-messaging` - WhatsApp messaging workflows
  ```bash
  npx skills add gokapso/agent-skills@whatsapp-messaging
  ```

- `gokapso/agent-skills@observe-whatsapp` - WhatsApp message monitoring and webhooks
  ```bash
  npx skills add gokapso/agent-skills@observe-whatsapp
  ```

### Python FastAPI Backend Skills

**Primary Skills:**
- `mindrally/skills@fastapi-python` - FastAPI development best practices
  ```bash
  npx skills add mindrally/skills@fastapi-python
  ```

- `0xdarkmatter/claude-mods@python-fastapi-patterns` - FastAPI architectural patterns
  ```bash
  npx skills add 0xdarkmatter/claude-mods@python-fastapi-patterns
  ```

- `jezweb/claude-skills@fastapi` - FastAPI implementation guidelines
  ```bash
  npx skills add jezweb/claude-skills@fastapi
  ```

### AI/Computer Vision Skills

**Primary Skills:**
- `jezweb/claude-skills@openai-api` - OpenAI API integration patterns
  ```bash
  npx skills add jezweb/claude-skills@openai-api
  ```

- `mindrally/skills@computer-vision-opencv` - Computer vision and image processing
  ```bash
  npx skills add mindrally/skills@computer-vision-opencv
  ```

- `pluginagentmarketplace/custom-plugin-ai-data-scientist@computer-vision` - Advanced CV techniques
  ```bash
  npx skills add pluginagentmarketplace/custom-plugin-ai-data-scientist@computer-vision
  ```

### Database & API Integration Skills

**Primary Skills:**
- `manutej/luxor-claude-marketplace@postgresql-database-engineering` - PostgreSQL patterns
  ```bash
  npx skills add manutej/luxor-claude-marketplace@postgresql-database-engineering
  ```

- `davila7/claude-code-templates@api-integration-specialist` - API integration patterns
  ```bash
  npx skills add davila7/claude-code-templates@api-integration-specialist
  ```

- `daffy0208/ai-dev-standards@api-integration-builder` - API integration builder
  ```bash
  npx skills add daffy0208/ai-dev-standards@api-integration-builder
  ```

### AWS/Serverless Deployment Skills

**Primary Skills:**
- `davila7/claude-code-templates@aws-serverless` - AWS serverless architecture
  ```bash
  npx skills add davila7/claude-code-templates@aws-serverless
  ```

- `sickn33/antigravity-awesome-skills@aws-serverless` - Serverless best practices
  ```bash
  npx skills add sickn33/antigravity-awesome-skills@aws-serverless
  ```

- `zxkane/aws-skills@aws-serverless-eda` - Event-driven serverless architecture
  ```bash
  npx skills add zxkane/aws-skills@aws-serverless-eda
  ```

### Testing & Quality Assurance Skills

**Primary Skills:**
- `bobmatnyc/claude-mpm-skills@pytest` - Pytest testing patterns
  ```bash
  npx skills add bobmatnyc/claude-mpm-skills@pytest
  ```

- `wshobson/agents@python-testing-patterns` - Python testing best practices
  ```bash
  npx skills add wshobson/agents@python-testing-patterns
  ```

- `pluginagentmarketplace/custom-plugin-python@pytest-testing` - Advanced pytest techniques
  ```bash
  npx skills add pluginagentmarketplace/custom-plugin-python@pytest-testing
  ```

### Documentation Skills

**Primary Skills:**
- `sickn33/antigravity-awesome-skills@api-documentation-generator` - API documentation
  ```bash
  npx skills add sickn33/antigravity-awesome-skills@api-documentation-generator
  ```

- `davila7/claude-code-templates@quality-documentation-manager` - Documentation management
  ```bash
  npx skills add davila7/claude-code-templates@quality-documentation-manager
  ```

### Quick Install All Recommended Skills

```bash
# WhatsApp
npx skills add gokapso/agent-skills@integrate-whatsapp -y
npx skills add gokapso/agent-skills@whatsapp-messaging -y

# Backend
npx skills add mindrally/skills@fastapi-python -y
npx skills add 0xdarkmatter/claude-mods@python-fastapi-patterns -y

# AI/Vision
npx skills add jezweb/claude-skills@openai-api -y
npx skills add mindrally/skills@computer-vision-opencv -y

# Database & APIs
npx skills add manutej/luxor-claude-marketplace@postgresql-database-engineering -y
npx skills add davila7/claude-code-templates@api-integration-specialist -y

# Deployment
npx skills add davila7/claude-code-templates@aws-serverless -y

# Testing
npx skills add bobmatnyc/claude-mpm-skills@pytest -y
npx skills add wshobson/agents@python-testing-patterns -y

# Documentation
npx skills add sickn33/antigravity-awesome-skills@api-documentation-generator -y
```

## 📋 MVP Scope & Requirements

### User Flow

1. **User Action:** Sends photo of meal to WhatsApp bot
2. **System Processing:**
   - Receives image via WhatsApp webhook
   - Validates image (format, size < 10MB)
   - Sends to OpenAI Vision for food detection
   - Estimates portion sizes using visual cues
   - Queries USDA nutrition database
   - Calculates total nutritional values
3. **Bot Response:** Formatted nutrition breakdown with confidence score

### Functional Requirements

#### Input Specifications
- **Format:** JPG, PNG
- **Max Size:** 10MB
- **Constraint:** One plate per image (v1 limitation)
- **Quality:** Minimum 480x480 pixels recommended

#### AI Processing Pipeline

**Step 1: Food Recognition**
- Identify all visible food items on the plate
- Detect multiple ingredients per dish
- Classify food categories (protein, vegetables, grains, etc.)

**Step 2: Portion Estimation**
- Estimate grams per food item
- Use plate size heuristics and visual scaling
- Apply standard portion size references

**Step 3: Nutrition Calculation**
- Map detected items to USDA FoodData Central
- Calculate total macronutrients (Protein, Carbs, Fat, Fiber)
- Calculate total calories
- Compute key micronutrients (Vitamins A, C, B12, Iron, Magnesium, Potassium)
- Generate confidence score based on detection certainty

#### Output Format (WhatsApp Response)

```
🍽 Meal Analysis – SnapCalories

Estimated Calories: 645 kcal

Macros:
Protein: 42g
Carbohydrates: 58g
Fat: 28g
Fiber: 9g

Vitamins:
Vitamin A: 35% DV
Vitamin C: 42% DV
Vitamin B12: 60% DV

Minerals:
Iron: 22% DV
Magnesium: 18% DV
Potassium: 25% DV

Confidence: 78%
(This is an AI estimate.)
```

### MVP Constraints & Limitations

**What's NOT included in MVP:**
- ❌ Medical-grade accuracy
- ❌ Allergy detection
- ❌ Long-term meal tracking
- ❌ User profiles or personalization
- ❌ Multi-meal or daily history
- ❌ Personalized nutrition recommendations
- ❌ Barcode scanning
- ❌ Recipe suggestions

**What IS included:**
- ✅ Single meal instant analysis
- ✅ Photo-based food recognition
- ✅ Calorie and macro estimation
- ✅ Basic micronutrient breakdown
- ✅ Confidence scoring
- ✅ WhatsApp integration
- ✅ Fast response (< 8 seconds)

### Ultra-Lean v0 Option

For rapid prototyping, consider starting with minimal output:
- Calories only
- Protein, Carbs, Fat
- Skip vitamins/minerals initially
- No user accounts
- No data storage
- Stateless processing

## ⚙️ Development Guidelines & Best Practices

### Code Quality Standards

#### Python/FastAPI Conventions
- **Style Guide:** Follow PEP 8
- **Type Hints:** Use type annotations for all functions
- **Async/Await:** Prefer async endpoints for I/O operations
- **Pydantic Models:** Use Pydantic for request/response validation
- **Error Handling:** Implement comprehensive error handling with custom exceptions
- **Logging:** Use structured logging (JSON format) for production

#### Project Structure
```
snap-calories/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── api/
│   │   ├── webhooks.py      # WhatsApp webhook handlers
│   │   └── health.py        # Health check endpoints
│   ├── services/
│   │   ├── whatsapp.py      # WhatsApp API integration
│   │   ├── vision.py        # OpenAI Vision processing
│   │   ├── nutrition.py     # USDA API integration
│   │   └── calculator.py    # Nutrition calculation logic
│   ├── models/
│   │   ├── message.py       # Message models
│   │   └── nutrition.py     # Nutrition data models
│   ├── utils/
│   │   ├── image.py         # Image processing utilities
│   │   └── formatting.py    # Response formatting
│   └── config.py            # Configuration management
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
└── README.md
```

### Non-Functional Requirements

#### Performance
- **Response Time:** < 8 seconds (target: 5-6 seconds)
- **Concurrent Users:** Support 100+ concurrent requests
- **Image Processing:** Optimize for batch processing if needed
- **Caching:** Implement Redis caching for repeated queries

#### Security
- **API Keys:** Store in environment variables, never in code
- **Webhook Validation:** Verify WhatsApp webhook signatures
- **Rate Limiting:** Implement rate limiting (e.g., 10 requests/minute per user)
- **Image Validation:** Sanitize and validate all uploaded images
- **HTTPS Only:** All communications must use HTTPS

#### Data Privacy & GDPR Compliance
- **Image Deletion:** Auto-delete images immediately after processing
- **No PII Storage:** Don't store personal information without consent
- **Data Retention:** No data retention in MVP (stateless)
- **User Consent:** Include disclaimer in response messages
- **Right to Deletion:** Implement data deletion capability for future phases

#### Reliability
- **Error Recovery:** Graceful error handling with user-friendly messages
- **Retry Logic:** Implement exponential backoff for external API calls
- **Circuit Breaker:** Use circuit breaker pattern for external services
- **Monitoring:** Implement health checks and alerting
- **Logging:** Comprehensive logging for debugging

### Testing Strategy

#### Unit Tests
- Test individual functions and methods
- Mock external API calls
- Aim for >80% code coverage
- Use pytest fixtures for test data

#### Integration Tests
- Test API endpoints end-to-end
- Test WhatsApp webhook handling
- Test external API integrations (with test accounts)
- Test database operations (if applicable)

#### E2E Tests
- Simulate complete user journey
- Test with real WhatsApp test numbers
- Validate response format and timing
- Test error scenarios

### Environment Variables

```bash
# WhatsApp Cloud API
WHATSAPP_API_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_id

# OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4-vision-preview

# USDA FoodData Central
USDA_API_KEY=your_usda_key

# Database (for future use)
DATABASE_URL=postgresql://user:pass@host:5432/snapcalories

# Application
ENVIRONMENT=development  # development, staging, production
LOG_LEVEL=INFO
MAX_IMAGE_SIZE_MB=10
RESPONSE_TIMEOUT_SECONDS=8

# AWS/Cloud (if applicable)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### API Integration Guidelines

#### WhatsApp Cloud API
- **Webhook Setup:** Use ngrok for local development
- **Message Types:** Handle text and image messages
- **Status Updates:** Implement read receipts
- **Error Responses:** Send user-friendly error messages

#### OpenAI Vision API
- **Image Encoding:** Convert to base64 or use URL
- **Prompt Engineering:** Use specific prompts for food detection
- **Token Limits:** Monitor token usage for cost optimization
- **Fallback:** Implement fallback for API failures

#### USDA FoodData Central
- **Data Format:** Use Foundation Foods or SR Legacy datasets
- **Caching:** Cache frequently requested food items
- **Fuzzy Matching:** Implement fuzzy string matching for food names
- **Fallback:** Use generic values if exact match not found

### Deployment Checklist

#### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] WhatsApp webhook verified
- [ ] API rate limits configured
- [ ] Monitoring and logging enabled
- [ ] Error tracking integrated (Sentry, etc.)
- [ ] Load testing completed

#### Post-Deployment
- [ ] Health check endpoint responding
- [ ] Webhook receiving messages
- [ ] Test with real WhatsApp number
- [ ] Monitor response times
- [ ] Check error rates
- [ ] Verify GDPR compliance (image deletion)

### Success Metrics (MVP)

**Technical Metrics:**
- Average response time: < 6 seconds
- API uptime: > 99.5%
- Error rate: < 2%
- Food detection accuracy: > 75%

**User Metrics:**
- 70%+ users send more than 2 meals
- 30% conversion to paid (future) within 30 days
- Retention > 40% after 2 weeks
- User satisfaction score > 4.0/5.0

### Future Roadmap

#### Phase 2 Features
- Daily calorie tracking
- User profiles (weight, height, goals)
- Macro target setting
- Meal history storage
- Weekly nutrition reports

#### Phase 3 Features
- Hormonal cycle-based nutrition tracking
- Coach dashboard for trainers
- Subscription tiers (Free vs Pro)
- WhatsApp reminders and tips
- Integration with fitness apps

### Support & Resources

- **WhatsApp Cloud API Docs:** https://developers.facebook.com/docs/whatsapp/cloud-api
- **OpenAI Vision Docs:** https://platform.openai.com/docs/guides/vision
- **USDA FoodData Central:** https://fdc.nal.usda.gov/api-guide.html
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Skills Marketplace:** https://skills.sh/

---

## 🚀 Quick Start Commands

```bash
# Install recommended skills
bash install_skills.sh

# Set up Python environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v --cov=app

# Deploy to AWS (example)
# Configure AWS credentials first
serverless deploy --stage production
```

---

**Last Updated:** 2026-02-11
**Project Status:** Planning Phase
**Next Steps:** Install recommended skills, set up development environment, implement MVP v1.0

