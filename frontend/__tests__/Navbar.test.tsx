// __tests__/navbar.test.jsx

import { render } from "@testing-library/react";
import Navbar from "../src/components/Navbar";
import "@testing-library/jest-dom";

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

describe("NavBar", () => {
  it("renders navbar unchanged", () => {
    render(<Navbar />);
  });
});
