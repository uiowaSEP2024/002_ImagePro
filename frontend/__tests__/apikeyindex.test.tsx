import { act, render, waitFor } from "@testing-library/react";
import ApiKeys from "@/pages/apikeys";
import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";

jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: "",
      asPath: "",
      push: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn()
      },
      beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
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
      id: 1
    },
    message: ""
  })
);

jest.spyOn(data, "fetchAPIkeys").mockImplementation(() =>
  Promise.resolve([
    {
      id: 1,
      user_id: 2,
      key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
      created_at: "2021-03-01T00:00:00.000Z"
    }
  ])
);

describe("API Keys Page", () => {
  it("renders a list of API keys", async () => {
    const { getByTestId } = await act(async () =>
      render(<ApiKeys />, { wrapper: AuthContextProvider })
    );

    const card = await waitFor(() => getByTestId("testkeys"));

    await waitFor(() => expect(card).toBeInTheDocument());
  });
});
