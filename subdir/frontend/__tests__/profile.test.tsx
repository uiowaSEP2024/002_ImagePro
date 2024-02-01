import { act, render, screen, waitFor } from "@testing-library/react";
import Profile from "@/pages/profile";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

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
      email: "johndoe@gmail.com",
      id: 1,
      role: "customer"
    },
    message: ""
  })
);

jest.spyOn(data, "fetchJobs").mockImplementation(() =>
  Promise.resolve([
    {
      id: 1,
      provider_job_name: "Kidney Cancer Detection",
      customer_id: 1,
      provider_job_id: "236",
      provider_id: 2,
      created_at: "2021-03-01T00:00:00.000Z",
      job_configuration_id: 1,
      job_configuration: {
        id: 1,
        name: "Kidney Cancer Detection",
        tag: "kidney_cancer_detection",
        step_configurations: [],
        version: "1.0.0",
        provider_id: 1
      },
      provider: {
        id: 1,
        first_name: "BotImage",
        last_name: "",
        email: "botimage@gmail.com"
      }
    }
  ])
);
jest.spyOn(data, "fetchEvents").mockImplementation(() => Promise.resolve([]));
jest.spyOn(data, "fetchJobById").mockImplementation(() =>
  Promise.resolve({
    id: 1,
    provider_job_name: "Kidney Cancer Detection",
    customer_id: 1,
    provider_job_id: "236",
    provider_id: 2,
    created_at: "2021-03-01T00:00:00.000Z",
    job_configuration_id: 1,
    job_configuration: {
      id: 1,
      name: "Kidney Cancer Detection",
      tag: "kidney_cancer_detection",
      step_configurations: [],
      version: "1.0.0",
      provider_id: 1
    },
    provider: {
      id: 1,
      first_name: "BotImage",
      last_name: "",
      email: "botimage@gmail.com"
    }
  })
);

describe("Profile", () => {
  it("shows initial messages", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).not.toBeCalledWith("/login");

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /John Doe/i
      })
    );
    const role = await waitFor(() => screen.getByTestId("role"));
    const email = await waitFor(() =>
      screen.getByRole("heading", {
        name: /johndoe@gmail.com/i
      })
    );

    expect(heading).toBeInTheDocument();
    expect(role).toBeInTheDocument();
    expect(email).toBeInTheDocument();
  });

  it("renders job", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    const job = await waitFor(() =>
      screen.getByText("Kidney Cancer Detection")
    );

    expect(job).toBeInTheDocument();
  });

  it("renders number of jobs", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    const job = await waitFor(() => screen.getByText("1 jobs"));

    expect(job).toBeInTheDocument();
  });

  it("renders copy id section for customer", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    const copyIdText = await waitFor(() => screen.getByText(/Copy.*id/i));
    const copyButton = await waitFor(() =>
      screen.getByTestId("copy-id-button")
    );

    expect(copyIdText).toBeInTheDocument();
    expect(copyButton).toBeInTheDocument();
  });
});
