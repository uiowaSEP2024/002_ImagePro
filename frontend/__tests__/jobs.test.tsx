import { act, render, screen, waitFor } from "@testing-library/react";
import Jobs from "@/pages/jobs";

import * as data from "@/data/index";

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";

jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: "",
      asPath: "",
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },
      beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    };
  }
}));

jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
  Promise.resolve({
    user: {
      first_name: "John",
      last_name: "Doe",
      email: "johndoe@gmail.com"
    },
    message: ""
  })
);
jest.spyOn(data, "fetchJobs").mockImplementation(() => Promise.resolve([]));
jest.spyOn(data, "fetchEvents").mockImplementation(() => Promise.resolve([]));
jest.spyOn(data, "fetchJobById").mockImplementation(() =>
  Promise.resolve({
    id: 1,
    provider_job_name: "Kidney Cancer Detection",
    customer_id: 1,
    provider_job_id: "236",
    provider_id: 2,
    created_at: "2021-03-01T00:00:00.000Z"
  })
);

describe("Jobs List Page", () => {
  it("renders a heading", async () => {
    await act(async () => render(<Jobs />, { wrapper: AuthContextProvider }));

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Jobs/i
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of jobs", async () => {
    await act(async () => render(<Jobs />, { wrapper: AuthContextProvider }));
    const table = await waitFor(() =>
      screen.getByRole("grid", {
        name: /Jobs/i
      })
    );

    expect(table).toBeInTheDocument();
  });
});
