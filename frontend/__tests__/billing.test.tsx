import { render, screen } from "@testing-library/react";
import Billing from "@/pages/billing";
import "@testing-library/jest-dom";
import fetch from 'node-fetch';



jest.mock('next/router', () => require('next-router-mock'));

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Billing", () => {

  beforeAll(() => {
    (global as any).fetch = fetch as (input: RequestInfo, init?: RequestInit) => Promise<Response>;
  });

  it("renders a heading", () => {
    render(<Billing />);
    const heading = screen.getByRole("heading", {
      name: /Billing page/i,
    });
    expect(heading).toBeInTheDocument();
  });

});