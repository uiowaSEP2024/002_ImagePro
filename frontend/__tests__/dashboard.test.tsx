import { render, screen, RenderResult, waitFor } from "@testing-library/react";
import Dashboard from "@/pages/dashboard";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";

jest.mock('next/router', () => ({
  useRouter() {
    return ({
      route: '/',
      pathname: '',
      query: '',
      asPath: '',
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },  beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    });
  },
}));

const router = useRouter()

jest.mock('@/utils/auth', () => ({
  checkUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {detail : "already logged in!"} )
    });
  },
}));

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
describe("Dashboard", () => {

  it("renders a heading", async () => {
    render(<Dashboard />);

    expect(router.push).not.toBeCalledWith('/login');

    const heading = await waitFor(() =>
    screen.getByRole("heading", {
      name: /Welcome/i,
    }));

    expect(heading).toBeInTheDocument();

  });

  it("renders Jobs card", async () => {
    render(<Dashboard />);

    expect(router.push).not.toBeCalledWith('/login');

    const table = await waitFor(() =>
    screen.getByRole("Text", {
      name: /Jobs/i,
    }));

    expect(table).toBeInTheDocument();

    const input = await waitFor(() =>
    screen.getByRole("Text", {
      name: /View past and currently active jobs/i,
    }));

    expect(input).toBeInTheDocument();

  });

});