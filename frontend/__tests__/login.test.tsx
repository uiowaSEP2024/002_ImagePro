
import { act, render, screen, RenderResult, waitFor, fireEvent } from "@testing-library/react";
import Login from "@/pages/login";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
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
  fetchCheckUserLoggedIn() {
    return new Promise((resolve) => {
      resolve({ detail: "Not authenticated" });
    });
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
}));

describe("Login", () => {
  it("renders text", async () => {
    await act(async () => render(<Login />, { wrapper: AuthContextProvider }));

    expect(useRouter().push).not.toBeCalledWith("/");

    const text = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Login/i
      })
    );

    expect(text).toBeInTheDocument();
  });

  it('login on change', async () => {

    await act(async () => render(<Login />, { wrapper: AuthContextProvider }));

    const emailInput = screen.queryByPlaceholderText('Email') as HTMLInputElement;
    fireEvent.input(emailInput, { target: { value: 'user@example.com' } });
    const passInput = screen.queryByPlaceholderText('Password')  as HTMLInputElement;
    fireEvent.input(passInput, { target: { value: 'abc' } });

    expect(emailInput.value).toBe('user@example.com');
    expect(passInput.value).toBe('abc');

    const button = await waitFor(() => screen.getByTestId("login"));
    fireEvent.click(button);

    expect(button).toBeInTheDocument();
  });

  it('show password button exists', async () => {

    await act(async () => render(<Login />, { wrapper: AuthContextProvider }));

    const button = await waitFor(() => screen.getByTestId("showbutton"));

    fireEvent.click(button);
    expect(button).toBeInTheDocument();

  });

  });
