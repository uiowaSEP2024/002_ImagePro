/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
  "/": {
    /** Read Root */
    get: operations["read_root__get"];
  };
  "/users/": {
    /** Create User */
    post: operations["create_user_users__post"];
  };
  "/users/{user_id}": {
    /** Read User */
    get: operations["read_user_users__user_id__get"];
  };
  "/api-keys": {
    /** Read Apikeys */
    get: operations["read_apikeys_api_keys_get"];
    /** Generate Api Key */
    post: operations["generate_api_key_api_keys_post"];
  };
  "/api-keys/{apikey_id}/expire": {
    /** Expire Apikey */
    post: operations["expire_apikey_api_keys__apikey_id__expire_post"];
  };
  "/api-keys/protected": {
    /** Read Api Key Protected Route */
    get: operations["read_api_key_protected_route_api_keys_protected_get"];
  };
  "/login": {
    /** Login */
    get: operations["login_login_get"];
    /** Login */
    post: operations["login_login_post"];
  };
  "/logout": {
    /** Logout */
    post: operations["logout_logout_post"];
  };
  "/studies": {
    /** Get Customer Studies */
    get: operations["get_customer_studies_studies_get"];
    /** Create Study */
    post: operations["create_study_studies_post"];
  };
  "/studies/{study_id}": {
    /** Get Study */
    get: operations["get_study_studies__study_id__get"];
  };
  "/studies/{study_id}/events": {
    /** Get Study Events */
    get: operations["get_study_events_studies__study_id__events_get"];
  };
  "/events": {
    /** Create Event */
    post: operations["create_event_events_post"];
  };
  "/job_configurations": {
    /** Create Job */
    post: operations["create_job_job_configurations_post"];
  };
  "/job_configurations/{job_configuration_id}": {
    /** Get Job Configuration By Id */
    get: operations["get_job_configuration_by_id_job_configurations__job_configuration_id__get"];
  };
  "/job_configurations/": {
    /** Get Job Configurations By Tag And Version */
    get: operations["get_job_configurations_by_tag_and_version_job_configurations__get"];
  };
  "/reporting": {
    /** Get Reporting */
    get: operations["get_reporting_reporting_get"];
  };
}

export type webhooks = Record<string, never>;

export interface components {
  schemas: {
    /** Apikey */
    Apikey: {
      /** Note */
      note: string;
      /** Id */
      id: number;
      /** User Id */
      user_id: number;
      /** Key */
      key: string;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
      /**
       * Expires At
       * Format: date-time
       */
      expires_at?: string;
    };
    /** ApikeyCreate */
    ApikeyCreate: {
      /** Note */
      note: string;
    };
    /** ApikeyPublic */
    ApikeyPublic: {
      /** Note */
      note: string;
      /** Id */
      id: number;
      /** User Id */
      user_id: number;
      /**
       * Key
       * Format: password
       */
      key: string;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
      /**
       * Expires At
       * Format: date-time
       */
      expires_at?: string;
    };
    /** Body_login_login_post */
    Body_login_login_post: {
      /** Grant Type */
      grant_type?: string;
      /** Username */
      username: string;
      /** Password */
      password: string;
      /**
       * Scope
       * @default
       */
      scope?: string;
      /** Client Id */
      client_id?: string;
      /** Client Secret */
      client_secret?: string;
    };
    /** Event */
    Event: {
      /** Name */
      name?: string;
      kind: components["schemas"]["EventKindEnum"];
      /** Event Metadata */
      event_metadata?: {
        [key: string]: (string | number | boolean) | undefined;
      };
      /** Id */
      id: number;
      /** Study Id */
      study_id: number;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
      step_configuration?: components["schemas"]["StepConfiguration"];
    };
    /** EventCreatePublic */
    EventCreatePublic: {
      /** Name */
      name?: string;
      kind: components["schemas"]["EventKindEnum"];
      /** Event Metadata */
      event_metadata?: {
        [key: string]: (string | number | boolean) | undefined;
      };
      /** Provider Study Id */
      provider_study_id: string;
      /** Tag */
      tag?: string;
    };
    /**
     * EventKindEnum
     * @description An enumeration.
     * @enum {string}
     */
    EventKindEnum: "Pending" | "Error" | "Info" | "Complete" | "In progress";
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components["schemas"]["ValidationError"][];
    };
    /** Study */
    Study: {
      /** Provider Study Id */
      provider_study_id: string;
      /** Hospital Id */
      hospital_id: number;
      /** Id */
      id: number;
      /** Provider Id */
      provider_id: number;
      /** Job Configuration Id */
      job_configuration_id: number;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
      provider: components["schemas"]["User"];
      job_configuration: components["schemas"]["JobConfiguration"];
      /**
       * Events
       * @default []
       */
      events?: components["schemas"]["Event"][];
    };
    /** JobConfiguration */
    JobConfiguration: {
      /** Tag */
      tag: string;
      /** Name */
      name: string;
      /** Version */
      version: unknown;
      /** Step Configurations */
      step_configurations: components["schemas"]["StepConfiguration"][];
      /** Id */
      id: number;
      /** Provider Id */
      provider_id: number;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
    };
    /** JobConfigurationCreate */
    JobConfigurationCreate: {
      /** Tag */
      tag: string;
      /** Name */
      name: string;
      /** Version */
      version: unknown;
      /** Step Configurations */
      step_configurations: components["schemas"]["StepConfigurationCreate"][];
    };
    /** StudyCreate */
    StudyCreate: {
      /** Provider Study Id */
      provider_study_id: string;
      /** Hospital Id */
      hospital_id: number;
      /** Tag */
      tag: string;
    };
    /** MetadataConfiguration */
    MetadataConfiguration: {
      /** Name */
      name: string;
      /** @default text */
      kind?: components["schemas"]["MetadataKindEnum"];
      /** Units */
      units?: string;
      /** Id */
      id: number;
      /** Step Configuration Id */
      step_configuration_id: number;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
    };
    /** MetadataConfigurationCreate */
    MetadataConfigurationCreate: {
      /** Name */
      name: string;
      /** @default text */
      kind?: components["schemas"]["MetadataKindEnum"];
      /** Units */
      units?: string;
    };
    /**
     * MetadataKindEnum
     * @description An enumeration.
     * @enum {string}
     */
    MetadataKindEnum: "text" | "number" | "link";
    /** StepConfiguration */
    StepConfiguration: {
      /** Tag */
      tag: string;
      /** Name */
      name: string;
      /** Points */
      points: number;
      /** Id */
      id: number;
      /** Job Configuration Id */
      job_configuration_id: number;
      /** Metadata Configurations */
      metadata_configurations?: components["schemas"]["MetadataConfiguration"][];
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
    };
    /** StepConfigurationCreate */
    StepConfigurationCreate: {
      /** Tag */
      tag: string;
      /** Name */
      name: string;
      /** Points */
      points: number;
      /**
       * Metadata Configurations
       * @default []
       */
      metadata_configurations?: components["schemas"]["MetadataConfigurationCreate"][];
    };
    /** Token */
    Token: {
      /** Access Token */
      access_token: string;
      /** Token Type */
      token_type: string;
    };
    /** User */
    User: {
      /** Email */
      email: string;
      /** First Name */
      first_name: string;
      /** Last Name */
      last_name: string;
      /** @default customer */
      role?: components["schemas"]["UserRoleEnum"];
      /** Id */
      id: number;
      /**
       * Created At
       * Format: date-time
       */
      created_at?: string;
      /**
       * Updated At
       * Format: date-time
       */
      updated_at?: string;
    };
    /** UserCreate */
    UserCreate: {
      /** Email */
      email: string;
      /** First Name */
      first_name: string;
      /** Last Name */
      last_name: string;
      /** @default customer */
      role?: components["schemas"]["UserRoleEnum"];
      /** Password */
      password: string;
    };
    /**
     * UserRoleEnum
     * @description An enumeration.
     * @enum {string}
     */
    UserRoleEnum: "customer" | "provider";
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (string | number)[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type external = Record<string, never>;

export interface operations {
  /** Read Root */
  read_root__get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
    };
  };
  /** Create User */
  create_user_users__post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["UserCreate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Read User */
  read_user_users__user_id__get: {
    parameters: {
      path: {
        user_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["User"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Read Apikeys */
  read_apikeys_api_keys_get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["ApikeyPublic"][];
        };
      };
    };
  };
  /** Generate Api Key */
  generate_api_key_api_keys_post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["ApikeyCreate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Apikey"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Expire Apikey */
  expire_apikey_api_keys__apikey_id__expire_post: {
    parameters: {
      path: {
        apikey_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["ApikeyPublic"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Read Api Key Protected Route */
  read_api_key_protected_route_api_keys_protected_get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": string;
        };
      };
    };
  };
  /** Login */
  login_login_get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": Record<string, never>;
        };
      };
    };
  };
  /** Login */
  login_login_post: {
    requestBody: {
      content: {
        "application/x-www-form-urlencoded": components["schemas"]["Body_login_login_post"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Token"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Logout */
  logout_logout_post: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": string;
        };
      };
    };
  };
  /** Get Customer Studies */
  get_customer_studies_studies_get: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Study"][];
        };
      };
    };
  };
  /** Create Study */
  create_study_studies_post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["StudyCreate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Study"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Study */
  get_study_studies__study_id__get: {
    parameters: {
      path: {
        study_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Study"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Study Events */
  get_study_events_studies__study_id__events_get: {
    parameters: {
      path: {
        study_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Event"][];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Create Event */
  create_event_events_post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["EventCreatePublic"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Event"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Create Job */
  create_job_job_configurations_post: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["JobConfigurationCreate"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["JobConfiguration"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Job Configuration By Id */
  get_job_configuration_by_id_job_configurations__job_configuration_id__get: {
    parameters: {
      path: {
        job_configuration_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["JobConfiguration"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Job Configurations By Tag And Version */
  get_job_configurations_by_tag_and_version_job_configurations__get: {
    parameters: {
      query: {
        tag?: string;
        version?: string;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["JobConfiguration"][];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get Reporting */
  get_reporting_reporting_get: {
    parameters: {
      query: {
        start_date?: number;
        end_date?: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: never;
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
}
