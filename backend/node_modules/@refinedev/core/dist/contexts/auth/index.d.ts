import React, { PropsWithChildren } from "react";
import { ILegacyAuthContext, IAuthBindingsContext } from "../../interfaces";
/**
 * @deprecated `LegacyAuthContext` is deprecated with refine@4, use `AuthBindingsContext` instead, however, we still support `LegacyAuthContext` for backward compatibility.
 */
export declare const LegacyAuthContext: React.Context<ILegacyAuthContext>;
/**
 * @deprecated `LegacyAuthContextProvider` is deprecated with refine@4, use `AuthBindingsContextProvider` instead, however, we still support `LegacyAuthContextProvider` for backward compatibility.
 */
export declare const LegacyAuthContextProvider: React.FC<ILegacyAuthContext & {
    children?: React.ReactNode;
}>;
export declare const AuthBindingsContext: React.Context<Partial<IAuthBindingsContext>>;
export declare const AuthBindingsContextProvider: React.FC<PropsWithChildren<IAuthBindingsContext>>;
/**
 * @deprecated `useLegacyAuthContext` is deprecated with refine@4, use `useAuthBindingsContext` instead, however, we still support `useLegacyAuthContext` for backward compatibility.
 */
export declare const useLegacyAuthContext: () => ILegacyAuthContext;
export declare const useAuthBindingsContext: () => Partial<IAuthBindingsContext>;
//# sourceMappingURL=index.d.ts.map