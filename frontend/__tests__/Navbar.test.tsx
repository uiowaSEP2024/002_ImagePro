// __tests__/navbar.test.jsx

import { render, screen, RenderResult } from "@testing-library/react";
import Navbar from "../src/components/Navbar";
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

describe("NavBar", () => {

  it("renders navbar unchanged", () => {
    render(<Navbar />);
  });
});
