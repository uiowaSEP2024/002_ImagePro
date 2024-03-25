import { act, render, waitFor, screen, fireEvent } from "@testing-library/react";
import ApiKeys from "@/pages/apikeys";
import "@testing-library/jest-dom";
import { AuthContextProvider } from "@/contexts/authContext";
import * as data from "@/data";
import { User } from "@/data/types";

const testHospital: User = Object.freeze({
  id: 1,
  first_name: "John",
  last_name: "Doe",
  email: "johndoe@gmail.com",
  role: "hospital"
});

const testProvider: User = Object.freeze({
  id: 1,
  first_name: "Bot",
  last_name: "Image",
  email: "botimage@gmail.com",
  role: "provider"
});

jest.mock("@/data", () => ({
  __esModule: true,
  ...jest.requireActual("@/data")
}));

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

jest.spyOn(data, "fetchAPIkeys").mockImplementation(() =>
    Promise.resolve([{
      id: 1,
      user_id: 2,
      key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
      note: "my key",
      created_at: "2021-03-01T00:00:00.000Z"
    }])
);

jest.spyOn(data, "fetchGenAPIKeys").mockImplementation(() =>
  Promise.resolve({
      note: "my key",
      key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
  }));

describe("API Keys Page", () => {
  beforeEach(() => {
    jest.spyOn(data, "fetchCheckUserLoggedIn").mockImplementation(() =>
      Promise.resolve({
        user: testProvider,
        message: ""
      })
    );
  });
  it("renders a heading", async () => {
    await act(async () => {
      render(<ApiKeys />, {
        wrapper: AuthContextProvider
      });
    });

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: 'API Keys'
      })
    );
    const text = await waitFor(() => screen.getByText('Manage API Keys for your provider account'));

    expect(heading).toBeInTheDocument();
    expect(text).toBeInTheDocument();

  });

  it("prompts user to create key", async () => {
    await act(async () => {
      render(<ApiKeys />, {
        wrapper: AuthContextProvider
      });
    });

    const heading = await waitFor(() =>
      screen.getByRole("heading", {
        name: 'Create API Key'
      })
    );

    expect(heading).toBeInTheDocument();
  });

  describe("when user is provider", () => {
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
          user: testHospital,
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

  it('submits APIKey on change', async () => {

    await act(async () => render(<ApiKeys />, { wrapper: AuthContextProvider }));

    const noteInput = screen.queryByPlaceholderText('Note') as HTMLInputElement;
    fireEvent.input(noteInput, { target: { value: 'My Key' } });

    expect(noteInput.value).toBe('My Key');

    const button = await waitFor(() => screen.getByTestId("submit"));
    fireEvent.click(button);

    expect(button).toBeInTheDocument();

    const notificationMessage = await waitFor(() => screen.getByText('Please copy this key for later. This is the only time you will see it.'));

    await waitFor(()=>{
      expect(notificationMessage).toBeInTheDocument();
    });
  });

});
