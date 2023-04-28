// __tests__/index.test.jsx

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import Home from "@/pages/index";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";

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

    fireEvent.click(button);
    expect(useRouter().push).toBeCalled();

  });

  it("renders a button to analytics", async () => {
    render(<Home />);

    const button = await waitFor(() => screen.getByText("Get Started With Analytics"));

    expect(button).toBeInTheDocument();

    fireEvent.click(button);
    expect(useRouter().push).toBeCalled();

  });
});
