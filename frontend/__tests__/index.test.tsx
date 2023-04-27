// __tests__/index.test.jsx

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import Home from "@/pages/index";
import "@testing-library/jest-dom";

jest.mock("next/router", () => ({
  useRouter() {
    return ({
      route: "/",
      pathname: "",
      query: "",
      asPath: "",
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },  beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    });
  },
}));


jest.mock("@/data", () => ({
  fetchCheckUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( { user: {}} )
    });
  },
}));


// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Home", () => {
  it("renders a heading", async () => {
    render(<Home />);

    const heading = await waitFor(() =>
      screen.getByTestId("header"));

    expect(heading).toBeInTheDocument();
  });

  it("renders a button to jobs", async () => {
    render(<Home />);

    const button = await waitFor(() => screen.getByText("Learn More About Jobs"));

    expect(button).toBeInTheDocument();
  });

  it("renders a button to analytics", async () => {
    render(<Home />);

    const button = await waitFor(() => screen.getByText("Get Started With Analytics"));

    expect(button).toBeInTheDocument();
  });
});
