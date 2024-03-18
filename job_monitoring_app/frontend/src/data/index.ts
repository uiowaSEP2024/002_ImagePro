import { Study, StudyEvent, ApiKey, User, UserCreate } from "./types";


// The base URL for the backend API.
//TODO: change to the actual backend URL for docker deployment
export const backendUrl = (
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
).replace(/\/$/, "");


/**
 * Fetches all studies from the backend API.
 *
 * @returns {Promise<Study[] | void>} A promise that resolves to an array of studies or void.
 */
export const fetchStudies = async (): Promise<Study[] | void> => {
  return fetch(`${backendUrl}/studies`, {
    credentials: "include",
    method: "GET"
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as Study[];
      }
    })
    .catch((e) => {
      console.log(e);
    });
};

/**
 * Fetches a study by its ID from the backend API.
 *
 * @param {number} id - The ID of the study to fetch.
 * @returns {Promise<Study | void>} A promise that resolves to a study or void.
 */
export const fetchStudyById = async (id: number): Promise<Study | void> => {
  return await fetch(`${backendUrl}/studies/${id}`, {
    credentials: "include",
    method: "GET"
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as Study;
      }
    })
    .catch((e) => {
      console.log(e);
    });
};

/**
 * Generates API keys by making a POST request to the backend API.
 */
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

/**
 * Fetches all API keys from the backend API.
 *
 * @returns {Promise<ApiKey[] | void>} A promise that resolves to an array of API keys or void.
 */
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

/**
 * Generates API keys by making a POST request to the backend API.
 *
 * @param {object} data - The data to send in the request body.
 * @param {string} data.note - A note to associate with the API key.
 * @returns {Promise<any>} A promise that resolves to the response data.
 */
export const fetchGenAPIKeys = async (data: { note: string }): Promise<any> => {
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

/**
 * Fetches all events for a study from the backend API.
 *
 * @param {number} studyId - The ID of the study to fetch events for.
 * @returns {Promise<StudyEvent[] | void>} A promise that resolves to an array of study events or void.
 */
export const fetchEvents = async (
  studyId: number
): Promise<StudyEvent[] | void> => {
  return await fetch(`${backendUrl}/studies/${studyId}/events`, {
    credentials: "include",
    method: "GET"
  })
    .then(async (response) => {
      if (response.status == 200) {
        return (await response.json()) as StudyEvent[];
      }
    })
    .catch((e) => {
      console.log(e);
    });
};

/**
 * Checks if the user is logged in by making a GET request to the backend API.
 *
 * @returns {Promise<{ user?: User; message: string }>} A promise that resolves to an object containing the user and a message.
 */
export async function fetchCheckUserLoggedIn(): Promise<{ user?: User; message: string; }> {
  try {
    const result = await fetch(`${backendUrl}/login`, {
      credentials: "include",
      method: "GET"
    });

    return await result.json() as unknown as { user?: User; message: string };
  } catch (error) {
    console.log(error);
    throw error;
  }
}

/**
 * Logs out the user by making a POST request to the backend API.
 *
 * @returns {Promise<any>} A promise that resolves to the response data.
 */
export const fetchLogout = async (): Promise<any> => {
  const response = await fetch(`${backendUrl}/logout`, {
    method: "POST",
    credentials: "include"
  });

  return response.json();
};

/**
 * Logs in the user by making a POST request to the backend API.
 *
 * @param {string} email - The email of the user.
 * @param {string} password - The password of the user.
 * @returns {Promise<{ user: User }>} A promise that resolves to an object containing the user.
 * @throws {Error} If the response status is not 200.
 */
export const fetchLogin = async (email: string, password: string): Promise<{ user: User; }> => {
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

/**
 * Signs up a new user by making a POST request to the backend API.
 *
 * @param {UserCreate} data - The data to send in the request body.
 * @returns {Promise<any>} A promise that resolves to the response data.
 */
export const fetchSignUp = async (data: UserCreate): Promise<any> => {
  const response = await fetch(`${backendUrl}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return await response.json();
};

/**
 * Expires an API key by making a POST request to the backend API.
 *
 * @param {number} id - The ID of the API key to expire.
 * @returns {Promise<any>} A promise that resolves to the response data.
 */
export const fetchExpireApiKey = async (id: number): Promise<any> => {
  const response = await fetch(`${backendUrl}/api-keys/${id}/expire`, {
    credentials: "include",
    method: "POST"
  });

  return await response.json();
};

/**
 * Downloads a report by making a GET request to the backend API.
 *
 * @param {string} startDateStr - The start date for the report in YYYY-MM-DD format.
 * @param {string} endDateStr - The end date for the report in YYYY-MM-DD format.
 */
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

  const startTimestampSeconds = startDate.getTime() / 1000;
  const endTimestampSeconds = endDate.getTime() / 1000;

  console.log(startTimestampSeconds, endTimestampSeconds);

  const endpointUrl = `${backendUrl}/reporting?start_date=${startTimestampSeconds}&end_date=${endTimestampSeconds}`;

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

/**
 * Checks if the backend is up and running.
 *
 * @returns {Promise<boolean>} A promise that resolves to a boolean indicating whether the backend is up.
 */
export const isBackendUp = async (): Promise<void> => {
  try {
    const response = await fetch(backendUrl, {
      method: "GET"
    });

    // If the response status is 200, the backend is up
    console.log("*** Backend is up ***");
    console.log(response.status);
  } catch (error) {
    // If there's an error (like a network error), assume the backend is down
    console.log(error);
  }
};

isBackendUp();
