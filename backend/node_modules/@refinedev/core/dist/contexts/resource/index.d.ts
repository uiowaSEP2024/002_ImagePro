import React from "react";
import { IResourceContext } from "./IResourceContext";
import { ResourceProps } from "../../interfaces/bindings/resource";
export { IResourceItem, IResourceComponents, IResourceComponentsProps, IResourceContext, } from "../../interfaces/bindings/resource";
export declare const ResourceContext: React.Context<IResourceContext>;
export declare const ResourceContextProvider: React.FC<React.PropsWithChildren<{
    resources: ResourceProps[];
}>>;
//# sourceMappingURL=index.d.ts.map