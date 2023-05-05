import { Job, JobEvent, ApiKey, User, UserCreate } from "./types";

export const backendUrl = (
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
).replace(/\/$/, "");

export const fetchJobs = async (): Promise<Job[] | void> => {
  return fetch(`${backendUrl}/jobs`, {
    credentials: "include",
    method: "GET"
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
    method: "GET"
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
    method: "POST"
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
    method: "GET"
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
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return await response.json();
};

export const fetchEvents = async (
  jobId: number
): Promise<JobEvent[] | void> => {
  return await fetch(`${backendUrl}/jobs/${jobId}/events`, {
    credentials: "include",
    method: "GET"
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
      method: "GET"
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
    credentials: "include"
  });

  return response.json();
};

export const fetchLogin = async (email: string, password: string) => {
  const response = await fetch(`${backendUrl}/login`, {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    },
    body: new URLSearchParams({
      username: email,
      password: password
    })
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
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return await response.json();
};

export const fetchDownloadReport = async (
  startDateStr: string,
  endDateStr: string
) => {
  console.log(startDateStr, endDateStr);
  const startDate = new Date(startDateStr);
  const endDate = new Date(endDateStr);

  startDate.setHours(new Date().getHours());
  startDate.setMinutes(new Date().getMinutes());
  startDate.setSeconds(new Date().getSeconds());
  startDate.setMilliseconds(new Date().getMilliseconds());

  endDate.setHours(new Date().getHours());
  endDate.setMinutes(new Date().getMinutes());
  endDate.setSeconds(new Date().getSeconds());
  endDate.setMilliseconds(new Date().getMilliseconds());

  const startTimestampSeconds = (startDate.getTime() / 1000).toFixed(6);
  const endTimestampSeconds = (endDate.getTime() / 1000).toFixed(6);

  console.log(startTimestampSeconds, endTimestampSeconds);

  const endpointUrl = `${backendUrl}/reporting?reporting?start_date=${startTimestampSeconds}&end_date=1683263397.421076`;

  console.log(endpointUrl);

  const response = await fetch(endpointUrl, {
    method: "GET",
    credentials: "include",
    headers: {
      "Content-Type": "text/csv"
    }
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `report-${startDateStr}-${endDateStr}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
};
