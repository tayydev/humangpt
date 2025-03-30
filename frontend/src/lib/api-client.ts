// API Client setup

// Direct imports from client source files since the client package isn't built
import { DefaultApi } from "humangpt-client";
import { Configuration } from "humangpt-client";

// Default API base path with environment variable override
const API_BASE_PATH = import.meta.env.VITE_API_BASE_PATH || 'https://api.humangpt.dev';

// Create a singleton instance of the API client
const config = new Configuration({
  basePath: API_BASE_PATH
});

export const apiClient = new DefaultApi(config);
