import { render, screen } from "@testing-library/react";
import Billing from "@/pages/billing";
import "@testing-library/jest-dom";

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Billing", () => {
  it("renders a heading", () => {
    render(<Billing />);
    const heading = screen.getByRole("heading", {
      name: /Billing page/i,
    });
    expect(heading).toBeInTheDocument();
  });

  xit("renders Billing unchanged", () => {
    const { container } = render(<Billing />);
    // expect(container).toMatchSnapshot();
  });
});