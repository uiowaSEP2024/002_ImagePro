import { render, screen, RenderResult } from "@testing-library/react";
import Dashboard from "@/pages/dashboard";
import "@testing-library/jest-dom";
let documentBody: RenderResult;

jest.mock('next/router', () => require('next-router-mock'));

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Dashboard", () => {

  beforeAll(() => {
    (global as any).fetch = fetch as (input: RequestInfo, init?: RequestInit) => Promise<Response>;
  });

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