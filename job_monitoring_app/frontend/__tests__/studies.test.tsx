import {
  act,
  render,
  screen,
  waitFor,
  fireEvent
} from "@testing-library/react";
import Studies from "src/pages/studies";

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

jest.spyOn(data, "fetchStudies").mockImplementation(() =>
  Promise.resolve([
    {
      id: 1,
      provider_study_name: "Kidney Cancer Detection",
      customer_id: 1,
      provider_study_id: "236",
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
jest.spyOn(data, "fetchStudyById").mockImplementation(() =>
  Promise.resolve({
    id: 1,
    provider_study_name: "Kidney Cancer Detection",
    customer_id: 1,
    provider_study_id: "236",
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

describe("Studys List Page", () => {
  it("renders a heading", async () => {
    await act(async () => render(<Studies />, { wrapper: AuthContextProvider }));

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Studies/i
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of studies", async () => {
    await act(async () => render(<Studies />, { wrapper: AuthContextProvider }));
    const table = await waitFor(() =>
      screen.getByRole("grid", {
        name: /Studies/i
      })
    );

    expect(table).toBeInTheDocument();
  });

  it("renders studies in list", async () => {
    await act(async () => render(<Studies />, { wrapper: AuthContextProvider }));

    const study = await waitFor(() =>
      screen.getByText("Kidney Cancer Detection")
    );

    expect(study).toBeInTheDocument();
  });

  it("renders a search bar", async () => {
    await act(async () => render(<Studies />, { wrapper: AuthContextProvider }));

    const bar = await waitFor(() => screen.getByTestId("search"));

    expect(bar).toBeInTheDocument();
  });

  it("search on change", () => {
    const handleSearch = jest.fn((value) => {});

    const { queryByPlaceholderText } = render(
      <input
        id="search"
        type="text"
        placeholder="Search Studies..."
        onChange={handleSearch}
      />
    );

    const searchInput = queryByPlaceholderText(
      "Search studies..."
    ) as HTMLInputElement;

    fireEvent.input(searchInput, { target: { value: "test" } });

    expect(searchInput.value).toBe("test");
    expect(handleSearch).toHaveBeenCalled();
  });
});
