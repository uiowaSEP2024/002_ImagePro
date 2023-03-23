import { render, screen, RenderResult } from "@testing-library/react";
import Login from "@/pages/login";
import "@testing-library/jest-dom";

jest.mock("next/router", () => require("next-router-mock"));
let documentBody: RenderResult;


// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
// https://www.pluralsight.com/guides/how-to-test-react-components-in-typescript
describe("Login", () => {

  beforeEach(() => {
    // Arrange
    documentBody = render(<Login />);
  });

  test("should display a blank login form", async () => {
  
    expect(documentBody).toHaveFormValues({
      email: "",
      password: "",
    });
  });


  xit("renders Login unchanged", () => {
    const { container } = render(<Login />);
    expect(container).toMatchSnapshot();
  });
});
