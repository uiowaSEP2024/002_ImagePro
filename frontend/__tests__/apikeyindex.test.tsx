import { act, render, waitFor } from "@testing-library/react";
import ApiKeys from "@/pages/apikeys";
import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";
import { User } from "@/data/types";

const testCustomer: User = Object.freeze({
  id: 1,
  first_name: "John",
  last_name: "Doe",
  email: "johndoe@gmail.com",
  role: "customer"
});

const testProvider: User = Object.freeze({
  id: 1,
  first_name: "Bot",
  last_name: "Image",
  email: "botimage@gmail.com",
  role: "provider"
});

const mockRouterPush = jest.fn();
jest.mock("next/router", () => ({
  useRouter() {
    return {
      route: "/",
      pathname: "",
      query: "",
      asPath: "",
      push: mockRouterPush
    };
  }
}));

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

jest.spyOn(data, "fetchAPIkeys").mockImplementation(() =>
  Promise.resolve([
    {
      id: 1,
      user_id: 2,
      key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
      created_at: "2021-03-01T00:00:00.000Z",
      note: "Test note"
    }
  ])
);

describe("API Keys Page", () => {
  describe("when user is provider", () => {
    beforeEach(() => {
      jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
        Promise.resolve({
          user: testProvider,
          message: ""
        })
      );
    });

    it("renders a list of API keys", async () => {
      const { getByTestId } = await act(async () =>
        render(<ApiKeys />, { wrapper: AuthContextProvider })
      );

      await waitFor(() => expect(mockRouterPush).toHaveBeenCalledTimes(0));

      const card = await waitFor(() => getByTestId("testkeys"));

      await waitFor(() => expect(card).toBeInTheDocument());
    });
  });

  describe("when user is not provider", () => {
    beforeEach(() => {
      jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
        Promise.resolve({
          user: testCustomer,
          message: ""
        })
      );
    });
    it("redirects to login", async () => {
      await act(async () =>
        render(<ApiKeys />, { wrapper: AuthContextProvider })
      );

      await waitFor(() =>
        expect(mockRouterPush).toHaveBeenCalledWith("/dashboard")
      );
    });
  });
});
