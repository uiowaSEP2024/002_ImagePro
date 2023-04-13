import { useContext, useEffect } from "react";

import { AuthContext } from "@/contexts/authContext";
import { useRouter } from "next/router";

export const useAuthContext = () => useContext(AuthContext);

export const useEnsureAuthenticated = () => {
  const {isAuthenticating, currentUser } = useAuthContext()
  const router= useRouter()

  useEffect(() => {
    if ( !isAuthenticating && !currentUser){
      router.push("/login")
    }
  }, [isAuthenticating, currentUser, router]);
}



export const useEnsureUnauthenticated = () => {
  const {isAuthenticating, currentUser } = useAuthContext()
  const router= useRouter()

  useEffect(() => {
    if (currentUser){
      router.push("/dashboard")
    }
  }, [isAuthenticating, currentUser, router]);
}

