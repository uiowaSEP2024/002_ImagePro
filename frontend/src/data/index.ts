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
  created_at?: string;
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

export const events: JobEvent[] = [
  {
    id: 1,
    job_id: 5,
    kind: "Step",
    name: "Lung scan created",
    created_at: "2023-03-22T00:00:00.000Z",
  },
  {
    id: 2,
    job_id: 5,
    kind: "Step",
    name: "Lung scan started",
    created_at: "2023-03-23T00:00:00.000Z",
  },
  {
    id: 3,
    job_id: 5,
    kind: "Step",
    name: "Lung scan completed",
    created_at: "2023-03-24T00:00:00.000Z",
  },
];

export type JobEvent = {
  kind: string;
  name: string;
  job_id: number;
  id: number;
  created_at?: string;
};

export const fetchJobs = async (): Promise<Job[] | void> => {
  fetch("http://localhost:8000/jobs", {
    credentials: "include",
    method: "GET",
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as Job[];
      }
    })
    .catch((e) => {
      console.log(e);
    });
  //return Object.values(jobs);
};

// TODO: Replace with actual API call
export const fetchJobById = async (id: number): Promise<Job | void> => {
  fetch(`http://localhost:8000/jobs/${id}`, {
    credentials: "include",
    method: "GET",
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as Job;
      }
    })
    .catch((e) => {
      console.log(e);
    });
  //return jobs[id];
};

export const fetchEvents = async (jobId: number): Promise<JobEvent[]> => {
  return events.map((event) => ({ ...event, job_id: jobId }));
};
