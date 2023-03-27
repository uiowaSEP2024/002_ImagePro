import { render, screen, RenderResult } from "@testing-library/react";
import 'core-js/es/modules/es.promise';
import Login from "@/pages/login";
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

const router = useRouter()

jest.mock('@/utils/auth', () => ({
  checkUserLoggedIn() {
    return new Promise((resolve) => {
      resolve( {detail : "Not authenticated"} )
    });
  },
}));

let documentBody: RenderResult;

// TODO: explore fixing snapshot testing with https://github.com/mui/material-ui/issues/21293#issuecomment-654921524
// https://www.pluralsight.com/guides/how-to-test-react-components-in-typescript
describe("Login", () => {

  beforeAll(() => {
    (global as any).fetch = fetch as (input: RequestInfo, init?: RequestInit) => Promise<Response>;
  });

  beforeEach(() => {
    // Arrange
    documentBody = render(<Login />);
  });

  
  });
