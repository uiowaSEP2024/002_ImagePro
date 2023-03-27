import { render, screen, waitFor } from "@testing-library/react";
import Jobs from "@/pages/jobs";

import "@testing-library/jest-dom";

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

  fetchJobs() {
  
    return new Promise((resolve) => {
  
      resolve([])
  
    });
  
  },

  fetchEvents() {
  
    return new Promise((resolve) => {
  
      resolve([])
  
    });
  
  },
  
}));

describe("Jobs List Page", () => {
  it("renders a heading", async () => {
    render(<Jobs />);

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Jobs/i,
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of jobs", async () => {
    render(<Jobs />);

    const table = await waitFor(() =>
      screen.getByRole("grid", {
        name: /Jobs/i,
      })
    );

    expect(table).toBeInTheDocument();
  });
});
