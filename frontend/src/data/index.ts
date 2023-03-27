export type Provider = {
  id: number;
  name: string;
};
export const providers: Record<string, Provider> = {
  "2": {
    id: 2,
    name: "BotImage",
  },
};

export type Job = {
  id: number;
  provider_job_name: string;
  customer_id: number;
  provider_job_id: string;
  provider_id: number;
  created_at: string;
};

export const jobs: Record<string, Job> = {
  "1": {
    id: 1,
    provider_job_name: "Kidney Cancer Detection",
    customer_id: 1,
    provider_job_id: "236",
    provider_id: 2,
    created_at: "2021-03-01T00:00:00.000Z",
  },

  "2": {
    id: 2,
    provider_job_name: "Lung Cancer Detection",
    customer_id: 1,
    provider_job_id: "237",
    provider_id: 2,
    created_at: "2021-03-01T00:00:00.000Z",
  },

  "3": {
    id: 3,
    provider_job_name: "Prostate Cancer Detection",
    customer_id: 1,
    provider_job_id: "238",
    provider_id: 2,
    created_at: "2021-03-01T00:00:00.000Z",
  },
};

export const events = [
  {
    id: 1,
    name: "Lung scan created",
    created_at: "2023-03-22T00:00:00.000Z",
  },
  {
    id: 2,
    name: "Lung scan started",
    created_at: "2023-03-23T00:00:00.000Z",
  },
  {
    id: 3,
    name: "Lung scan completed",
    created_at: "2023-03-24T00:00:00.000Z",
  },
];

export type JobEvent = typeof events[number];

export const fetchJobs = async (): Promise<Job[]> => {
  return Object.values(jobs);
};

// TODO: Replace with actual API call
export const fetchJobById = async (id: string): Promise<Job> => {
  return jobs[id];
};

export const fetchEvents = async (jobId: string): Promise<JobEvent[]> => {
  return events.map((event) => ({ ...event, job_id: jobId }));
};
