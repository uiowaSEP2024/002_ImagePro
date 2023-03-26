import { render, screen } from "@testing-library/react";
import Billing from "@/pages/billing";
import "@testing-library/jest-dom";
import fetch, { Response as FetchResponse } from 'node-fetch';


jest.mock('next/router', () => require('next-router-mock'));
jest.mock('node-fetch', () => jest.fn());

describe("Billing", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it("renders a heading", async () => {

    type ResponseBody = {
      data: any[];
    };
    
    const responseBody: ResponseBody = { data: [] };

    const blob = new Blob([JSON.stringify(responseBody)], { type: 'application/json' });

    const formData = new FormData();
    formData.append('data', blob);

    const response = new Response(blob, {
      status: 200,
      headers: { 'Content-type': 'application/json' },
    });

    jest.spyOn(global, 'fetch').mockResolvedValueOnce(response);

    render(<Billing />);

    const heading = screen.getByRole("heading", {
      name: /Billing page/i,
    });

    expect(heading).toBeInTheDocument();

    // Assert that the fetch function was called with the expected parameters
    expect(fetch).toHaveBeenCalledWith('/api/billing', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });
});

//  it("renders a heading", () => {
//    render(<Billing />);
//    const heading = screen.getByRole("heading", {
//      name: /Billing page/i,
//    });
//    expect(heading).toBeInTheDocument();
//  });

//});