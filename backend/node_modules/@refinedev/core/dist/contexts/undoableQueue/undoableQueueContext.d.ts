import React, { ReactNode } from "react";
import { IUndoableQueue, IUndoableQueueContext } from "../../interfaces";
export declare const UndoableQueueContext: React.Context<IUndoableQueueContext>;
export declare const undoableQueueReducer: (state: IUndoableQueue[], action: any) => any[];
export declare const UndoableQueueContextProvider: React.FC<{
    children: ReactNode;
}>;
//# sourceMappingURL=undoableQueueContext.d.ts.map