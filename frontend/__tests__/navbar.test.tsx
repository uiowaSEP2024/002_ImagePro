// __tests__/navbar.test.jsx

import { render, screen } from "@testing-library/react";
import { Navbar, Button, Link, Text, Card, Radio } from "@nextui-org/react";
import TopNavbar from "../src/pages/navbar"
import "@testing-library/jest-dom";

describe("NavBar", () => {

  it("renders navbar unchanged", () => {
    const { container } = render(<TopNavbar />);
    expect(container).toMatchSnapshot();
  });
});
