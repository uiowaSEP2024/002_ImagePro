import React from "react";
import { act, render, screen, waitFor } from "@testing-library/react";
import Analytics from "@/pages/analytics";
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

jest.spyOn(data, "fetchStudies").mockImplementation(() =>
  Promise.resolve([
    {
      id: 1,
      provider_study_name: "Kidney Cancer Detection",
      hospital_id: 1,
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
