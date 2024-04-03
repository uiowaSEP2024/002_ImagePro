import React from "react";
import { act, render, screen, waitFor } from "@testing-library/react";
import Analytics from "@/pages/analytics";
import Login from "@/pages/login";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import * as data from "@/data";
import { AuthContextProvider } from "@/contexts/authContext";
import { kidneyStudyFixture } from "fixtures/kidneyStudyFixture";

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

jest.spyOn(data, "fetchStudies").mockImplementation(() =>
  Promise.resolve([kidneyStudyFixture])
);

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

jest.spyOn(data, "fetchProviders").mockImplementation(() => Promise.resolve([]));

jest.spyOn(data, "fetchHospitals").mockImplementation(() => Promise.resolve([]));

jest.mock("react-chartjs-2", () => ({
  Bar: () => null
}));

// jest.mock("@/components/StackedChart", () => () => null)

describe("Analytics", () => {
  jest.mock("react-chartjs-2", () => ({
    Bar: () => null
  }));
  it("renders a heading", async () => {
    await act(async () =>
      render(<Analytics />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).not.toBeCalledWith("/login");

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Analytics/i
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("does not render login or signup", async () => {
    await act(async () => render(<Login />, { wrapper: AuthContextProvider }));

    expect(useRouter().push).toBeCalledWith("/dashboard");

    await act(async () => render(<Signup />, { wrapper: AuthContextProvider }));

    expect(useRouter().push).toBeCalledWith("/dashboard");
  });
});
