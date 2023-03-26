import { render, screen } from "@testing-library/react";
import Signup from "@/pages/signup";
import "@testing-library/jest-dom";

jest.mock('next/router', () => require('next-router-mock'));

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Signup", () => {
  it("renders Signup unchanged", () => {

    beforeAll(() => {
      (global as any).fetch = fetch as (input: RequestInfo, init?: RequestInit) => Promise<Response>;
    });

    const { container } = render(<Signup />);
    // expect(container).toMatchSnapshot();
  });
});
