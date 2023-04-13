import { render, screen, waitFor } from "@testing-library/react";
import Profile from "@/pages/profile";
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
      resolve( {detail : "already logged in!", user: {}} )
    });
  },
}));

describe("Profile", () => {

  it("shows initial messages", async () => {
    expect(useRouter().push).not.toBeCalledWith("/login");
    render(<Profile />);

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /First Name/i,
      }));
    
    expect(heading).toBeInTheDocument();
  });
});