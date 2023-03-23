// __tests__/navbar.test.jsx

import { render, screen, RenderResult } from "@testing-library/react";
import Navbar from "../src/components/Navbar";
import "@testing-library/jest-dom";

let documentBody: RenderResult;

describe("NavBar", () => {

  beforeEach(() => {
    // Arrange
    documentBody = render(<Navbar />);
  });

  xit("renders navbar unchanged", () => {
    const { container } = render(<Navbar />);
    // expect(container).toMatchSnapshot();
  });
});
