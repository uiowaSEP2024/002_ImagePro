import { User } from "@/data/types";
import {
  useAuthContext,
  useEnsureAuthenticated,
  useEnsureUnauthenticated
} from "@/hooks/useAuthContext";

/**
 * A Higher Order Component (HOC) that ensures the user is authenticated before rendering the wrapped component.
 * If the user is not authenticated, it will not render the wrapped component.
 * It also supports role-based authentication by accepting an array of roles as an optional parameter.
 * Only users with a role that is included in the roles array will be able to access the wrapped component.
 *
 * @param WrappedComponent - The component to be wrapped by the HOC.
 * @param roles - An optional array of user roles. If provided, only users with a role that is included in this array will be able to access the wrapped component.
 * @returns - A new component that wraps the original component with authentication logic.
 */
export const withAuthenticated = <P extends object>(
  WrappedComponent: React.ComponentType<P>,
  roles: User["role"][] = []
) => {
  const ComponentWithAuth = (props: P) => {
    useEnsureAuthenticated(roles);
    const { isAuthenticating } = useAuthContext();
    if (isAuthenticating) return null;
    return <WrappedComponent {...props} />;
  };

  return ComponentWithAuth;
};

/**
 * A Higher Order Component (HOC) that ensures the user is unauthenticated before rendering the wrapped component.
 * If the user is authenticated, it will not render the wrapped component.
 *
 * @param WrappedComponent - The component to be wrapped by the HOC.
 * @returns - A new component that wraps the original component with authentication logic.
 */
export const withUnauthenticated = <P extends object>(
  WrappedComponent: React.ComponentType<P>
) => {
  const ComponentWithAuth = (props: P) => {
    useEnsureUnauthenticated();
    const { isAuthenticating } = useAuthContext();
    if (isAuthenticating) return null;
    return <WrappedComponent {...props} />;
  };

  return ComponentWithAuth;
};
