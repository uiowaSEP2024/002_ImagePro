import React from "react";
import { AuthContextProvider } from "@/contexts/authContext";
import { fireEvent, render, waitFor, act } from "@testing-library/react";
import { useAuthContext } from "@/hooks/useAuthContext";
import * as data from "@/data/index";

import "@testing-library/jest-dom"

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
      }, beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    });
  },
}));


jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data"),
}));


describe("authContext", () => {
  const TestComponent = () => {
    const { currentUser, logOut } = useAuthContext();
    return (
      <div>
        {!!currentUser && <div role="user">{currentUser.first_name}</div>}
        <button onClick={logOut}>Log Out</button>
      </div>
    );
  };


  test("currentUser available when logged in and reset on logged out", async () => {

    jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
      Promise.resolve({user: { first_name: "John", last_name: "Doe", email: "johndoe@gmail.com"}, message: ""}),
    );


    const {getByRole, queryByRole} = await act(async () => render(
      <AuthContextProvider>
        <TestComponent />
      </AuthContextProvider>,
    ));


    await waitFor(() => {
      expect(getByRole("user")).toBeInTheDocument();
    });


    // Setup signed out mocks
    jest.spyOn(data, "fetchLogout").mockImplementation(() =>
      Promise.resolve(),
    );

    jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
      Promise.resolve({message: "Not authenticated"}),
    );

    fireEvent.click(getByRole("button", {name: "Log Out"}))


    await waitFor(() => {
      expect(queryByRole("user")).not.toBeInTheDocument();
    })

  })
})
