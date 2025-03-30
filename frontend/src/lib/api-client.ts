// API Client setup

// Direct imports from client source files since the client package isn't built
import { DefaultApi } from "humangpt-client";
import { Configuration } from "humangpt-client";

// Create a singleton instance of the API client
const config = new Configuration({
  basePath: 'https://api.humangpt.dev'  // Assuming backend runs on this URL
});

export const apiClient = new DefaultApi(config);
