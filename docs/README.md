# Nexus API Documentation

## Overview

Welcome to the Nexus API documentation. Nexus is a comprehensive platform for telemetry collection, command execution, task management, AI agent coordination, and real-time event streaming.

### Key Features

- 🔄 **Telemetry Collection**: Real-time metrics and event ingestion
- ⚡ **Command Execution**: Distributed command orchestration
- 📋 **Task Management**: Comprehensive task tracking and workflow automation
- 🤖 **AI Coordination**: Multi-agent collaboration and AI-assisted workflows
- 🔒 **Security**: Role-based access control, OAuth 2.0, and audit logging
- 📡 **Event Streaming**: WebSocket-based real-time updates
- 🔔 **Webhooks**: Event-driven integrations

## Quick Start

### Prerequisites

- Node.js 18+ or Python 3.9+
- API key (obtain from [Nexus Dashboard](https://nexus.example.com/dashboard))

### Installation

#### Node.js
```bash
npm install @nexus/client
```

#### Python
```bash
pip install nexus-client
```

### Basic Usage

#### Submit Telemetry (Node.js)

```javascript
const { NexusClient } = require('@nexus/client');

const client = new NexusClient({
  apiKey: process.env.NEXUS_API_KEY,
  baseUrl: 'https://api.nexus.example.com'
});

// Submit a telemetry event
await client.telemetry.submit({
  event_type: 'system.metric',
  source: 'my-app',
  data: {
    metric_name: 'api_response_time',
    value: 125,
    unit: 'ms'
  }
});
```

#### Submit Telemetry (Python)

```python
from nexus_client import NexusClient
import os

client = NexusClient(
    api_key=os.getenv('NEXUS_API_KEY'),
    base_url='https://api.nexus.example.com'
)

# Submit a telemetry event
client.telemetry.submit({
    'event_type': 'system.metric',
    'source': 'my-app',
    'data': {
        'metric_name': 'api_response_time',
        'value': 125,
        'unit': 'ms'
    }
})
```

#### Execute Command

```javascript
// Execute a command on a target system
const command = await client.commands.execute({
  command_type: 'deploy.app',
  target: 'production-server-01',
  parameters: {
    version: 'v1.2.3',
    rollback_on_failure: true
  }
});

console.log(`Command ID: ${command.command_id}`);

// Poll for command status
const status = await client.commands.getStatus(command.command_id);
console.log(`Status: ${status.status}`);
```

#### Create Task

```javascript
// Create a new task
const task = await client.tasks.create({
  title: 'Deploy feature XYZ',
  description: 'Deploy the new authentication feature',
  type: 'deployment',
  priority: 'high',
  assignee: 'ai_agent_001'
});

// Update task progress
await client.tasks.update(task.task_id, {
  status: 'in_progress',
  progress: 50
});
```

#### Request AI Assistance

```javascript
// Request code review from AI agent
const request = await client.ai.requestAssistance({
  request_type: 'code_review',
  target_agent: 'code_reviewer_v1',
  context: {
    repository: 'github.com/myorg/myrepo',
    pull_request: 42
  },
  parameters: {
    check_security: true,
    check_style: true
  }
});

// Get results
const result = await client.ai.getResult(request.request_id);
console.log('Review findings:', result.findings);
```

### WebSocket Streaming

```javascript
const { NexusWebSocket } = require('@nexus/client');

const ws = new NexusWebSocket({
  apiKey: process.env.NEXUS_API_KEY,
  url: 'wss://api.nexus.example.com/stream'
});

// Subscribe to events
ws.subscribe(['telemetry.metrics', 'tasks.updates']);

// Handle incoming events
ws.on('event', (event) => {
  console.log('Received event:', event);
});

ws.connect();
```

See [WEBSOCKET_EXAMPLE.md](./WEBSOCKET_EXAMPLE.md) for detailed WebSocket implementation.

## Configuration

### Environment Variables

```bash
# Required
NEXUS_API_KEY=your_api_key_here
NEXUS_BASE_URL=https://api.nexus.example.com

# Optional
NEXUS_TIMEOUT=30000
NEXUS_RETRY_ATTEMPTS=3
NEXUS_LOG_LEVEL=info
```

### Advanced Configuration

```javascript
const client = new NexusClient({
  apiKey: process.env.NEXUS_API_KEY,
  baseUrl: process.env.NEXUS_BASE_URL,
  timeout: 30000,
  retryAttempts: 3,
  retryDelay: 1000,
  logLevel: 'debug'
});
```

## Documentation Structure

- [**NEXUS_API_SPEC.md**](../NEXUS_API_SPEC.md) - Complete API specification
- [**DEPLOY_INSTRUCTIONS.md**](./DEPLOY_INSTRUCTIONS.md) - Deployment guides for Render and Netlify
- [**GMAIL_OAUTH_SETUP.md**](./GMAIL_OAUTH_SETUP.md) - Gmail OAuth 2.0 integration
- [**WEBSOCKET_EXAMPLE.md**](./WEBSOCKET_EXAMPLE.md) - WebSocket implementation examples
- [**GGI_BROADCAST_INTEGRATION.md**](./GGI_BROADCAST_INTEGRATION.md) - GGI Broadcast integration
- [**SECURITY_RUNBOOK.md**](./SECURITY_RUNBOOK.md) - Security best practices and runbooks
- [**openapi.yaml**](./openapi.yaml) - OpenAPI 3.1 specification
- [**nexus.proto**](./nexus.proto) - Protocol Buffer definitions

## Authentication

Nexus supports multiple authentication methods:

1. **API Keys** - For service-to-service communication
2. **OAuth 2.0** - For user-delegated access
3. **JWT Tokens** - For session-based authentication

```javascript
// API Key authentication (recommended)
const client = new NexusClient({
  apiKey: 'nexus_api_xxxxxxxxxx'
});

// OAuth 2.0 (for user-delegated access)
const client = new NexusClient({
  oauth: {
    clientId: process.env.OAUTH_CLIENT_ID,
    clientSecret: process.env.OAUTH_CLIENT_SECRET,
    redirectUri: 'https://myapp.com/oauth/callback'
  }
});
```

See [GMAIL_OAUTH_SETUP.md](./GMAIL_OAUTH_SETUP.md) for OAuth configuration.

## Rate Limits

Default rate limits:
- Telemetry (single): 1,000 requests/minute
- Telemetry (batch): 100 requests/minute
- Commands: 100 requests/minute
- Tasks: 500 requests/minute
- AI Requests: 50 requests/minute

Rate limit headers are included in every response:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1699000000
```

## Error Handling

```javascript
try {
  await client.telemetry.submit(event);
} catch (error) {
  if (error.code === 'RATE_LIMIT_EXCEEDED') {
    const retryAfter = error.retryAfter;
    console.log(`Rate limited. Retry after ${retryAfter} seconds`);
  } else if (error.code === 'AUTHENTICATION_FAILED') {
    console.error('Invalid API key');
  } else {
    console.error('Error:', error.message);
  }
}
```

## Examples

### Complete Deployment Workflow

```javascript
async function deployFeature() {
  // 1. Create deployment task
  const task = await client.tasks.create({
    title: 'Deploy Feature XYZ',
    type: 'deployment',
    priority: 'high'
  });

  // 2. Request AI code review
  const review = await client.ai.requestAssistance({
    request_type: 'code_review',
    context: { pull_request: 42 }
  });

  const reviewResult = await client.ai.getResult(review.request_id);
  
  if (reviewResult.summary.critical > 0) {
    await client.tasks.update(task.task_id, {
      status: 'blocked',
      notes: 'Critical issues found in code review'
    });
    return;
  }

  // 3. Execute deployment command
  const command = await client.commands.execute({
    command_type: 'deploy.app',
    target: 'production',
    parameters: { version: 'v1.2.3' }
  });

  // 4. Wait for completion
  const result = await client.commands.waitForCompletion(command.command_id);

  // 5. Update task status
  await client.tasks.update(task.task_id, {
    status: result.success ? 'completed' : 'failed'
  });

  // 6. Submit telemetry
  await client.telemetry.submit({
    event_type: 'deployment.complete',
    data: {
      task_id: task.task_id,
      success: result.success,
      duration_ms: result.duration
    }
  });
}
```

## Support

- **Documentation**: https://docs.nexus.example.com
- **API Status**: https://status.nexus.example.com
- **GitHub Issues**: https://github.com/nexus/api/issues
- **Discord Community**: https://discord.gg/nexus
- **Email Support**: support@nexus.example.com

## License

See [LICENSE](../LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct before submitting pull requests.

---

**Getting Started**: Follow the [Quick Start](#quick-start) guide above to begin integrating Nexus into your application.

**Need Help?**: Check our [comprehensive API specification](../NEXUS_API_SPEC.md) or reach out to our support team.
