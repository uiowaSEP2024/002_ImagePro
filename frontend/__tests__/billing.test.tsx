import { render, screen, waitFor } from "@testing-library/react";
import Billing from "@/pages/billing";
import "@testing-library/jest-dom";

jest.mock('next/router', () => require('next-router-mock'));

jest.mock('@/utils/auth', () => ({
  checkUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {detail : "Not authenticated"} )
    });
  },
}));

describe("Billing", () => {
  
  it("renders a heading", async () => {
  
    render(<Billing />);

    const heading = await waitFor(() =>
    screen.getByRole("heading", {
      name: /Billing page/i,
    }));

    expect(heading).toBeInTheDocument();
  
  });
});