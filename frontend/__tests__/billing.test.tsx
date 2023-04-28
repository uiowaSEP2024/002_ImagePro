import { act, render, screen, waitFor } from "@testing-library/react";
import Billing from "@/pages/billing";
import Login from "@/pages/login";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import * as data from "@/data";
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

describe("Billing", () => {
  it("renders a heading", async () => {
    await act(async () =>
      render(<Billing />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).not.toBeCalledWith("/login");

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Billing page/i
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("does not render login or signup", async () => {
    await act(async () =>
      render(<Login />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).toBeCalledWith("/dashboard");

    await act(async () =>
      render(<Signup />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).toBeCalledWith("/dashboard");
  });
});
