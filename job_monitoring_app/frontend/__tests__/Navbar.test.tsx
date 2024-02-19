// __tests__/navbar.test.jsx
import { render, screen, RenderResult, waitFor, fireEvent, act } from "@testing-library/react";
import Navbar from "../src/components/Navbar";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import * as data from "@/data";
import { AuthContextProvider } from "@/contexts/authContext";
import { useAuthContext, useEnsureAuthenticated } from "@/hooks/useAuthContext";
import { createContext } from "react";

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

jest.mock("@/hooks/useAuthContext", () => ({
    useAuthContext() {
      return new Promise((resolve) => {
      });
    },
    useEnsureAuthenticated() {
      {
        return {
          currentUser: {
            first_name: "John",
            last_name: "Doe",
            email: "johndoe@gmail.com",
            id: 1},
          isAuthenticated: true,
          router: useRouter(),
        };
      }
    },

    fetchLogin(){
      console.log("Heyyy there")
      return new Promise((resolve) => {
        const data = new URLSearchParams({
          email: "user@example.com",
          password: "abc"
        });
        resolve( data)
      })}
    })
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

describe("NavBar", () => {

  it("renders text", async () => {
    await act(async () => render(<Navbar />, { wrapper: AuthContextProvider }));

    expect(useRouter().push).not.toBeCalledWith("/");

    const text = await waitFor(() =>
      screen.getByRole("link", {
        name: /Home/i,
      }));

    await waitFor(()=>{
      expect(text).toBeInTheDocument();
    })
  });

  it("logs in", async () => {
    await act(async () => render(<Navbar />, { wrapper: AuthContextProvider }));

    const button = await waitFor(() => screen.getByText("Log in"));

    expect(button).toBeInTheDocument();

  });

});
