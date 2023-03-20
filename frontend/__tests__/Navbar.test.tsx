// __tests__/navbar.test.jsx

import { render, screen } from "@testing-library/react";
import Navbar from "../src/components/Navbar";
import "@testing-library/jest-dom";

describe("NavBar", () => {
  xit("renders navbar unchanged", () => {
    const { container } = render(<Navbar />);
    // expect(container).toMatchSnapshot();
  });
});
