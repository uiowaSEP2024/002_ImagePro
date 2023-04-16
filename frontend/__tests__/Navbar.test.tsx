// __tests__/navbar.test.jsx

import { render, screen, RenderResult, waitFor, fireEvent } from "@testing-library/react";
import Navbar from "../src/components/Navbar";
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

jest.mock("@/utils/auth", () => ({
  checkUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {detail : "already logged in!"} )
    });
  },
  sendLogOutReq(){
    console.log("Heyyy there")
    return new Promise((resolve) => {
      const data = {
        email: "user@example.com",
        first_name: "string",
        last_name: "string",
        id: 0
      }
      resolve( data)
    });
  }
}))

const router = useRouter()

describe("NavBar", () => {

  it("renders text", async () => {
  
    render(<Navbar />);

    expect(router.push).not.toBeCalledWith("/");

    const text = await waitFor(() =>
      screen.getByRole("link", {
        name: /Home/i,
      }));

    await waitFor(()=>{
      expect(text).toBeInTheDocument();
    })
  });
  
  it("logs out", async () => {
    const button = await waitFor(() => screen.getByTestId("logoutButton"));
    fireEvent.click(button);

    expect(router.push).toBeCalledWith("/");

  });

});
