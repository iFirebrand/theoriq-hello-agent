# Deploying a Theoriq Agent on DigitalOcean: A Complete Guide

## Context
The Theoriq Agent SDK allows developers to create AI agents that can be integrated with the Theoriq platform. This guide covers deploying a Python-based Theoriq agent using DigitalOcean's App Platform, which provides a simple yet robust hosting solution.

## Prerequisites
- GitHub account
- DigitalOcean account
- Basic understanding of Python and Flask
- Git installed locally
- A Theoriq Agent private key (provided by Theoriq)

## Project Setup

### 1. Repository Structure
Your repository should have the following essential files:
```
theoriq-hello-agent/
├── .env
├── main.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

### 2. Key Files Configuration

#### requirements.txt
```
python-dotenv==1.0.*
flask==3.1.*
flask-cors==4.0.*
gunicorn==21.2.*
git+https://github.com/chain-ml/theoriq-agent-sdk.git#egg=theoriq[flask]
```

#### .env
```
AGENT_PRIVATE_KEY=your_private_key_here
THEORIQ_URI=https://theoriq-backend.dev-02.lab.chainml.net
FLASK_PORT=8000
```

#### Dockerfile
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=main.py
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "main:create_app()"]
```

#### .dockerignore
```
.env
__pycache__
*.pyc
.git
.gitignore
```

## Deployment on DigitalOcean

### 1. Create App on DigitalOcean App Platform
1. Log in to DigitalOcean
2. Go to App Platform
3. Click "Create App"
4. Choose GitHub as the source
5. Select your repository
6. Choose the main branch
7. Select "Dockerfile" as the deployment method

### 2. Configure Environment Variables
In the App Platform settings, add these environment variables:
```
AGENT_PRIVATE_KEY=your_private_key_here
THEORIQ_URI=https://theoriq-backend.dev-02.lab.chainml.net
FLASK_PORT=8000
```

### 3. Deploy
Click "Deploy" and wait for the build to complete.

## Troubleshooting Guide

### 1. Verify Deployment Health
Check if your agent is running:
```bash
curl https://your-app-name.ondigitalocean.app/health
```
Expected response:
```json
{
    "status": "healthy",
    "theoriq_uri": "https://theoriq-backend.dev-02.lab.chainml.net"
}
```

### 2. Test Execute Endpoint
Send a test request:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"dialog":{"items":[{"blocks":[{"type":"text","data":{"text":"test"}}]}]}}' \
  https://your-app-name.ondigitalocean.app/execute
```

### 3. Common Issues and Solutions

#### DNS Resolution Issues
If you see "Name or service not known" errors:
1. Verify the THEORIQ_URI is correct
2. Test DNS resolution:
```bash
dig +short theoriq-backend.dev-02.lab.chainml.net
```

#### 502 Bad Gateway
1. Check DigitalOcean logs in App Platform
2. Verify environment variables are set correctly
3. Test the health endpoint
4. Ensure CORS settings are correct if calling from a browser

#### 404 Not Found on Public Key
Test the public key endpoint:
```bash
curl -v https://theoriq-backend.dev-02.lab.chainml.net/api/v1alpha2/auth/biscuits/public-key
```

## Registering with Theoriq Infinity Hub

1. Deploy your agent and ensure it's running correctly
2. Go to [Theoriq Infinity Hub](https://infinity.dev.theoriq.ai)
3. Click "Register New Agent"
4. Fill in the agent details:
   - Name: Your agent's name
   - Description: What your agent does
   - URL: Your DigitalOcean app URL (e.g., https://your-app-name.ondigitalocean.app)
   - Agent Type: Select appropriate type
5. Test the connection using the provided test interface
6. Submit for registration

## Monitoring and Maintenance

### View Logs
In DigitalOcean App Platform:
1. Go to your app
2. Click "Components"
3. Select your service
4. Click "Logs"

### Update Agent
1. Push changes to your GitHub repository
2. DigitalOcean will automatically rebuild and deploy

### Monitor Performance
Use DigitalOcean's metrics to monitor:
- CPU usage
- Memory usage
- Request count
- Response times

## Best Practices
1. Always use HTTPS for production
2. Keep dependencies updated
3. Use environment variables for sensitive data
4. Implement proper error handling
5. Add detailed logging
6. Use CORS appropriately
7. Implement rate limiting for production use

## Support
If you encounter issues:
1. Check DigitalOcean App Platform logs
2. Verify environment variables
3. Test endpoints using curl commands
4. Contact Theoriq support if the issue persists

Remember to never share your private keys or sensitive environment variables. Always use secure methods to manage and transfer credentials.