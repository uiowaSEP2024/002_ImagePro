import { render, screen, RenderResult } from "@testing-library/react";
import 'core-js/es/modules/es.promise';
import Login from "@/pages/login";
import "@testing-library/jest-dom";
import fetch from 'node-fetch';


jest.mock("next/router", () => require("next-router-mock"));
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
