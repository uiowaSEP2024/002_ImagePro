import { render, RenderResult, screen, waitFor } from "@testing-library/react";
import Profile from "@/pages/profile";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";

let documentBody: RenderResult;
 
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

describe("Profile", () => {

    it('shows initial messages', async () => {
        expect(router.push).not.toBeCalledWith('/login');
        render(<Profile />);
        let documentBody: RenderResult;

        const heading = await waitFor(() =>
        screen.getByRole("heading", {
          name: /First Name/i,
        }));
    
        expect(heading).toBeInTheDocument();
      });
});