// Configuration for API endpoints
const isDevelopment = process.env.NODE_ENV === 'development';

// API base URL - use localhost for development, deployed URL for production
export const API_BASE_URL = isDevelopment 
  ? 'http://localhost:8000' 
  : 'https://personal-website-backend-4xh7uqxwwa-uc.a.run.app';

/**
 * Build a complete API URL by appending the endpoint to the base URL
 * @param endpoint - The API endpoint (e.g., '/api/search', '/api/contact')
 * @returns Complete API URL
 */
export function buildApiUrl(endpoint: string): string {
  return `${API_BASE_URL}${endpoint}`;
}

// Export the base URL for direct use if needed
export default API_BASE_URL;
