/**
 * Environment variable validation and configuration
 */

interface EnvValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Validates that required environment variables are present
 */
function validateRequiredEnvVars(requiredVars: string[]): string[] {
  const missing: string[] = [];
  requiredVars.forEach((varName) => {
    if (!process.env[varName]) {
      missing.push(varName);
    }
  });
  return missing;
}

/**
 * Validates that optional environment variables have valid values if present
 */
function validateOptionalEnvVars(
  optionalVars: { name: string; validator?: (value: string) => boolean }[],
): string[] {
  const warnings: string[] = [];
  optionalVars.forEach(({ name, validator }) => {
    const value = process.env[name];
    if (value && validator && !validator(value)) {
      warnings.push(`${name} has invalid value: "${value}"`);
    }
  });
  return warnings;
}

/**
 * Validates all environment variables used by the application
 */
function validateEnvironment(): EnvValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Currently no required environment variables
  // Firebase variables are set in CI but not yet used in code
  const requiredVars: string[] = [];

  // Optional environment variables with validation
  const optionalVars = [
    {
      name: "VUE_APP_FLAG_MARATHON",
      validator: (value: string) => value === "true" || value === "false",
    },
  ];

  // Validate required variables
  const missingRequired = validateRequiredEnvVars(requiredVars);
  if (missingRequired.length > 0) {
    errors.push(
      `Missing required environment variables: ${missingRequired.join(", ")}`,
    );
  }

  // Validate optional variables
  const invalidOptional = validateOptionalEnvVars(optionalVars);
  warnings.push(...invalidOptional);

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
  };
}

/**
 * Gets a boolean environment variable with a default value
 */
function getBooleanEnv(name: string, defaultValue: boolean): boolean {
  const value = process.env[name];
  if (value === undefined || value === "") {
    return defaultValue;
  }
  return value === "true";
}

// Validate environment on module load
const validation = validateEnvironment();

// Log warnings in development
if (process.env.NODE_ENV !== "production" && validation.warnings.length > 0) {
  console.warn("Environment variable warnings:");
  validation.warnings.forEach((warning) => console.warn(`  - ${warning}`));
}

// Throw errors for missing required variables
if (!validation.isValid) {
  throw new Error(
    `Environment configuration error:\n${validation.errors.join("\n")}`,
  );
}

// Export validated configuration
export default {
  flagMarathons: getBooleanEnv("VUE_APP_FLAG_MARATHON", false),
};
