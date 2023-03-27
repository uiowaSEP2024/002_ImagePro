// __tests__/index.test.jsx

import { render, screen, waitFor } from "@testing-library/react";
import Home from "@/pages/index";
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


// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Home", () => {
  it("renders a heading", async () => {
    render(<Home />);

    const heading = await waitFor(() =>
    screen.getByRole("heading", {
      name: /welcome to the tracking site/i,
    }));

    expect(heading).toBeInTheDocument();
  });
});
