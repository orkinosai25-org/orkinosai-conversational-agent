# CMS Module - User Management and Onboarding

This module provides comprehensive CMS (Content Management System) functionality for the Orkinosai Conversational Agent, with a focus on user registration, authentication, and onboarding.

## Features

### ✅ User Registration & Authentication
- **Secure Password Storage**: Bcrypt hashing with salt
- **JWT Tokens**: Token-based authentication with 24-hour expiration
- **Input Validation**: Comprehensive validation using Pydantic models
- **Email & Phone Validation**: Proper format validation
- **Password Strength Requirements**: Minimum 8 characters, uppercase, lowercase, and digit required

### ✅ User Onboarding Workflow
- **Multi-Step Onboarding**: Welcome → Profile Setup → Organization Setup → Preferences → Training Intro → Complete
- **Progress Tracking**: Track current step, completed steps, and overall status
- **Skip Option**: Users can skip onboarding if desired
- **Data Collection**: Collect and store onboarding data at each step

### ✅ User Profile Management
- **Extended Profiles**: Job title, department, bio, avatar URL
- **User Preferences**: Theme, language, notifications, timezone, chat history
- **Custom Fields**: Flexible custom profile fields support
- **Profile Updates**: Full CRUD operations on user profiles

## Architecture

```
src/cms_module/
├── __init__.py              # Module exports
├── models/                  # Data models
│   ├── __init__.py
│   ├── user.py             # User models (User, UserCreate, UserLogin, etc.)
│   └── onboarding.py       # Onboarding models (OnboardingProgress, UserProfile, etc.)
├── services/               # Business logic
│   ├── __init__.py
│   ├── auth_service.py     # Authentication (password hashing, JWT tokens)
│   ├── user_service.py     # User management (register, login)
│   └── onboarding_service.py  # Onboarding workflow
└── db/                     # Data storage
    ├── __init__.py
    └── user_db.py          # In-memory user database (for dev/test)
```

## API Endpoints

### Authentication

#### Register a User
```bash
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe",
  "phone": "+1234567890",        # Optional
  "organization_name": "Acme"    # Optional
}

# Response (201)
{
  "message": "User registered successfully",
  "token": "eyJhbGci...",
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "is_verified": false,
    "onboarding_completed": false
  }
}
```

#### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

# Response (200)
{
  "message": "Login successful",
  "token": "eyJhbGci...",
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "last_login": "2025-12-11T21:00:00.000000"
  }
}
```

### Onboarding

#### Start Onboarding
```bash
POST /onboarding/start
Content-Type: application/json

{
  "user_id": "user_abc123"
}

# Response (200)
{
  "message": "Onboarding started successfully",
  "progress": {
    "user_id": "user_abc123",
    "current_step": "welcome",
    "completed_steps": [],
    "status": "in_progress",
    "started_at": "2025-12-11T21:00:00.000000"
  }
}
```

#### Get Onboarding Progress
```bash
GET /onboarding/progress/{user_id}

# Response (200)
{
  "user_id": "user_abc123",
  "current_step": "profile_setup",
  "completed_steps": ["welcome"],
  "status": "in_progress",
  "started_at": "2025-12-11T21:00:00.000000",
  "data": {
    "welcome": { "acknowledged": true }
  }
}
```

#### Complete Onboarding Step
```bash
POST /onboarding/step/complete
Content-Type: application/json

{
  "user_id": "user_abc123",
  "step": "profile_setup",
  "data": {
    "job_title": "Product Manager",
    "department": "Product",
    "bio": "Building great products"
  }
}

# Response (200)
{
  "message": "Step profile_setup completed successfully",
  "progress": {
    "user_id": "user_abc123",
    "current_step": "organization_setup",
    "completed_steps": ["welcome", "profile_setup"],
    "status": "in_progress"
  }
}
```

#### Skip Onboarding
```bash
POST /onboarding/skip
Content-Type: application/json

{
  "user_id": "user_abc123"
}

# Response (200)
{
  "message": "Onboarding skipped",
  "progress": {
    "user_id": "user_abc123",
    "status": "skipped"
  }
}
```

### Profile Management

#### Get User Profile
```bash
GET /profile/{user_id}

# Response (200)
{
  "user_id": "user_abc123",
  "job_title": "Product Manager",
  "department": "Product",
  "bio": "Building great products",
  "avatar_url": null,
  "preferences": {
    "theme": "light",
    "language": "en",
    "notifications_enabled": true,
    "email_notifications": true,
    "chat_history_enabled": true,
    "timezone": "UTC"
  },
  "updated_at": "2025-12-11T21:00:00.000000"
}
```

#### Update User Profile
```bash
PUT /profile/{user_id}
Content-Type: application/json

{
  "job_title": "Senior Product Manager",
  "department": "Product",
  "bio": "Passionate about user experience",
  "preferences": {
    "theme": "dark",
    "language": "en",
    "notifications_enabled": false
  }
}

# Response (200)
{
  "message": "Profile updated successfully",
  "profile": {
    "user_id": "user_abc123",
    "job_title": "Senior Product Manager",
    "department": "Product",
    "bio": "Passionate about user experience"
  }
}
```

## Onboarding Steps

1. **Welcome** (`welcome`): Introduction and welcome message
2. **Profile Setup** (`profile_setup`): Job title, department, bio
3. **Organization Setup** (`organization_setup`): Organization details
4. **Preferences** (`preferences`): Theme, language, notifications, timezone
5. **Training Intro** (`training_intro`): Introduction to training features
6. **Complete** (`complete`): Onboarding completed

## Data Models

### User
```python
{
  "id": str,                      # User ID
  "email": EmailStr,              # Email address
  "name": str,                    # Full name
  "phone": Optional[str],         # Phone number
  "organization_id": Optional[str],
  "organization_name": Optional[str],
  "is_active": bool,              # Active status
  "is_verified": bool,            # Email verified
  "created_at": datetime,
  "updated_at": datetime,
  "last_login": Optional[datetime],
  "onboarding_completed": bool
}
```

### UserProfile
```python
{
  "user_id": str,
  "job_title": Optional[str],
  "department": Optional[str],
  "bio": Optional[str],
  "avatar_url": Optional[str],
  "preferences": {
    "theme": str,                 # "light" or "dark"
    "language": str,              # ISO language code
    "notifications_enabled": bool,
    "email_notifications": bool,
    "chat_history_enabled": bool,
    "timezone": str               # IANA timezone
  },
  "custom_fields": Dict[str, Any],
  "updated_at": datetime
}
```

## Security

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- Hashed using bcrypt with automatic salt generation

### JWT Tokens
- HS256 algorithm
- 24-hour expiration
- Contains: user_id, email, name, organization_id
- Secret key configurable (default for dev only)

### Best Practices
⚠️ **IMPORTANT**: This module currently uses an in-memory database for development and testing. For production:

1. Replace `UserDatabase` with a real database (PostgreSQL, MongoDB, etc.)
2. Store JWT secret key in environment variables
3. Implement rate limiting for login endpoints
4. Add HTTPS/TLS
5. Implement CSRF protection
6. Add proper session management
7. Use environment-specific configurations
8. Add security headers (HSTS, CSP, etc.)

## Testing

The module includes comprehensive unit tests:

```bash
# Run all tests
pytest tests/test_user_registration.py tests/test_onboarding.py -v

# Run only registration tests
pytest tests/test_user_registration.py -v

# Run only onboarding tests
pytest tests/test_onboarding.py -v
```

### Test Coverage
- **Registration Tests**: 11 tests covering all registration scenarios
- **Onboarding Tests**: 9 tests covering complete onboarding workflow
- **Total**: 20 tests, all passing ✅

## Usage Example

```python
from src.cms_module import UserService, OnboardingService
from src.cms_module.models import UserCreate, OnboardingStepData, OnboardingStep

# Initialize services
user_service = UserService()
onboarding_service = OnboardingService()

# Register a user
user_data = UserCreate(
    email="user@example.com",
    password="SecurePass123",
    name="John Doe",
    phone="+1234567890"
)
response = user_service.register_user(user_data)

if response.success:
    user = response.user
    token = response.token
    
    # Start onboarding
    onboarding_response = onboarding_service.start_onboarding(user.id)
    
    # Complete welcome step
    step_data = OnboardingStepData(
        step=OnboardingStep.WELCOME,
        data={"acknowledged": True}
    )
    step_response = onboarding_service.complete_step(user.id, step_data)
```

## Migration Notes

This module was migrated from the orkinosaiCMS repository and adapted to work with the Orkinosai Conversational Agent. Key improvements:

1. **Security**: Replaced plain-text passwords with bcrypt hashing
2. **Authentication**: Replaced UUID tokens with JWT tokens
3. **Validation**: Added comprehensive Pydantic validation
4. **Testing**: Added full test coverage
5. **Documentation**: Complete API documentation
6. **Modularity**: Clean separation of concerns (models, services, db)

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Email verification workflow
- [ ] Password reset functionality
- [ ] Social authentication (OAuth)
- [ ] Two-factor authentication (2FA)
- [ ] User roles and permissions
- [ ] Organization management
- [ ] Content management features
- [ ] Document upload and management
- [ ] API rate limiting
- [ ] Audit logging

## License

MIT License - See [LICENSE](../../LICENSE) for details
