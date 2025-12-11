# Onboarding Integration with CMS

This document describes the onboarding integration system that leverages the CMS features from orkinosai25-org/orkinosaiCMS. The integration provides a complete user onboarding experience with content management, welcome flows, and scalable configuration.

## Overview

The onboarding system provides a multi-step wizard that guides new users through initial setup. It integrates with the CMS to enable:

- **Dynamic Content Management**: All step content is managed through the CMS, allowing updates without code changes
- **Personalized User Welcome Flows**: Content can be personalized based on user context (name, role, etc.)
- **Scalable Configuration**: Easy to add new steps, modify flows, and customize per organization
- **Progress Tracking**: Comprehensive tracking of user progress through onboarding steps
- **State Management**: Resume interrupted onboarding sessions seamlessly

## Architecture

### Components

The onboarding system consists of four main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Onboarding System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌─────────────────────────────────┐ │
│  │  Data Models     │  │  OnboardingContentManager       │ │
│  │  (models.py)     │  │  (content_manager.py)           │ │
│  │                  │  │                                 │ │
│  │ • OnboardingStep │  │ • Manages step content         │ │
│  │ • OnboardingFlow │  │ • CMS integration              │ │
│  │ • UserProgress   │  │ • Personalization              │ │
│  └──────────────────┘  │ • Localization support         │ │
│                        └─────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OnboardingService (service.py)                      │  │
│  │                                                       │  │
│  │ • Flow initialization and management                 │  │
│  │ • Step progression and validation                    │  │
│  │ • State persistence and recovery                     │  │
│  │ • Progress tracking                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints (onboarding_routes.py)               │  │
│  │                                                       │  │
│  │ • RESTful API for onboarding flows                   │  │
│  │ • Progress tracking endpoints                        │  │
│  │ • Step navigation                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

#### OnboardingStep
Represents a single step in the onboarding flow. Each step contains:
- Unique identifier
- Step type (WELCOME, PROFILE, ORGANIZATION, etc.)
- Order in the flow
- CMS-managed content (title, description, HTML)
- Configuration options
- Validation rules
- Skip capability

#### OnboardingFlow
Defines a complete onboarding flow with multiple steps. Supports:
- Multiple flow types (user, organization, admin)
- Conditional steps based on user role or plan
- Dynamic step ordering
- Customizable content per step

#### UserOnboardingProgress
Tracks user progress through an onboarding flow:
- Current step position
- Completed steps
- Collected data from each step
- Overall completion status
- State management (NOT_STARTED, IN_PROGRESS, COMPLETED, etc.)

### CMS Integration

The system integrates with CMS features in several ways:

1. **Content Management**: All step content is managed through the `OnboardingContentManager`, which acts as a bridge to CMS content storage.

2. **Dynamic Content Loading**: Step content is loaded dynamically based on:
   - Step type
   - User context (name, role, organization)
   - Locale (for internationalization)

3. **Personalization**: Content can include template variables that are replaced with user-specific data:
   ```python
   # Example: Welcome message personalization
   "Welcome to Orkinosai, {user_name}! 🚀"
   # Becomes: "Welcome to Orkinosai, John! 🚀"
   ```

4. **Version Control**: The CMS content manager supports content versioning for A/B testing and gradual rollouts.

## Usage

### Starting the Onboarding Flow

When a new user registers, start the onboarding flow:

```python
from src.cms.onboarding import OnboardingService

# Initialize service
service = OnboardingService()

# Start onboarding for a new user
progress = service.start_onboarding(
    user_id="user-123",
    flow_type="user_onboarding",
    metadata={
        'source': 'website',
        'referrer': 'google'
    }
)

print(f"Onboarding started: {progress.id}")
```

### Getting the Current Step

Retrieve the current step with CMS content:

```python
# Get current step with personalization
step = service.get_current_step(
    progress_id=progress.id,
    user_context={
        'name': 'John Doe',
        'role': 'Developer'
    }
)

print(f"Current step: {step.title}")
print(f"Description: {step.description}")
print(f"Content: {step.content}")
```

### Completing a Step

When a user completes a step, record the data and advance:

```python
# Complete step with collected data
success = service.complete_step(
    progress_id=progress.id,
    step_id=step.id,
    step_data={
        'profile': {
            'name': 'John Doe',
            'role': 'Developer',
            'company': 'Acme Inc.'
        }
    }
)

if success:
    # Get next step
    next_step = service.get_current_step(progress.id)
    if next_step:
        print(f"Next step: {next_step.title}")
    else:
        print("Onboarding complete!")
```

### Skipping Optional Steps

Users can skip non-required steps:

```python
# Skip optional step (e.g., theme selection)
success = service.skip_step(
    progress_id=progress.id,
    step_id=step.id
)
```

## API Endpoints

The onboarding system exposes RESTful API endpoints:

### List Available Flows

```bash
GET /api/onboarding/flows
```

Response:
```json
{
  "success": true,
  "flows": [
    {
      "id": "user_onboarding",
      "name": "user_onboarding",
      "title": "User Onboarding",
      "description": "Standard onboarding flow for new users",
      "steps": [...],
      "is_active": true
    }
  ]
}
```

### Start Onboarding

```bash
POST /api/onboarding/start
Content-Type: application/json

{
  "user_id": "user-123",
  "flow_type": "user_onboarding",
  "metadata": {
    "source": "website",
    "referrer": "google"
  }
}
```

Response:
```json
{
  "success": true,
  "progress": {
    "id": "progress-123",
    "user_id": "user-123",
    "flow_id": "user_onboarding",
    "state": "in_progress",
    "current_step_index": 0,
    "started_at": "2025-12-11T18:30:00Z"
  }
}
```

### Get Current Step

```bash
GET /api/onboarding/progress/progress-123/current-step?user_name=John&user_role=Developer
```

Response:
```json
{
  "success": true,
  "step": {
    "id": "user_onboarding_welcome",
    "step_type": "welcome",
    "order": 0,
    "title": "Welcome to Orkinosai, John! 🚀",
    "description": "Let's get you set up in just a few minutes.",
    "content": {
      "hero_text": "Welcome to the future of conversational AI",
      "subtitle": "We're excited to help you build amazing experiences",
      "features": [
        "AI-powered conversations",
        "Easy integration",
        "Scalable infrastructure"
      ]
    },
    "is_required": true,
    "cta_text": "Get Started"
  }
}
```

### Complete Step

```bash
POST /api/onboarding/progress/progress-123/complete-step
Content-Type: application/json

{
  "step_id": "user_onboarding_profile",
  "step_data": {
    "name": "John Doe",
    "role": "Developer",
    "company": "Acme Inc."
  }
}
```

Response:
```json
{
  "success": true,
  "message": "Step completed successfully",
  "next_step": {
    "id": "user_onboarding_organization",
    "title": "Create Workspace",
    ...
  }
}
```

### Get Progress

```bash
GET /api/onboarding/progress/progress-123
```

Response:
```json
{
  "success": true,
  "progress": {
    "id": "progress-123",
    "user_id": "user-123",
    "flow_id": "user_onboarding",
    "state": "in_progress",
    "current_step_index": 2,
    "completed_steps": ["step1", "step2"],
    "completion_percentage": 33.3,
    "started_at": "2025-12-11T18:30:00Z",
    "last_activity_at": "2025-12-11T18:35:00Z"
  }
}
```

## Customizing Onboarding Flows

### Adding a New Step

To add a new step to an existing flow:

1. Define the step type in `models.py`:
```python
class OnboardingStepType(str, Enum):
    # ... existing types
    MY_NEW_STEP = "my_new_step"
```

2. Add content for the step in `content_manager.py`:
```python
def _load_default_content(self):
    # ... existing content
    
    # Add new step content
    self._content_cache[OnboardingStepType.MY_NEW_STEP] = {
        'title': 'My New Step',
        'description': 'Description for the new step',
        'content': {
            # Your step-specific content
        },
        'cta_text': 'Continue',
        'skip_text': 'Skip'
    }
```

3. Add the step to the flow in `service.py`:
```python
def _create_user_onboarding_flow(self) -> OnboardingFlow:
    steps = [
        # ... existing steps
        OnboardingStep(
            id=f"{flow_id}_my_new_step",
            step_type=OnboardingStepType.MY_NEW_STEP,
            order=3,  # Set appropriate order
            title="My New Step",
            description="Step description",
            is_required=False
        )
    ]
```

### Creating a New Flow

To create a completely new onboarding flow:

1. Create a method in `service.py`:
```python
def _create_admin_onboarding_flow(self) -> OnboardingFlow:
    flow_id = "admin_onboarding"
    
    steps = [
        OnboardingStep(
            id=f"{flow_id}_welcome",
            step_type=OnboardingStepType.WELCOME,
            order=0,
            title="Welcome Admin",
            description="Admin-specific welcome",
            is_required=True
        ),
        # ... additional steps
    ]
    
    return OnboardingFlow(
        id=flow_id,
        name="admin_onboarding",
        title="Admin Onboarding",
        description="Onboarding flow for administrators",
        steps=steps,
        target_role="admin",
        is_active=True
    )
```

2. Initialize the flow in `_initialize_default_flows()`:
```python
def _initialize_default_flows(self):
    # ... existing flows
    admin_flow = self._create_admin_onboarding_flow()
    self._flows[admin_flow.id] = admin_flow
```

### Customizing Content

Content is managed through the `OnboardingContentManager`. To customize:

1. **Programmatically**:
```python
from src.cms.onboarding import OnboardingContentManager, OnboardingStepType

content_manager = OnboardingContentManager()
content_manager.update_content(
    step_type=OnboardingStepType.WELCOME,
    content={
        'title': 'Custom Welcome Title',
        'description': 'Custom description',
        'content': {
            'hero_text': 'Custom hero text',
            # ... more content
        }
    }
)
```

2. **Via Configuration**:
Pass custom content configuration when initializing the service:
```python
config = {
    'content': {
        'welcome': {
            'title': 'Custom Welcome',
            # ... more content
        }
    }
}
service = OnboardingService(config)
```

## Integration with User Registration

Integrate onboarding with your user registration flow:

```python
from src.cms.onboarding import OnboardingService

def register_user(email, password, name):
    # 1. Create user account
    user = create_user_account(email, password, name)
    
    # 2. Start onboarding
    onboarding_service = OnboardingService()
    progress = onboarding_service.start_onboarding(
        user_id=user.id,
        flow_type="user_onboarding",
        metadata={
            'source': 'registration',
            'email': email
        }
    )
    
    # 3. Return user and onboarding progress ID
    return {
        'user': user,
        'onboarding_progress_id': progress.id
    }
```

## Future Extensions

The onboarding system is designed to be extensible. Future enhancements could include:

1. **Database Persistence**: Currently uses in-memory storage; migrate to database
2. **Analytics Integration**: Track completion rates, drop-off points, funnel analysis
3. **A/B Testing**: Test different content variations to optimize conversion
4. **Email Integration**: Send reminder emails for incomplete onboarding
5. **Team Onboarding**: Support for team-based onboarding flows
6. **Custom Themes**: Allow organizations to customize onboarding appearance
7. **Video Tutorials**: Embed video content in onboarding steps
8. **Interactive Demos**: Provide hands-on product tours

## Best Practices

1. **Keep Steps Short**: Each step should take less than 2 minutes
2. **Make Optional Steps Skippable**: Don't force users through unnecessary steps
3. **Provide Clear Progress Indicators**: Show users where they are in the flow
4. **Collect Only Essential Data**: Don't ask for information you don't need
5. **Personalize Content**: Use user context to make content relevant
6. **Test Flows Regularly**: Ensure all steps work correctly after changes
7. **Monitor Drop-off Rates**: Identify and fix problematic steps
8. **Provide Help Resources**: Link to documentation and support

## Troubleshooting

### Onboarding Not Starting

Check that:
1. User ID is valid
2. Flow type exists (`user_onboarding`)
3. Service is properly initialized

### Step Content Not Loading

Check that:
1. Step type is defined in `OnboardingStepType` enum
2. Content is defined in `_load_default_content()`
3. Content manager is properly initialized

### Progress Not Saving

Currently uses in-memory storage. For production:
1. Implement database persistence
2. Add transaction management
3. Handle concurrent access

## Support

For questions or issues with the onboarding system:
- Check the code comments in `src/cms/onboarding/`
- Review this documentation
- Open an issue on GitHub
- Contact the development team

---

**Last Updated**: December 11, 2025
**Version**: 1.0.0
