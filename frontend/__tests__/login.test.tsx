import { render, screen } from "@testing-library/react";
import Login from "@/pages/login";
import "@testing-library/jest-dom";

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Login", () => {
  it("renders Login unchanged", () => {
    const { container } = render(<Login />);
    expect(container).toMatchSnapshot();
  });
});