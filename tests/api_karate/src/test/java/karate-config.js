function fn() {
  // 1. Access Java System to read Environment Variables
  var System = Java.type('java.lang.System');

  var config = {
    baseUrl: System.getenv('BASE_URL'),

    // 2. Fetch from Env (from .env file), fallback to defaults if missing
    managerUsername: System.getenv('MANAGER_USERNAME'),
    managerPassword: System.getenv('MANAGER_PASSWORD')
  };

  // 3. Pass the config (which now has credentials) to auth.feature
  var result = karate.callSingle('classpath:examples/auth.feature', config);

  config.authHeader = { Authorization: 'Bearer ' + result.accessToken };

  return config;
}