// Configuration for different environments
const CONFIG = {
  development: {
    apiBaseUrl: 'http://127.0.0.1:5000'
  },
  staging: {
    apiBaseUrl: 'https://staging-api.yourdomain.com'
  },
  production: {
    apiBaseUrl: 'https://api.yourdomain.com'
  }
};

// Detect environment (default to development)
function getEnvironment() {
  // Check if we're in production by checking the hostname
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'development';
  } else if (hostname.includes('staging')) {
    return 'staging';
  } else {
    return 'production';
  }
}

// Get API URL based on environment
function getApiUrl(endpoint) {
  const env = getEnvironment();
  const baseUrl = CONFIG[env].apiBaseUrl;
  return `${baseUrl}${endpoint}`;
}
