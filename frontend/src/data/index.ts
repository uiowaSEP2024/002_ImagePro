import { Job, JobEvent, ApiKey, User, UserCreate } from "./types";

export const backendUrl = (
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
).replace(/\/$/, "");

export const fetchJobs = async (): Promise<Job[] | void> => {
  return fetch(`${backendUrl}/jobs`, {
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
  return await fetch(`${backendUrl}/jobs/${id}`, {
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
  await fetch(`${backendUrl}/api-keys`, {
    credentials: "include",
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      return data;
    })
    .catch((e) => {
      console.log(e);
    });
};

export const fetchAPIkeys = async (): Promise<ApiKey[] | void> => {
  return await fetch(`${backendUrl}/api-keys`, {
    credentials: "include",
    method: "GET",
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as ApiKey[];
      }
    })
    .catch((e) => {
      console.log(e);
    });
};

export const fetchGenAPIKeys = async (data: { note: string }) => {
  const response = await fetch(`${backendUrl}/api-keys`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return await response.json();
};

export const fetchEvents = async (
  jobId: number
): Promise<JobEvent[] | void> => {
  return await fetch(`${backendUrl}/jobs/${jobId}/events`, {
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

export async function fetchCheckUserLoggedIn() {
  try {
    const result = await fetch(`${backendUrl}/login`, {
      credentials: "include",
      method: "GET",
    });

    return result.json() as unknown as { user?: User; message: string };
  } catch (error) {
    console.log(error);
    throw error;
  }
}

export const fetchLogout = async () => {
  const response = await fetch(`${backendUrl}/logout`, {
    method: "POST",
    credentials: "include",
  });

  return response.json();
};

export const fetchLogin = async (email: string, password: string) => {
  const response = await fetch(`${backendUrl}/login`, {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    },
    body: new URLSearchParams({
      username: email,
      password: password,
    }),
  });

  // TODO: check for wider range of error codes
  if (response.status !== 200) {
    throw new Error(await response.text());
  }

  return (await response.json()) as { user: User };
};

export const fetchSignUp = async (data: UserCreate) => {
  const response = await fetch(`${backendUrl}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return await response.json();
};
