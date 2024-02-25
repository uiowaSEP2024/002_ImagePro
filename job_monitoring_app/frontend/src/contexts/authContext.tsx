/**
 * This file contains the AuthContext and AuthContextProvider components of the application.
 * The AuthContext is a React context that provides a way to pass the authentication data down the component tree without having to pass props down manually at every level.
 * The AuthContextProvider is a React component that provides the actual data and functions that will be passed down to the components that subscribe to the AuthContext.
 * It fetches the current user data from the server, and provides functions for logging in, logging out, and refreshing the authentication data.
 *
 * https://react.dev/reference/react/createContext
 * https://vercel.com/guides/react-context-state-management-nextjs
 *
 */

// Import necessary libraries, components, hooks, and types.
import { fetchCheckUserLoggedIn, fetchLogin, fetchLogout } from "@/data";
import { User } from "@/data/types";
import { useRouter } from "next/router";
import React, { createContext, useEffect, useState } from "react";

// Define the type for the AuthContext props.
interface IAuthContextProps {
  currentUser?: User;
  isAuthenticating: boolean;
  setCurrentUser: (user: any) => void;
  setIsAuthenticating: (loading: boolean) => void;
  logOut: () => Promise<void>;
  logIn: (email: string, password: string) =>  Promise<{user: User}|void>;
  refreshAuth: () => Promise<void>;
}

/**
 * The AuthContext is a React context that provides a way to pass the authentication data down the component tree without having to pass props down manually at every level.
 */
export const AuthContext = createContext<IAuthContextProps>({
  currentUser: undefined,
  isAuthenticating: true,
  setCurrentUser: () => {},
  setIsAuthenticating: () => {},
  logOut: async () =>{},
  logIn: async () =>{},
  refreshAuth: async () =>{}
});

/**
 * The AuthContextProvider is a React component that provides the actual data and functions that will be passed down to the components that subscribe to the AuthContext.
 * It fetches the current user data from the server, and provides functions for logging in, logging out, and refreshing the authentication data.
 *
 * @param props - The children components that the AuthContextProvider will wrap around.
 * @returns - The AuthContext.Provider component that wraps around the children components, providing them with access to the AuthContext.
 */
export const AuthContextProvider = (props: React.PropsWithChildren) => {
  // Initialize state variables for the current user data and the authentication loading state.
  const [currentUser, setCurrentUser] = useState<User>();
  const [isAuthenticating, setIsAuthenticating] = useState(true);
  const router = useRouter();

  // Refresh the authentication data when the component mounts.
  useEffect(()=>{
    refreshAuth()
  }, [])

  /**
   * Define the logOut function.
   * This function sends a request to the server to log out the current user, then refreshes the authentication data and redirects the user to the login page.
   * @returns - The data returned from the server after the logout request.
   * @throws - An error if the logout request fails.
   */
  const logOut = async () => {
    try {
      await fetchLogout();
      await refreshAuth()
      router.push("/login");
    } catch (e) {
      throw e
    }
  };

  /**
   * Define the logIn function.
   * This function sends a request to the server to log in a user with the provided email and password, then refreshes the authentication data.
   *
   * @param email - The email of the user to log in.
   * @param password - The password of the user to log in.
   * @returns - The data returned from the server after the login request.
   */
  const logIn = async (email:string, password: string) => {
    let data
    try {
      data = await fetchLogin(email, password);
      await refreshAuth()
    } catch (e) {
      throw e
    }
    return data
  };

  /**
   * Define the refreshAuth function.
   * This function sends a request to the server to check if the current user is logged in, then updates the current user data and the authentication loading state based on the response.
   */
  const refreshAuth = async () =>{
    try{
      const data = await fetchCheckUserLoggedIn()
      setCurrentUser(data.user)
    }catch(e){
      setCurrentUser(undefined)
    }
    setIsAuthenticating(false)
  }

  // Render the AuthContextProvider component.
  return (
    <AuthContext.Provider
      value={{
        currentUser,
        isAuthenticating,
        setCurrentUser,
        setIsAuthenticating,
        logOut,
        logIn,
        refreshAuth
      }}
    >
      {props.children}
    </AuthContext.Provider>
  );
};
