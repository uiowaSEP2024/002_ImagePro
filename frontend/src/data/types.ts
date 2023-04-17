export type User = {
  first_name: string
  last_name: string
  email: string
}

export type UserCreate = {
  email: string
  password: string
  first_name: string
  last_name: string
}


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
  user_id: number,
  key: string,
  created_at?: string
};


export type JobEvent = {
  kind: string;
  name: string;
  job_id: number;
  id: number;
  created_at?: string;
};

