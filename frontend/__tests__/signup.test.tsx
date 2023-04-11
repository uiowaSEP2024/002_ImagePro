import { render, screen, waitFor, fireEvent, getByTestId } from "@testing-library/react";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";

jest.mock('next/router', () => ({
  useRouter() {
    return ({
      route: '/',
      pathname: '',
      query: '',
      asPath: '',
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },  beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    });
  },
}));

const router = useRouter()

jest.mock('@/utils/auth', () => ({
  checkUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {detail : "Not authenticated"} )
    });
  },
}));

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Signup", () => {
  it("renders text", async () => {
  
    render(<Signup />);

    expect(router.push).not.toBeCalledWith('/');

    const text = await waitFor(() =>
    screen.getByRole("heading", {
      name: /Sign Up/i,
    }));

    expect(text).toBeInTheDocument();
  
  });

  it('signup on change', async () => {
    
    const { queryByPlaceholderText } = render(<Signup />);

    const firstNameInput = queryByPlaceholderText('First Name') as HTMLInputElement;
    fireEvent.input(firstNameInput, { target: { value: 'John' } });
    const lastNameInput = queryByPlaceholderText('Last Name') as HTMLInputElement;
    fireEvent.input(lastNameInput, { target: { value: 'Smith' } });
    const emailInput = queryByPlaceholderText('Email') as HTMLInputElement;
    fireEvent.input(emailInput, { target: { value: 'abc@gmail.com' } });
    const passInput = queryByPlaceholderText('Password') as HTMLInputElement;
    fireEvent.input(passInput, { target: { value: 'abc' } });
    const pass2Input = queryByPlaceholderText('Confirm Password') as HTMLInputElement;
    fireEvent.input(pass2Input, { target: { value: 'abc' } });

    expect(firstNameInput.value).toBe('John');
    expect(lastNameInput.value).toBe('Smith');
    expect(emailInput.value).toBe('abc@gmail.com');
    expect(passInput.value).toBe('abc');
    expect(pass2Input.value).toBe('abc');

    //const button = await waitFor(() => screen.getByTestId("signup"));
    //fireEvent.click(button);

  });

});
