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

  // Define the logOut function.
  const logOut = async () => {
    try {
      await fetchLogout();
      await refreshAuth()
      router.push("/login");
    } catch (e) {
      throw e
    }
  };

  // Define the logIn function.
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

  // Define the refreshAuth function.
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
