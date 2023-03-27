import { render, screen, waitFor } from "@testing-library/react";
import Jobs from "@/pages/jobs";

import "@testing-library/jest-dom";

describe("Jobs List Page", () => {
  it("renders a heading", async () => {
    render(<Jobs />);

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: /Jobs/i,
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of jobs", async () => {
    render(<Jobs />);

    const table = await waitFor(() =>
      screen.getByRole("grid", {
        name: /Jobs/i,
      })
    );

    expect(table).toBeInTheDocument();
  });
});
