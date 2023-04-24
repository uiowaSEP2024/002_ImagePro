
import { act, render, screen, waitFor, fireEvent } from "@testing-library/react";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";
import { AuthContextProvider } from "@/contexts/authContext";
import { fetchLogin } from "@/data";

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
  fetchCheckUserLoggedIn() {
    return new Promise((resolve) => {
      resolve({ detail: "Not authenticated" });
    });
  },

  fetchSignUp(){
    console.log("Heyyy there")
    return new Promise((resolve) => {
      const data = {
        email: "user@example.com",
        first_name: "string",
        last_name: "string",
        id: 0
      }
      resolve( data)
    })},

  fetchLogin(){
    console.log("Heyyy there")
    return new Promise((resolve) => {
      const data = new URLSearchParams({
        email: "user@example.com",
        password: "abc"
      });
      resolve( data)
    })},
}))

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("SignUp", () => {
  it("renders text", async () => {
    await act(async () => render(<Signup />, { wrapper: AuthContextProvider }));
    expect(useRouter().push).not.toBeCalledWith("/");

    const text = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Sign Up/i
      })
    );

    expect(text).toBeInTheDocument();
  });
 
  it("signup on change", async () => {

    await act(async () => render(<Signup />, { wrapper: AuthContextProvider }));

    await waitFor(()=>{
      const firstNameInput = screen.queryByPlaceholderText("First Name") as HTMLInputElement;
      fireEvent.input(firstNameInput, { target: { value: "John" } });
      const lastNameInput = screen.queryByPlaceholderText("Last Name") as HTMLInputElement;
      fireEvent.input(lastNameInput, { target: { value: "Smith" } });
      const emailInput = screen.queryByPlaceholderText("Email") as HTMLInputElement;
      fireEvent.input(emailInput, { target: { value: "abc@gmail.com" } });
      const passInput = screen.queryByPlaceholderText("Password") as HTMLInputElement;
      fireEvent.input(passInput, { target: { value: "abc" } });
      const pass2Input = screen.queryByPlaceholderText("Confirm Password") as HTMLInputElement;
      fireEvent.input(pass2Input, { target: { value: "abc" } });

      expect(firstNameInput.value).toBe("John");
      expect(lastNameInput.value).toBe("Smith");
      expect(emailInput.value).toBe("abc@gmail.com");
      expect(passInput.value).toBe("abc");
      expect(pass2Input.value).toBe("abc");
    });


    const button = await waitFor(() => screen.getByTestId("signup"));
    fireEvent.click(button);

    const notificationMessage = await waitFor(() => screen.getByText(/Sign up successful/i));

    await waitFor(()=>{
      expect(notificationMessage).toBeInTheDocument();
    });
  });

});