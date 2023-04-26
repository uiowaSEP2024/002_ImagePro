import { CrudFilters, CrudSorting, CrudFilter, CrudSort, CrudOperators, SortOrder } from "../../interfaces";
export declare const parseTableParams: (url: string) => {
    parsedCurrent: number | "" | undefined;
    parsedPageSize: number | "" | undefined;
    parsedSorter: CrudSorting;
    parsedFilters: CrudFilters;
};
export declare const parseTableParamsFromQuery: (params: any) => {
    parsedCurrent: number | "" | undefined;
    parsedPageSize: number | "" | undefined;
    parsedSorter: CrudSorting;
    parsedFilters: CrudFilters;
};
/**
 * @internal This function is used to stringify table params from the useTable hook.
 */
export declare const stringifyTableParams: (params: {
    [key: string]: any;
    pagination?: {
        current?: number | undefined;
        pageSize?: number | undefined;
    } | undefined;
    sorters: CrudSorting;
    filters: CrudFilters;
}) => string;
export declare const compareFilters: (left: CrudFilter, right: CrudFilter) => boolean;
export declare const compareSorters: (left: CrudSort, right: CrudSort) => boolean;
export declare const unionFilters: (permanentFilter: CrudFilters, newFilters: CrudFilters, prevFilters?: CrudFilters) => CrudFilters;
export declare const unionSorters: (permanentSorter: CrudSorting, newSorters: CrudSorting) => CrudSorting;
export declare const setInitialFilters: (permanentFilter: CrudFilters, defaultFilter: CrudFilters) => CrudFilters;
export declare const setInitialSorters: (permanentSorter: CrudSorting, defaultSorter: CrudSorting) => CrudSorting;
export declare const getDefaultSortOrder: (columnName: string, sorter?: CrudSorting) => SortOrder | undefined;
export declare const getDefaultFilter: (columnName: string, filters?: CrudFilters, operatorType?: CrudOperators) => CrudFilter["value"] | undefined;
//# sourceMappingURL=index.d.ts.map