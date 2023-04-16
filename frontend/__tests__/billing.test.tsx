import { render, screen, waitFor } from "@testing-library/react";
import Billing from "@/pages/billing";
import Login from "@/pages/login";
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
      resolve( {detail : "already logged in!"} )
    });
  },
}));

describe("Billing", () => {
  
  it("renders a heading", async () => {
  
    render(<Billing />);

    expect(router.push).not.toBeCalledWith('/login');

    const heading = await waitFor(() =>
    screen.getByRole("heading", {
      name: /Billing page/i,
    }));

    expect(heading).toBeInTheDocument();
  
  });

  it('other pages are not rendered', async () => {
    render(<Login />);
    expect(router.push).toBeCalledWith("/");

    render(<Signup />);
    expect(router.push).toBeCalledWith("/");

  });
});