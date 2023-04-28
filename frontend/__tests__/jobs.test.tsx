
import { act, render, screen, waitFor, fireEvent } from "@testing-library/react";
import Jobs from "@/pages/jobs";

import * as data from "@/data/index";

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";

const mockRouterPush = jest.fn();
jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: "",
      push: mockRouterPush
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
      role: "provider"
    },
    message: ""
  })
);

jest.spyOn(data, "fetchJobs").mockImplementation(() => Promise.resolve(
  [{
    id: 1,
    provider_job_name: "Kidney Cancer Detection",
    customer_id: 1,
    provider_job_id: "236",
    provider_id: 2,
    created_at: "2021-03-01T00:00:00.000Z"
  }]));
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

  it("renders jobs in list", async () => {
    await act(async () => render(<Jobs />, { wrapper: AuthContextProvider }));

    const job = await waitFor(() => screen.getByText("Kidney Cancer Detection"));

    expect(job).toBeInTheDocument();
  });

  it("renders a search bar", async () => {
    await act(async () => render(<Jobs />, { wrapper: AuthContextProvider }));

    const bar = await waitFor(() => screen.getByTestId("search"));

    expect(bar).toBeInTheDocument();
  });

  it('search on change', () => {
    const handleSearch = jest.fn((value) => {});
    
    const { queryByPlaceholderText } = render(<input id="search" type="text" placeholder="Search jobs..." onChange={handleSearch} />);

    const searchInput = queryByPlaceholderText('Search jobs...') as HTMLInputElement;

    fireEvent.input(searchInput, { target: { value: 'test' } });

    expect(searchInput.value).toBe('test');
    expect(handleSearch).toHaveBeenCalled();
  });

});
