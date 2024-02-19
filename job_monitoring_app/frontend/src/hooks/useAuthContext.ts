import { useContext, useEffect } from "react";

import { AuthContext } from "@/contexts/authContext";
import { useRouter } from "next/router";
import { User } from "@/data/types";

export const useAuthContext = () => useContext(AuthContext);

export const useEnsureAuthenticated = (roles: User["role"][] = []) => {
  const { isAuthenticating, currentUser } = useAuthContext();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticating) {
      return;
    }

    if (!currentUser) {
      router.push("/login");
      return;
    }

    if (roles.length && !roles.includes(currentUser.role)) {
      router.push("/dashboard");
      return;
    }
  }, [isAuthenticating, currentUser, router, roles]);
};

export const useEnsureUnauthenticated = () => {
  const { isAuthenticating, currentUser } = useAuthContext();
  const router = useRouter();

  useEffect(() => {
    if (currentUser) {
      router.push("/dashboard");
    }
  }, [isAuthenticating, currentUser, router]);
};
