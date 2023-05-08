import React from "react";
import { act, render, screen, waitFor } from "@testing-library/react";
import Billing from "@/pages/billing";
import Login from "@/pages/login";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";
import JobsChart from "@/components/stackedChart";
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

jest.spyOn(data, "fetchJobs").mockImplementation(() =>
  Promise.resolve([
    {
      id: 1,
      provider_job_name: "Kidney Cancer Detection",
      customer_id: 1,
      provider_job_id: "236",
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

describe("Billing", () => {
  it("renders a heading", async () => {
    await act(async () =>
      render(<Billing />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).not.toBeCalledWith("/login");

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Billing/i
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

  // it("Renders a Stacked Chart", () => {
  //   const wrapper = mount(
  //     <JobsChart />,
  //   )
  //   expect(wrapper).toMatchSnapshot()
  // })
});
