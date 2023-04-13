import { render, screen, waitFor } from "@testing-library/react";
import Login from "@/pages/login";
import "@testing-library/jest-dom";
import { useRouter } from "next/router";


jest.mock("next/router", () => ({
  useRouter() {
    return ({
      route: "/",
      pathname: "",
      query: "",
      asPath: "",
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },  beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    });
  },
}));


jest.mock("@/data", () => ({
  fetchCheckUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {detail : "Not authenticated"} )
    });
  },
}));

describe("Login", () => {

  it("renders text", async () => {
  
    render(<Login />);

    expect(useRouter().push).not.toBeCalledWith("/");

    const text = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Login/i,
      }));

    expect(text).toBeInTheDocument();
  
  });

});

