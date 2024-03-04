import {
  act,
  fireEvent,
  render,
  screen,
  waitFor
} from "@testing-library/react";
import StudyPage from "@/pages/studies/[id]";
import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";
import { kidneyStudyFixture } from "fixtures/kidneyStudyFixture";

const studyId = "1";

// Mock the router to return information needed for the page to render
const mockRouterPush = jest.fn();
jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: { id: studyId },
      push: mockRouterPush
    };
  }
}));

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
  Promise.resolve({
    user: {
      first_name: "John",
      last_name: "Doe",
      email: "johndoe@gmail.com",
      id: 1,
      role: "provider"
    },
    message: ""
  })
);

jest.spyOn(data, "fetchStudies").mockImplementation(() =>
  Promise.resolve([kidneyStudyFixture])
);

jest.spyOn(data, "fetchEvents").mockImplementation(() =>
  Promise.resolve([
    {
      kind: "step",
      name: "Scanning Left Kidney",
      study_id: 1,
      id: 1,
      created_at: "2021-03-01T00:00:00.000Z"
    }
  ])
);

jest.spyOn(data, "fetchStudyById").mockImplementation(() =>
  Promise.resolve(kidneyStudyFixture)
);

describe("Study Page", () => {
  it("renders a heading", async () => {
    await act(async () => {
      render(<StudyPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: new RegExp(`Study #${studyId}`, "i")
      })
    );

    expect(heading).toBeInTheDocument();
  });

  it("renders a list of study events", async () => {
    await act(async () => {
      render(<StudyPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const table = await waitFor(() => screen.getByTestId("events-timeline"));

    expect(table).toBeInTheDocument();
  });

  it("renders a progress bar", async () => {
    await act(async () => {
      render(<StudyPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const progressBar = await waitFor(() => screen.getByRole("progressbar"));

    expect(progressBar).toBeInTheDocument();
    expect(progressBar).toHaveAttribute("aria-valuenow", "1");
  });

  it("has back button", async () => {
    await act(async () => {
      render(<StudyPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const backarrow = await waitFor(() => screen.getByTestId("backarrow"));

    expect(backarrow).toBeInTheDocument();

    fireEvent.click(backarrow);

    const link = await waitFor(() => screen.getByTestId("backlink"));

    expect(link).toHaveAttribute("href", "/studies");
  });

  it("renders an admin link at bottom", async () => {
    await act(async () => {
      render(<StudyPage initialIsPageLoading={false} />, {
        wrapper: AuthContextProvider
      });
    });

    const adminLink = await waitFor(() =>
      screen.getByText("Issue with this study? Contact system administrator at")
    );

    expect(adminLink).toBeInTheDocument();
  });
});
