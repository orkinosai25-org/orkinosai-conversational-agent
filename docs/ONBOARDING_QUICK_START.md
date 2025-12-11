# Onboarding System Quick Start

This guide provides a quick walkthrough of using the onboarding system.

## For Developers

### Starting Onboarding for a New User

```python
from src.cms.onboarding import OnboardingService

# Initialize the service
service = OnboardingService()

# Start onboarding when user registers
progress = service.start_onboarding(
    user_id="new-user-123",
    flow_type="user_onboarding"
)

print(f"Onboarding started with ID: {progress.id}")
```

### Getting and Displaying the Current Step

```python
# Get current step with personalized content
step = service.get_current_step(
    progress_id=progress.id,
    user_context={'name': 'John', 'role': 'Developer'}
)

# Display to user
print(f"Step {step.order + 1}: {step.title}")
print(f"Description: {step.description}")
print(f"Content: {step.content}")
```

### Completing a Step

```python
# User fills out the form and submits
user_data = {
    'name': 'John Doe',
    'role': 'Developer',
    'company': 'Acme Inc.'
}

# Complete the step
success = service.complete_step(
    progress_id=progress.id,
    step_id=step.id,
    step_data=user_data
)

if success:
    print("Step completed! Moving to next step...")
```

## API Usage

### Start Onboarding via API

```bash
curl -X POST http://localhost:5000/api/onboarding/start \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "flow_type": "user_onboarding",
    "metadata": {"source": "web"}
  }'
```

### Get Current Step

```bash
curl http://localhost:5000/api/onboarding/progress/{progress_id}/current-step?user_name=John
```

### Complete Step

```bash
curl -X POST http://localhost:5000/api/onboarding/progress/{progress_id}/complete-step \
  -H "Content-Type: application/json" \
  -d '{
    "step_id": "user_onboarding_profile",
    "step_data": {
      "name": "John Doe",
      "role": "Developer"
    }
  }'
```

## Frontend Integration Example

```javascript
// Start onboarding
async function startOnboarding(userId) {
  const response = await fetch('/api/onboarding/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      flow_type: 'user_onboarding'
    })
  });
  
  const data = await response.json();
  return data.progress.id;
}

// Get current step
async function getCurrentStep(progressId, userName) {
  const response = await fetch(
    `/api/onboarding/progress/${progressId}/current-step?user_name=${userName}`
  );
  
  const data = await response.json();
  return data.step;
}

// Complete step
async function completeStep(progressId, stepId, stepData) {
  const response = await fetch(
    `/api/onboarding/progress/${progressId}/complete-step`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        step_id: stepId,
        step_data: stepData
      })
    }
  );
  
  const data = await response.json();
  return data.next_step;
}

// Example usage
async function runOnboarding() {
  // Start onboarding
  const progressId = await startOnboarding('user-123');
  
  // Get first step
  let step = await getCurrentStep(progressId, 'John');
  console.log('Current step:', step.title);
  
  // Complete step
  const nextStep = await completeStep(progressId, step.id, {
    name: 'John Doe',
    role: 'Developer'
  });
  
  if (nextStep) {
    console.log('Next step:', nextStep.title);
  } else {
    console.log('Onboarding complete!');
  }
}
```

## Testing

### Run Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Run onboarding tests only
python -m pytest tests/ -k onboarding
```

### Manual Testing with Flask

```bash
# Start the server
python main.py

# In another terminal, test the API
curl http://localhost:5000/api/onboarding/flows

# Should return list of available flows
```

## Common Issues

### Issue: "Flow not found"
**Solution**: Make sure you're using a valid flow type like `"user_onboarding"`

### Issue: "Progress not found"
**Solution**: Check that you're using the correct progress ID returned from `/start`

### Issue: "Cannot skip required step"
**Solution**: Only optional steps (with `is_required=False`) can be skipped

## Next Steps

- Read the full documentation: `docs/ONBOARDING_INTEGRATION.md`
- Customize step content in `src/cms/onboarding/content_manager.py`
- Add new steps by extending the flow in `src/cms/onboarding/service.py`
- Integrate with your UI framework

---

For detailed documentation, see [ONBOARDING_INTEGRATION.md](ONBOARDING_INTEGRATION.md)
