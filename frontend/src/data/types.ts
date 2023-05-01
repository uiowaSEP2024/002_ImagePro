export type User = {
  first_name: string;
  last_name: string;
  email: string;
  role: "customer" | "provider";
  id: number;
};

export type UserCreate = {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: "customer" | "provider";
};

export type JobConfiguration = {
    name: string;
    tag: string;
    version: string;
    step_configurations: Array<{
      name: string;
      tag: string;
      points: number;
      id: number;
      job_configuration_id: number;
      created_at: string;
      updated_at: string;
    }>;
    id: number;
    provider_id: number;
    created_at: string;
    updated_at: string;
};

export type Provider = {
  id: number;
  name: string;
};

export type Job = {
  id: number;
  provider_job_name: string;
  customer_id: number;
  provider_job_id: string;
  provider_id: number;
  created_at?: string;
  num_steps?: number;
};

export type Key = {
  id: number;
  user_id: number;
  key: string;
  note: string;
  created_at?: string;
};

export type JobEvent = {
  kind: string;
  name: string;
  job_id: number;
  id: number;
  created_at?: string;
  event_metadata?: Record<string, any>;
};
