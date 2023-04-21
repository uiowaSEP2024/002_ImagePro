import { Table, Tbody, Tr, Td, TableProps, Text } from "@chakra-ui/react";
import React from "react";

type MetadataProps = {
  metadata: Record<string, any>;
} & TableProps;

export const Metadata = React.forwardRef<HTMLElement, MetadataProps>(
  function MetadataRef({ metadata, ...rest }, ref) {
    return (
      <Table ref={ref} width={"fit-content"} variant={"unstyled"} {...rest}>
        <Tbody>
          {Object.entries(metadata).map(([key, value]) => (
            <Tr key={key}>
              <Td mr={6} pl={0} py={1}>
                <Text fontSize={"inherit"}>{key}</Text>
              </Td>
              <Td py={1} px={0}>
                <Text fontSize={"inherit"}>{value}</Text>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    );
  }
);
