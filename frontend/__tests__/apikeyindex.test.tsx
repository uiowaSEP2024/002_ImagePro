import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
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

jest.mock("@/data", () => ({
  fetchCheckUserLoggedIn() {
    Promise.resolve({
      user: {
        first_name: "John",
        last_name: "Doe",
        email: "johndoe@gmail.com",
        id: 1
      },
      message: ""
    })
  },
  fetchAPIkeys() {
    Promise.resolve([{
      id: 1,
      user_id: 2,
      key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
      note: "my key",
      created_at: "2021-03-01T00:00:00.000Z"
    }])
  },
  fetchGenAPIKeys() {
  console.log("Heyyy there")
  return new Promise((resolve) => {
    const data = {
      note: "my key",
      key: "q-jAqPWCRGr2u6SeK6r6UASAO0LBfJA",
    }
    resolve(data)
  })},
}));

describe("API Keys Page", () => {
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

  it("renders a list of API keys", async () => {
    const { getByTestId } = await act(async () =>
      render(<ApiKeys />, { wrapper: AuthContextProvider })
    );

    const card = await waitFor(() => getByTestId("testkeys"));

    await waitFor(() => expect(card).toBeInTheDocument());
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
