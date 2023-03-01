// __tests__/navbar.test.jsx

import { render, screen } from "@testing-library/react";
import NavBar from "@/pages/index";
import "@testing-library/jest-dom";

describe("NavBar", () => {
  it("renders a navbar with links", () => {
    render(<NavBar />);
    const link1 = screen.getByRole("link", {
      name: /Contact/i,
    });
    expect(link1).toBeInTheDocument();
  });

  it("renders navbar unchanged", () => {
    const { container } = render(<NavBar />);
    expect(container).toMatchSnapshot();
  });
});
