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
  num_steps?: number;
};

export type Key = {
  id: number;
  user_id: number,
  key: string,
  created_at?: string
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
  return fetch("http://localhost:8000/jobs", {
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
};

// TODO: Replace with actual API call
export const fetchJobById = async (id: number): Promise<Job | void> => {
  return await fetch(`http://localhost:8000/jobs/${id}`, {
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
};

export const generateAPIKeys = async () => {
  await fetch("http://localhost:8000/api-keys", {
    credentials: "include",
    method: "POST"
  }).then((response) => response.json())
    .then((data) => {
      console.log(data)
      return data
    }).catch((e) => {
      console.log(e)
    })
}

export const fetchAPIkeys = async (): Promise<Key[] | void> => {
  return await fetch("http://localhost:8000/api-keys", {
    credentials: "include",
    method: "GET"
  }).
    then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as Key[];
      }
    })
    .catch((e) => {
      console.log(e)
    });
}


export const fetchEvents = async (
  jobId: number
): Promise<JobEvent[] | void> => {
  return await fetch(`http://localhost:8000/jobs/${jobId}/events`, {
    credentials: "include",
    method: "GET",
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as JobEvent[];
      }
    })
    .catch((e) => {
      console.log(e);
    });
};


export type User = {
  first_name: string
  last_name: string
  email: string
}

export async function fetchCheckUserLoggedIn() {
  try {
    const result = await 
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }) 
      
    return result.json() as unknown as {user: User, message: string} 
  } catch (error) {
    console.log(error)
    throw error
  }
}


export const fetchLogout = async () => {
  const response = await fetch("http://localhost:8000/logout", {
    method: "POST",
    credentials: "include",
  })

  return response.json()
};


export const fetchLogin = async (email: string, password: string) => {
  const response = await fetch("http://localhost:8000/login", {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    },
    body: new URLSearchParams({
      username: email,
      password: password,
    }),
  })

  return await response.json() as {user: User}
}



type UserCreate = {
  email: string
  password: string
  first_name: string
  last_name: string
}
export const fetchSignUp = async (data: UserCreate) => {
  const response = await fetch("http://localhost:8000/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: data.email,
      password: data.password,
      first_name: data.first_name,
      last_name: data.last_name,
    }),
  })

  return await response.json()
}