import {
  act,
  fireEvent,
  render,
  screen,
  waitFor
} from "@testing-library/react";
import JobPage from "@/pages/jobs/[id]";
import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";

const jobId = "1";

// Mock the router to return information needed for the page to render
const mockRouterPush = jest.fn();
jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: { id: jobId },
      push: mockRouterPush
    };
  }
}));

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
  Promise.resolve({
    user: {
      first_name: "John",
      last_name: "Doe",
      email: "johndoe@gmail.com",
      id: 1,
      role: "provider"
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

jest.spyOn(data, "fetchEvents").mockImplementation(() =>
  Promise.resolve([
    {
      kind: "step",
      name: "Scanning Left Kidney",
      job_id: 1,
      id: 1,
      created_at: "2021-03-01T00:00:00.000Z"
    }
  ])
);

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

describe("Job Page", () => {
  it("renders a heading", async () => {
    await act(async () => {
      render(<JobPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: new RegExp(`Job #${jobId}`, "i")
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of job events", async () => {
    await act(async () => {
      render(<JobPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const table = await waitFor(() => screen.getByTestId("events-timeline"));

    expect(table).toBeInTheDocument();
  });

  it("renders a progress bar", async () => {
    await act(async () => {
      render(<JobPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const progressBar = await waitFor(() => screen.getByRole("progressbar"));

    expect(progressBar).toBeInTheDocument();
    expect(progressBar).toHaveAttribute("aria-valuenow", "1");
  });

  it("has back button", async () => {
    await act(async () => {
      render(<JobPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const backarrow = await waitFor(() => screen.getByTestId("backarrow"));

    expect(backarrow).toBeInTheDocument();

    fireEvent.click(backarrow);

    const link = await waitFor(() => screen.getByTestId("backlink"));

    expect(link).toHaveAttribute("href", "/jobs");
  });

  it("renders an admin link at bottom", async () => {
    await act(async () => {
      render(<JobPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const adminLink = await waitFor(() =>
      screen.getByText("Issue with this job? Contact system administrator at")
    );

    expect(adminLink).toBeInTheDocument();
  });
});