# Project Context for AI Assistant

## Project Overview
- Repository: theoriq-hello-agent
- Purpose: Deployment of a Theoriq Protocol agent on DigitalOcean
- Current Status: Successfully deployed and documented
- GitHub Repository: https://github.com/iFirebrand/theoriq-hello-agent
- Deployment URL: https://hello-world-sdk-lla6e.ondigitalocean.app

## Technical Configuration
### Environment Variables
```
AGENT_PRIVATE_KEY=0x20df21e77a241e4d9381fa91c927715317a5088ce0c66d817d1881eaa1dede1a
THEORIQ_URI=https://theoriq-backend.dev-02.lab.chainml.net
FLASK_PORT=8000
```

### Deployment Platform
- Platform: DigitalOcean App Platform
- Deployment Method: Dockerfile
- Environment: Production
- Python Version: 3.9

## Development History

### Initial Setup Phase
1. Created GitHub repository
2. Set up basic project structure
3. Implemented initial Flask application
4. Added Theoriq SDK integration

### Deployment Challenges Addressed
1. DNS Resolution Issues
   - Initially tried direct IP (3.229.204.140)
   - Resolved by using proper hostname with HTTPS

2. CORS Configuration
   - Added support for both development and production domains
   - Configured for https://infinity.dev.theoriq.ai and https://infinity.theoriq.ai

3. Dependencies
   - Added Rust support for SDK requirements
   - Included git in Dockerfile for package installation
   - Configured Gunicorn for production deployment

### Current Implementation Details
1. Main Application Features:
   - Health check endpoint (/health)
   - Execute endpoint (/execute)
   - Comprehensive error handling
   - Detailed logging

2. Security Measures:
   - HTTPS enabled
   - Environment variables for sensitive data
   - CORS restrictions

## Current State
- Application is deployed and running
- Health endpoint is responding correctly
- Execute endpoint is properly configured
- CORS is set up for Theoriq domains
- Logging is implemented for debugging

## Recent Changes
1. Updated THEORIQ_URI to use HTTPS and proper hostname
2. Added comprehensive logging
3. Implemented proper error handling
4. Created detailed documentation

## Known Working State
- Health Check Response:
```json
{
    "status": "healthy",
    "theoriq_uri": "https://theoriq-backend.dev-02.lab.chainml.net"
}
```

## Repository Structure
```
theoriq-hello-agent/
├── .env
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── context-for-agent.md
```

## Next Steps or Pending Items
1. Monitor production performance
2. Consider implementing rate limiting
3. Set up automated testing
4. Implement additional error handling if needed

## Important URLs
- Development Backend: https://theoriq-backend.dev-02.lab.chainml.net
- Production Frontend: https://infinity.theoriq.ai
- Development Frontend: https://infinity.dev.theoriq.ai

## Notes for Future Development
1. Always maintain HTTPS for production
2. Keep the development and production URIs separate
3. Monitor DigitalOcean logs for issues
4. Test both health and execute endpoints after changes
5. Verify CORS settings when testing from Theoriq frontend

## Troubleshooting Context
Common issues that were resolved:
1. DNS resolution errors - Fixed by using proper hostname
2. 404 errors on public key - Resolved with correct THEORIQ_URI
3. CORS issues - Addressed with proper configuration
4. Build failures - Resolved with proper Dockerfile setup

## Testing Commands
```bash
# Health Check
curl https://hello-world-sdk-lla6e.ondigitalocean.app/health

# Execute Endpoint
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"dialog":{"items":[{"blocks":[{"type":"text","data":{"text":"test"}}]}]}}' \
  https://hello-world-sdk-lla6e.ondigitalocean.app/execute

# Backend Verification
curl -v https://theoriq-backend.dev-02.lab.chainml.net/api/v1alpha2/auth/biscuits/public-key
```

This context represents the current state of the project as of March 18, 2025.