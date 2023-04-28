import { act, render, screen, waitFor } from "@testing-library/react";
import Dashboard from "@/pages/dashboard";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import * as data from "@/data";
import { AuthContextProvider } from "@/contexts/authContext";

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

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

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Dashboard", () => {
  it("renders a heading", async () => {
    await act(async () =>
      render(<Dashboard />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).not.toBeCalledWith("/login");

    const heading = await waitFor(() =>
      screen.getByText("Explore our tools"));

    expect(heading).toBeInTheDocument();
  });

  it("renders Jobs card", async () => {
    await act(async () => render(<Dashboard />, { wrapper: AuthContextProvider }));

    expect(useRouter().push).not.toBeCalledWith('/login');

    const table = await waitFor(() =>
    screen.getByText("Jobs"));

    expect(table).toBeInTheDocument();

  });

});
