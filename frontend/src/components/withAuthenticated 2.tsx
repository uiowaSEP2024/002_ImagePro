import { useAuthContext, useEnsureAuthenticated, useEnsureUnauthenticated } from "@/hooks/useAuthContext";

/**
 * A HOC that ensures the user is authenticated before rendering the wrapped component
 * @param WrappedComponent 
 * @returns 
 */
export const withAuthenticated = <P extends object>(
  WrappedComponent: React.ComponentType<P>
) => {

  const ComponentWithAuth = (props: P) => {
    useEnsureAuthenticated()
    const { isAuthenticating } = useAuthContext();
    if (isAuthenticating) return null;
    return <WrappedComponent {...props} />;
  };

  return ComponentWithAuth;
};


/**
 * A HOC that ensures the user is un-authenticated before rendering the wrapped component
 * @param WrappedComponent 
 * @returns 
 */
export const withUnauthenticated = <P extends object>(
  WrappedComponent: React.ComponentType<P>
) => {

  const ComponentWithAuth = (props: P) => {
    useEnsureUnauthenticated()
    const { isAuthenticating } = useAuthContext();
    if (isAuthenticating) return null;
    return <WrappedComponent {...props} />;
  };

  return ComponentWithAuth;
};