import { fetchCheckUserLoggedIn, fetchLogin, fetchLogout } from "@/data";
import { User } from "@/data/types";
import { useRouter } from "next/router";
import React, { createContext, useEffect, useState } from "react";

interface IAuthContextProps {
  currentUser?: User;
  isAuthenticating: boolean;
  setCurrentUser: (user: any) => void;
  setIsAuthenticating: (loading: boolean) => void;
  logOut: () => Promise<void>;
  logIn: (email: string, password: string) =>  Promise<{user: User}|void>;
  refreshAuth: () => Promise<void>;
}

export const AuthContext = createContext<IAuthContextProps>({
  currentUser: undefined,
  isAuthenticating: true,
  setCurrentUser: () => {},
  setIsAuthenticating: () => {},
  logOut: async () =>{},
  logIn: async () =>{},
  refreshAuth: async () =>{}
});

export const AuthContextProvider = (props: React.PropsWithChildren) => {
  const [currentUser, setCurrentUser] = useState<User>();
  const [isAuthenticating, setIsAuthenticating] = useState(true);
  const router = useRouter();



  useEffect(()=>{
    refreshAuth()
  }, [])

  const logOut = async () => {
    try {
      await fetchLogout();
      await refreshAuth()
      router.push("/login");
    } catch (e) {
      throw e
    }
  };


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

  const refreshAuth = async () =>{
    try{
      const data = await fetchCheckUserLoggedIn()
      setCurrentUser(data.user)
    }catch(e){
      setCurrentUser(undefined)
    }
    setIsAuthenticating(false)
  }


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
