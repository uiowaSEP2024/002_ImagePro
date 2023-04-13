import { act, render, screen, waitFor } from "@testing-library/react";
import Billing from "@/pages/billing";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import * as data from "@/data";
import { AuthContextProvider } from "@/contexts/authContext";

jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: "",
      asPath: "",
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },
      beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
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
      id: 1
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
});
