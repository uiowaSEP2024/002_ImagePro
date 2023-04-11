import { render, screen, waitFor, fireEvent } from "@testing-library/react";
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

  it("renders a search bar", async () => {
    render(<Jobs />);

    const bar = await waitFor(() =>
      screen.getByRole("input")
    );

    expect(bar).toBeInTheDocument();
  });

  it('search on change', () => {
    const handleSearch = jest.fn((value) => {});
    
    const { queryByPlaceholderText } = render(<input id="search" type="text" placeholder="Search jobs..." onChange={handleSearch} />);

    const searchInput = queryByPlaceholderText('Search jobs...') as HTMLInputElement;

    fireEvent.input(searchInput, { target: { value: 'test' } });

    expect(searchInput.value).toBe('test');
    expect(handleSearch).toHaveBeenCalledWith('test');
  });

});
