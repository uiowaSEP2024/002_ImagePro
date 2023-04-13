import { render, waitFor } from "@testing-library/react";
import ApiKeys from "@/pages/apikeys";
import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";

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
      }, beforePopState: jest.fn(() => null),
      prefetch: jest.fn(() => null)
    });
  },
}));

jest.mock("@/data", () => ({
  fetchAPIkeys() {
    return new Promise((resolve) => {

      resolve([
        {
          id: 1,
          user_id: 2,
          key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
          created_at: "2021-03-01T00:00:00.000Z"
        }
      ])
    })
  }
}));


jest.mock("@/utils/auth", () => ({
  fetchCheckUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {user: {}} )
    });
  },
}));

describe("API Keys Page", () => {
  it("renders a list of API keys", async () => {
    const {getByTestId} = render(<AuthContextProvider>
      <ApiKeys />
    </AuthContextProvider>);


    const card = await waitFor(() =>
      getByTestId("testkeys"));

    await waitFor(() => expect(card).toBeInTheDocument());

  })
})