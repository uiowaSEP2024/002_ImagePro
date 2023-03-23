import { render, screen, RenderResult } from "@testing-library/react";
import Dashboard from "@/pages/dashboard";
import "@testing-library/jest-dom";

let documentBody: RenderResult;

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Dashboard", () => {

  beforeEach(() => {
    // Arrange
    documentBody = render(<Dashboard />);
  });

  it("renders a heading", () => {
    render(<Dashboard />);
    const heading = screen.getByRole("heading", {
      name: /Dashboard page/i,
    });
    expect(heading).toBeInTheDocument();
  });

  xit('shows initial messages', () => {
    // ASSERT
    const welcome = documentBody.getByText('Welcome');
    expect(welcome).toBeInTheDocument();
  });
});