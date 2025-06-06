# 🤖 Langchain API Hub

A comprehensive Django-based AI services platform with user authentication, API key management, and 8 powerful AI-powered text processing APIs.

## 🌟 Features

### Authentication System

- **User Registration & Login**: Secure signup and login system
- **API Key Management**: Automatic API key generation for each user
- **Dashboard**: User dashboard with API key management and usage statistics
- **Middleware Authentication**: Secure API endpoints with API key validation

### AI Services (8 APIs)

1. **📝 Text Summarization** - Extract key points from long texts
2. **😊 Sentiment Analysis** - Analyze emotional tone of text
3. **🔑 Keyword Extraction** - Extract important keywords and phrases
4. **🏷️ Text Classification** - Categorize text into different topics
5. **🌐 Language Detection** - Identify the language of input text
6. **🔄 Text Translation** - Translate text between multiple languages
7. **❓ Question Answering** - Get answers to questions with optional context
8. **✨ Content Generation** - Generate various types of content

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Django 5.2+
- Google Gemini API key

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd service_hub
   ```

2. **Install dependencies**

   ```bash
   pip install django djangorestframework python-dotenv langchain-google-genai
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open http://127.0.0.1:8000 in your browser

## 🔐 Authentication Flow

### User Registration

1. Visit `/signup/` to create a new account
2. Fill in username, email, and password
3. Upon successful registration, an API key is automatically generated
4. User is redirected to the home page

### User Login

1. Visit `/login/` to sign in
2. Enter username and password
3. Access dashboard at `/dashboard/` to view API key and statistics

### API Key Usage

- **Header Method**: Include `X-API-Key: your_api_key` in request headers
- **Body Method**: Include `"api_key": "your_api_key"` in request body

## 📡 API Endpoints

### Authentication Endpoints

- `GET /` - Home page with API testing interface
- `GET /login/` - Login page
- `POST /login/` - Process login
- `GET /signup/` - Registration page
- `POST /signup/` - Process registration
- `GET /dashboard/` - User dashboard
- `POST /logout/` - Logout user
- `POST /regenerate-api-key/` - Generate new API key

### AI Service Endpoints

All endpoints require API key authentication:

| Endpoint            | Method | Description         |
| ------------------- | ------ | ------------------- |
| `/summarize/`       | POST   | Text summarization  |
| `/sentiment/`       | POST   | Sentiment analysis  |
| `/keywords/`        | POST   | Keyword extraction  |
| `/classify/`        | POST   | Text classification |
| `/detect-language/` | POST   | Language detection  |
| `/translate/`       | POST   | Text translation    |
| `/answer/`          | POST   | Question answering  |
| `/generate/`        | POST   | Content generation  |

## 🔧 API Usage Examples

### Text Summarization

```javascript
fetch("/summarize/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-Key": "your_api_key_here",
  },
  body: JSON.stringify({
    text: "Your long text here...",
    method: "stuff", // 'stuff', 'map_reduce', or 'refine'
  }),
});
```

### Sentiment Analysis

```javascript
fetch("/sentiment/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-Key": "your_api_key_here",
  },
  body: JSON.stringify({
    text: "I love this product!",
  }),
});
```

### Text Translation

```javascript
fetch("/translate/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-Key": "your_api_key_here",
  },
  body: JSON.stringify({
    text: "Hello, how are you?",
    target_language: "Spanish",
  }),
});
```

### Content Generation

```javascript
fetch("/generate/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-Key": "your_api_key_here",
  },
  body: JSON.stringify({
    prompt_text: "Write a professional email",
    content_type: "email",
    max_length: 500,
  }),
});
```

## 🏗️ Project Structure

```
service_hub/
├── ai_services/                 # Main Django app
│   ├── logic/                  # AI service logic
│   │   ├── summarizer.py       # Text summarization
│   │   ├── sentiment_analyzer.py # Sentiment analysis
│   │   ├── keyword_extractor.py # Keyword extraction
│   │   ├── text_classifier.py  # Text classification
│   │   ├── language_detector.py # Language detection
│   │   ├── text_translator.py  # Text translation
│   │   ├── question_answerer.py # Question answering
│   │   ├── content_generator.py # Content generation
│   │   └── gemini_setup.py     # Gemini API setup
│   ├── templates/              # HTML templates
│   │   └── ai_services/
│   │       ├── home.html       # Main interface
│   │       ├── login.html      # Login page
│   │       ├── signup.html     # Registration page
│   │       └── dashboard.html  # User dashboard
│   ├── models.py              # Database models
│   ├── views.py               # API views
│   ├── auth_views.py          # Authentication views
│   ├── serializers.py         # API serializers
│   ├── middleware.py          # API key middleware
│   └── urls.py                # URL patterns
├── service_hub/               # Django project settings
│   ├── settings.py           # Project settings
│   └── urls.py               # Main URL configuration
└── manage.py                 # Django management script
```

## 🎨 Frontend Features

### Responsive Design

- Modern gradient-based UI design
- Mobile-responsive layout
- Interactive service cards
- Real-time API testing interface

### User Experience

- Sample data pre-loaded for testing
- Loading spinners and progress indicators
- Success/error message handling
- Copy-to-clipboard functionality for API keys

## 🔒 Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **API Key Authentication**: Secure API access with unique keys
- **Password Validation**: Strong password requirements
- **Session Management**: Secure user session handling
- **Middleware Protection**: All API endpoints protected by authentication middleware

## 📊 Admin Interface

Access Django admin at `/admin/` to:

- View and manage user accounts
- Monitor API key usage
- View API usage statistics
- Manage user permissions

## 🧪 Testing

Run the included test script:

```bash
python test_auth.py
```

This tests:

- User registration
- User login
- API key authentication
- API endpoint functionality

## 🚀 Deployment

### Vercel Deployment

This project is configured for easy deployment on Vercel:

1. **Install Vercel CLI**

   ```bash
   npm install -g vercel
   ```

2. **Set Environment Variables**
   Configure these in your Vercel dashboard:

   ```
   SECRET_KEY=your-secret-django-key
   DEBUG=False
   SUPABASE_DB_NAME=your_db_name
   SUPABASE_DB_USER=your_db_user
   SUPABASE_DB_PASSWORD=your_db_password
   SUPABASE_DB_HOST=your_db_host
   SUPABASE_DB_PORT=5432
   GOOGLE_API_KEY=your-google-api-key
   ```

3. **Deploy**

   ```bash
   vercel --prod
   ```

4. **Test Production Settings Locally**
   ```bash
   python test_production.py
   ```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🚀 Deployment Considerations

### Production Settings

- Set `DEBUG = False`
- Configure secure database (PostgreSQL recommended)
- Set up proper static file serving
- Configure HTTPS
- Set secure session cookies
- Use environment variables for all secrets

### Environment Variables

```env
SECRET_KEY=your_django_secret_key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your_database_url
GOOGLE_API_KEY=your_gemini_api_key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Write tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the documentation
2. Run the test script to verify setup
3. Check Django logs for errors
4. Ensure all environment variables are set

## 🔮 Future Enhancements

- Rate limiting for API calls
- Usage analytics and billing
- Additional AI models integration
- Bulk processing capabilities
- API versioning
- Webhook support
- Team collaboration features
