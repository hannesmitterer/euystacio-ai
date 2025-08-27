# API Reference

## REST API Endpoints

### Core Endpoints

- `GET /api/red_code` - Get current Red Code state
- `GET /api/pulses` - Get recent emotional pulses
- `POST /api/pulse` - Submit new emotional pulse
- `GET /api/reflections` - Get AI reflections

### Documentation Endpoints

- `GET /docs/` - Documentation index
- `GET /docs/<slug>` - Get documentation page
- `GET /docs/api/<slug>` - Get documentation as JSON

### Authentication

For Hygraph integration, set these environment variables:
- `HYGRAPH_ENDPOINT` - Your Hygraph GraphQL endpoint
- `HYGRAPH_TOKEN` - Authentication token

## GraphQL Schema

The Hygraph integration expects a `Doc` content type with:
- `title` (String)
- `slug` (String, unique)
- `content` (RichText or String)