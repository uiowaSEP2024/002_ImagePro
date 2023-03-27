import { render, screen, waitFor } from "@testing-library/react";
import JobPage from "@/pages/jobs/[id]";

import "@testing-library/jest-dom";

const jobId = "1";

// Mock the router to return information needed for the page to render
jest.mock("next/router", () => ({
  useRouter() {
    return {
      query: { id: jobId },
    };
  },
}));

jest.mock("@/data", () => ({

  fetchJobById() {
  
    return new Promise((resolve) => {
  
      resolve( {
        id: 1,
        provider_job_name: "Kidney Cancer Detection",
        customer_id: 1,
        provider_job_id: "236",
        provider_id: 2,
        created_at: "2021-03-01T00:00:00.000Z",
      } )
  
    });
  
  },

  fetchEvents() {
  
    return new Promise((resolve) => {
  
      resolve([])
  
    });
  
  },
  
}));

describe("Job Page", () => {
  it("renders a heading", async () => {
    render(<JobPage />);

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: new RegExp(`Job #${jobId}`, "i"),
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of job events", async () => {
    render(<JobPage />);

    const table = await waitFor(() =>
      screen.getByRole("grid", {
        name: /Events/i,
      })
    );

    expect(table).toBeInTheDocument();
  });

  it("renders a progress bar", async () => {
    render(<JobPage />);

    const progressBar = await waitFor(() =>
      screen.getByRole("progressbar", {
        name: /Progress/i,
      })
    );

    expect(progressBar).toBeInTheDocument();
  });
});
