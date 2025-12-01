# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

Most endpoints require authentication using JWT Bearer tokens.

### Get Access Token

**Endpoint:** `POST /api/v1/users/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Usage:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/users/
```

## Users API

### Register User

**Endpoint:** `POST /api/v1/users/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "onboarding_completed": false,
  "onboarding_step": 0,
  "account_id": null,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": null
}
```

### Login User

**Endpoint:** `POST /api/v1/users/login`

See Authentication section above.

### List Users

**Endpoint:** `GET /api/v1/users/`

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    ...
  }
]
```

### Get User

**Endpoint:** `GET /api/v1/users/{user_id}`

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  ...
}
```

### Update User

**Endpoint:** `PUT /api/v1/users/{user_id}`

**Request Body:**
```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response:** `200 OK`

### Delete User

**Endpoint:** `DELETE /api/v1/users/{user_id}`

**Response:** `204 No Content`

## Accounts API

### Create Account

**Endpoint:** `POST /api/v1/accounts/`

**Request Body:**
```json
{
  "name": "My Organization",
  "slug": "my-org",
  "subscription_tier": "free",
  "max_agents": 1,
  "max_users": 1
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "My Organization",
  "slug": "my-org",
  "subscription_tier": "free",
  "is_active": true,
  "max_agents": 1,
  "max_users": 1,
  "settings": {},
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": null
}
```

### List Accounts

**Endpoint:** `GET /api/v1/accounts/`

**Query Parameters:**
- `skip` (optional): Number of records to skip
- `limit` (optional): Maximum records to return

**Response:** `200 OK`

### Get Account

**Endpoint:** `GET /api/v1/accounts/{account_id}`

**Response:** `200 OK`

### Get Account by Slug

**Endpoint:** `GET /api/v1/accounts/slug/{slug}`

**Response:** `200 OK`

### Update Account

**Endpoint:** `PUT /api/v1/accounts/{account_id}`

**Request Body:**
```json
{
  "subscription_tier": "premium",
  "max_agents": 10
}
```

**Response:** `200 OK`

### Delete Account

**Endpoint:** `DELETE /api/v1/accounts/{account_id}`

**Response:** `204 No Content`

## Agents API

### Create Agent

**Endpoint:** `POST /api/v1/agents/?owner_id={owner_id}`

**Request Body:**
```json
{
  "name": "Customer Support Agent",
  "description": "Handles customer inquiries",
  "agent_type": "conversational",
  "is_public": false,
  "configuration": {
    "language": "en",
    "tone": "professional"
  }
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Customer Support Agent",
  "description": "Handles customer inquiries",
  "agent_type": "conversational",
  "is_active": true,
  "is_public": false,
  "training_status": "untrained",
  "knowledge_sources": [],
  "configuration": {
    "language": "en",
    "tone": "professional"
  },
  "azure_deployment_id": null,
  "azure_model_version": null,
  "owner_id": 1,
  "account_id": null,
  "created_at": "2024-12-01T10:00:00Z",
  "updated_at": null,
  "last_trained_at": null
}
```

### List Agents

**Endpoint:** `GET /api/v1/agents/`

**Query Parameters:**
- `skip` (optional): Pagination offset
- `limit` (optional): Results per page
- `owner_id` (optional): Filter by owner
- `account_id` (optional): Filter by account

**Response:** `200 OK`

### Get Agent

**Endpoint:** `GET /api/v1/agents/{agent_id}`

**Response:** `200 OK`

### Update Agent

**Endpoint:** `PUT /api/v1/agents/{agent_id}`

**Request Body:**
```json
{
  "name": "Updated Agent Name",
  "is_active": true
}
```

**Response:** `200 OK`

### Delete Agent

**Endpoint:** `DELETE /api/v1/agents/{agent_id}`

**Response:** `204 No Content`

### Activate Agent

**Endpoint:** `POST /api/v1/agents/{agent_id}/activate`

**Response:** `200 OK`

### Deactivate Agent

**Endpoint:** `POST /api/v1/agents/{agent_id}/deactivate`

**Response:** `200 OK`

## Onboarding API

### Get Onboarding Status

**Endpoint:** `GET /api/v1/onboarding/status/{user_id}`

**Response:** `200 OK`
```json
{
  "user_id": 1,
  "onboarding_completed": false,
  "current_step": 1,
  "total_steps": 3,
  "steps": [
    {
      "step": 1,
      "name": "Create Account",
      "completed": true
    },
    {
      "step": 2,
      "name": "Create First Agent",
      "completed": false
    },
    {
      "step": 3,
      "name": "Complete Profile",
      "completed": false
    }
  ]
}
```

### Complete Onboarding Step

**Endpoint:** `POST /api/v1/onboarding/step/{user_id}`

**Request Body:**
```json
{
  "step": 1,
  "data": {
    "additional": "info"
  }
}
```

**Response:** `200 OK`
```json
{
  "message": "Step 1 completed",
  "onboarding_completed": false,
  "current_step": 1
}
```

### Complete Full Onboarding

**Endpoint:** `POST /api/v1/onboarding/complete/{user_id}`

**Request Body:**
```json
{
  "account_name": "My Organization",
  "account_slug": "my-org",
  "agent_name": "First Agent",
  "agent_description": "My first conversational agent"
}
```

**Response:** `200 OK`
```json
{
  "message": "Onboarding completed successfully",
  "user_id": 1,
  "account_id": 1,
  "onboarding_completed": true
}
```

### Skip Onboarding

**Endpoint:** `POST /api/v1/onboarding/skip/{user_id}`

**Response:** `200 OK`

## Training API

### Train Agent

**Endpoint:** `POST /api/v1/training/{agent_id}/train`

**Request Body:**
```json
{
  "sources": [
    {
      "type": "url",
      "url": "https://example.com/docs"
    },
    {
      "type": "document",
      "filename": "guide.pdf"
    }
  ],
  "azure_model": "gpt-4",
  "configuration": {
    "max_tokens": 4096
  }
}
```

**Response:** `202 Accepted`
```json
{
  "message": "Training initiated",
  "agent_id": 1,
  "status": "training",
  "sources_count": 2
}
```

### Train from URL

**Endpoint:** `POST /api/v1/training/{agent_id}/train/url`

**Request Body:**
```json
{
  "url": "https://example.com/documentation",
  "metadata": {
    "category": "documentation"
  }
}
```

**Response:** `200 OK`
```json
{
  "message": "URL added to training queue",
  "agent_id": 1,
  "url": "https://example.com/documentation",
  "sources_count": 1
}
```

### Upload Training Document

**Endpoint:** `POST /api/v1/training/{agent_id}/train/document`

**Request:** Multipart form data with file

**Response:** `200 OK`
```json
{
  "filename": "guide.pdf",
  "size": 0,
  "content_type": "application/pdf",
  "storage_path": "agents/1/documents/guide.pdf"
}
```

### Get Training Status

**Endpoint:** `GET /api/v1/training/{agent_id}/training-status`

**Response:** `200 OK`
```json
{
  "agent_id": 1,
  "training_status": "training",
  "knowledge_sources_count": 3,
  "last_trained_at": "2024-12-01T10:00:00Z",
  "azure_deployment_id": null,
  "azure_model_version": "gpt-4"
}
```

### Remove Knowledge Source

**Endpoint:** `DELETE /api/v1/training/{agent_id}/sources/{source_index}`

**Response:** `200 OK`
```json
{
  "message": "Knowledge source removed",
  "removed_source": {
    "type": "url",
    "url": "https://example.com/docs"
  },
  "remaining_sources": 2
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Incorrect email or password"
}
```

### 403 Forbidden
```json
{
  "detail": "User account is inactive"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production use.

## Pagination

List endpoints support pagination with `skip` and `limit` parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 100)

Example:
```
GET /api/v1/users/?skip=20&limit=10
```

## Filtering

Some endpoints support filtering:
- Agents: `owner_id`, `account_id`

Example:
```
GET /api/v1/agents/?owner_id=1&account_id=1
```
