import { render, screen } from "@testing-library/react";
import Dashboard from "@/pages/dashboard";
import "@testing-library/jest-dom";

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Dashboard", () => {
  it("renders a heading", () => {
    render(<Dashboard />);
    const heading = screen.getByRole("heading", {
      name: /Dashboard page/i,
    });
    expect(heading).toBeInTheDocument();
  });

  xit("renders Dashboard unchanged", () => {
    const { container } = render(<Dashboard />);
    // expect(container).toMatchSnapshot();
  });
});