// __tests__/index.test.jsx

import { render, screen } from "@testing-library/react";
import Home from "@/pages/index";
import "@testing-library/jest-dom";

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Home", () => {
  it("renders a heading", () => {
    render(<Home />);
    const heading = screen.getByRole("heading", {
      name: /welcome to the tracking site/i,
    });
    expect(heading).toBeInTheDocument();
  });
});
