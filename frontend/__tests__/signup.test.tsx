import { render, screen } from "@testing-library/react";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Signup", () => {
  xit("renders Signup unchanged", () => {
    const { container } = render(<Signup />);
    // expect(container).toMatchSnapshot();
  });
});
