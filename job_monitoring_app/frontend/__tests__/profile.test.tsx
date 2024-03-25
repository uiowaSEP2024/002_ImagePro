import { act, render, screen, waitFor } from "@testing-library/react";
import Profile from "@/pages/profile";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";
import { kidneyStudyFixture } from "fixtures/kidneyStudyFixture";

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

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

jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
  Promise.resolve({
    user: {
      first_name: "John",
      last_name: "Doe",
      email: "johndoe@gmail.com",
      id: 1,
      role: "hospital"
    },
    message: ""
  })
);

jest.spyOn(data, "fetchStudies").mockImplementation(() =>
  Promise.resolve([kidneyStudyFixture])
);
jest.spyOn(data, "fetchEvents").mockImplementation(() => Promise.resolve([]));
jest.spyOn(data, "fetchStudyById").mockImplementation(() =>
  Promise.resolve(kidneyStudyFixture)
);

describe("Profile", () => {
  it("shows initial messages", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    expect(useRouter().push).not.toBeCalledWith("/login");

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /John Doe/i
      })
    );
    const role = await waitFor(() => screen.getByTestId("role"));
    const email = await waitFor(() =>
      screen.getByRole("heading", {
        name: /johndoe@gmail.com/i
      })
    );

    expect(heading).toBeInTheDocument();
    expect(role).toBeInTheDocument();
    expect(email).toBeInTheDocument();
  });

  it("renders study", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    const study = await waitFor(() =>
      screen.getByText("Kidney Cancer Detection")
    );

    expect(study).toBeInTheDocument();
  });

  it("renders number of studies", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    const study = await waitFor(() => screen.getByText("1 studies"));

    expect(study).toBeInTheDocument();
  });

  it("renders copy id section for hospital", async () => {
    await act(async () =>
      render(<Profile />, { wrapper: AuthContextProvider })
    );

    const copyIdText = await waitFor(() => screen.getByText(/Copy.*id/i));
    const copyButton = await waitFor(() =>
      screen.getByTestId("copy-id-button")
    );

    expect(copyIdText).toBeInTheDocument();
    expect(copyButton).toBeInTheDocument();
  });
});
